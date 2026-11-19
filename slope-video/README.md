# فيديو «ميل المستقيم» – Shorts 9:16 (40 ثانية)

الناتج: `out/mayl_almustaqim_9x16.mp4` (1080×1920، 30fps، H.264، AAC 48kHz).

## المحتويات
- `assets/scene1..5.png` صور البداية (Nano Banana Pro)، `assets/clip1..5.mp4` مقاطع الحركة (Grok Video 1.5 Lite، 7 ث تُمدَّد إلى 8 ث).
- `assets/vo_a.mp3` التعليق الصوتي (ElevenLabs v4 – صوت Muafaq)، و`vo_b.mp3` نسخة بديلة. `assets/words.json` توقيت كل كلمة.
- `captions.json` نصوص الشاشة وتوقيت ظهور كل كلمة وألوانها.
- `render_captions.mjs` يرسم طبقات الترجمة (Chromium + خط Cairo) ← `build.py` يجمّع كل شيء.

## التعديل
- **النص أو التوقيت أو اللون:** عدّل `captions.json` (التوقيت بالثواني من بداية الفيديو).
- **استبدال مقطع:** ضع ملفًا جديدًا باسم `assets/clipN.mp4` (أي مدة؛ يُمدَّد تلقائيًا إلى 8 ث).
- **استبدال الصوت:** ضع `assets/vo_a.mp3` جديدًا وعدّل `VO_CUTS` في `build.py` (حدود الأجزاء الخمسة).
- **المؤثرات:** `WHOOSH_AT` و`POP_AT` في `build.py`.

ثم:
```bash
node render_captions.mjs && python3 build.py
```
