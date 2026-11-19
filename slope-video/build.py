#!/usr/bin/env python3
"""تجميع الفيديو النهائي: 5 مقاطع × 8 ث + تعليق صوتي مقسّم + ترجمة كلمة بكلمة + مؤثرات.
التشغيل:  node render_captions.mjs && python3 build.py
"""
import json, subprocess, os

ROOT = os.path.dirname(os.path.abspath(__file__))
A = lambda p: os.path.join(ROOT, 'assets', p)
OUT = os.path.join(ROOT, 'out')
SCENE = 8.0          # مدة كل مشهد
LEAD = 0.20          # بداية الكلام بعد بداية المشهد
# حدود أجزاء التعليق الصوتي داخل vo_a.mp3 (من توقيت الكلمات)
VO_CUTS = [0.0, 6.36, 14.12, 21.66, 28.04, 33.84]
WHOOSH_AT = [7.55, 15.55, 23.55, 31.55]                    # قبيل كل انتقال
POP_AT = [18.32, 20.35, 24.46, 26.86, 28.74]                # ظهور الأضلاع والإشارات

overlays = json.load(open(os.path.join(OUT, 'overlays.json')))

inputs, fc = [], []
def add(args):
    inputs.extend(args); return len([a for a in inputs if a == '-i']) - 1

# 1) المقاطع: تمديد كل مقطع إلى 8 ث، رفع الدقة إلى 1080x1920، 30fps
vids = []
for n in range(1, 6):
    i = add(['-i', A(f'clip{n}.mp4')])
    dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                                         '-of', 'csv=p=0', A(f'clip{n}.mp4')]).decode())
    fc.append(f'[{i}:v]setpts=PTS*{SCENE/dur:.6f},scale=1080:1920:flags=lanczos,fps=30,'
              f'trim=duration={SCENE},setpts=PTS-STARTPTS,setsar=1[v{n}]')
    vids.append(f'[v{n}]')
fc.append(''.join(vids) + 'concat=n=5:v=1:a=0,format=yuva420p[base]')

# 2) طبقات الترجمة
last = 'base'
for k, o in enumerate(overlays):
    i = add(['-i', o['file']])
    nxt = f'c{k}'
    fc.append(f"[{last}][{i}:v]overlay=0:0:enable='between(t,{o['start']},{o['end'] - 0.001})'[{nxt}]")
    last = nxt
fc.append(f'[{last}]fade=t=in:st=0:d=0.25,format=yuv420p[vout]')

# 3) الصوت: خمسة أجزاء من التعليق، كل جزء في بداية مشهده
vo = add(['-i', A('vo_a.mp3')])
parts = []
for s in range(5):
    a, b = VO_CUTS[s], VO_CUTS[s + 1]
    d = int((s * SCENE + LEAD) * 1000)
    fc.append(f'[{vo}:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.03,'
              f'afade=t=out:st={b - a - 0.06:.3f}:d=0.06,adelay={d}|{d}[p{s}]')
    parts.append(f'[p{s}]')
fc.append(''.join(parts) + f'amix=inputs=5:normalize=0,loudnorm=I=-15:TP=-1.5:LRA=9[vo]')

# مؤثرات مولّدة (بدون ملفات خارجية): Whoosh = ضوضاء وردية بمرشح متحرك، Pop = نبضة جيبية قصيرة
sfx = []
for k, t in enumerate(WHOOSH_AT):
    fc.append(f'anoisesrc=color=pink:d=0.7:a=0.5,highpass=f=500,lowpass=f=4500,'
              f'afade=t=in:d=0.45:curve=exp,afade=t=out:st=0.45:d=0.25,volume=0.30,'
              f'adelay={int(t*1000)}|{int(t*1000)}[w{k}]')
    sfx.append(f'[w{k}]')
for k, t in enumerate(POP_AT):
    fc.append(f'sine=f=880:d=0.09,afade=t=out:st=0.02:d=0.07,volume=0.18,'
              f'adelay={int(t*1000)}|{int(t*1000)}[q{k}]')
    sfx.append(f'[q{k}]')
fc.append(''.join(sfx) + f'amix=inputs={len(sfx)}:normalize=0,aformat=channel_layouts=mono[sfx]')
fc.append('[vo][sfx]amix=inputs=2:normalize=0,aresample=48000,aformat=channel_layouts=stereo,'
          'apad,atrim=0:40,afade=t=out:st=39.6:d=0.4[aout]')

os.makedirs(OUT, exist_ok=True)
script = os.path.join(OUT, 'filter.txt')
open(script, 'w').write(';\n'.join(fc))
cmd = ['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', *inputs,
       '-filter_complex_script', script, '-map', '[vout]', '-map', '[aout]',
       '-t', '40', '-r', '30', '-c:v', 'libx264', '-preset', 'slow', '-b:v', '12M', '-maxrate', '16M',
       '-bufsize', '24M', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-movflags', '+faststart',
       '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', os.path.join(OUT, 'mayl_almustaqim_9x16.mp4')]
subprocess.run(cmd, check=True)
print('done →', os.path.join(OUT, 'mayl_almustaqim_9x16.mp4'))
