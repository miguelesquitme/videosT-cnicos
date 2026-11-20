import React from 'react';
import {Audio, Sequence, staticFile, useCurrentFrame, useVideoConfig, interpolate, Easing, Img} from 'remotion';

export const useT = () => { const f = useCurrentFrame(); const {fps} = useVideoConfig(); return f / fps; };
export const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
export const ease = (x) => 1 - Math.pow(1 - clamp(x), 3);
export const ein = (t, a, d = 0.45) => ease((t - a) / d);           // 0→1 desde el segundo a
export const eout = (t, a, d = 0.35) => 1 - ease((t - a) / d);      // 1→0 desde el segundo a
export const lerp = (a, b, p) => a + (b - a) * p;
export const secOf = (props, k) => props.sec.find((s) => s.k === k);
export const loc = (t, s) => t - s.ini;                               // tiempo local de la sección
export const vis = (t, s, pre = 0.15, post = 0.35) => t >= s.ini - pre && t < s.ini + s.dur + post;

export const Voces = ({props}) => (
  <>
    {props.sec.map((s) => (
      <Sequence key={s.k} from={Math.round(s.ini * 30)} durationInFrames={Math.ceil((s.dur + 0.2) * 30)}>
        <Audio src={staticFile(`${props.clave}/${s.k}.wav`)} />
      </Sequence>
    ))}
  </>
);

export const Sfx = ({at, name, vol = 0.35}) => (
  <Sequence from={Math.max(0, Math.round(at * 30))} durationInFrames={60}>
    <Audio src={staticFile(`sfx/${name}.wav`)} volume={vol} />
  </Sequence>
);

export const Tornillo = ({x, y, r = 9, c = '#C9CED6'}) => (
  <g>
    <circle cx={x} cy={y} r={r} fill={c} stroke="#475467" strokeWidth={r * 0.18} />
    <path d={`M${x - r * 0.6} ${y}H${x + r * 0.6}M${x} ${y - r * 0.6}V${y + r * 0.6}`} stroke="#344054" strokeWidth={r * 0.22} />
  </g>
);

export const Cierre = ({t, ini, color = '#00E5FF', texto, fondo = 'rgba(10,14,40,0.92)'}) => {
  const p = ein(t, ini, 0.5);
  return (
    <div style={{position: 'absolute', left: 90, right: 90, top: 640, opacity: p, transform: `scale(${0.9 + 0.1 * p})`, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 34}}>
      {texto && <div style={{background: color, color: '#06101F', fontWeight: 900, fontSize: 44, padding: '14px 30px', borderRadius: 40, textAlign: 'center'}}>{texto}</div>}
      <div style={{background: fondo, border: `3px solid ${color}`, borderRadius: 36, padding: '40px 50px', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 22, width: 760}}>
        <Img src={staticFile('logo.png')} style={{width: 260}} />
        <div style={{color: '#FFFFFF', fontWeight: 900, fontSize: 56}}>@miguelesquit</div>
        <div style={{display: 'flex', gap: 24}}>
          <div style={{background: '#E5484D', color: 'white', fontWeight: 900, fontSize: 46, padding: '12px 28px', borderRadius: 40, transform: `scale(${ein(t, ini + 0.5, 0.3)})`}}>SUSCRÍBETE</div>
          <div style={{background: color, color: '#06101F', fontWeight: 900, fontSize: 46, padding: '12px 28px', borderRadius: 40, transform: `scale(${ein(t, ini + 0.8, 0.3)})`}}>SÍGUEME</div>
        </div>
      </div>
    </div>
  );
};
