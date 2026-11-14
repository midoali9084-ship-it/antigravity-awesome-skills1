import React from 'react';
import {registerRoot, Composition, AbsoluteFill, useCurrentFrame, interpolate} from 'remotion';
const T = () => { const f = useCurrentFrame(); const o = interpolate(f,[0,20],[0,1],{extrapolateRight:'clamp'});
 return <AbsoluteFill style={{background:'#111',justifyContent:'center',alignItems:'center'}}><h1 style={{color:'#fff',fontSize:120,opacity:o}}>Remotion OK</h1></AbsoluteFill>; };
registerRoot(() => <Composition id="Test" component={T} durationInFrames={90} fps={30} width={1080} height={1920} />);
