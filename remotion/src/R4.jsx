// Reel R4 · ARRANQUE DE MOTORES: DIRECTO · ESTRELLA-DELTA · SUAVE.  Diseño "tablero HMI + osciloscopio".
import React from 'react';
import {AbsoluteFill} from 'remotion';
import {useT, ein, eout, clamp, lerp, ease, loc, vis, Voces, Sfx, Tornillo, Cierre} from './lib';

const BG = '#0D1117', PANEL = '#161B22', AM = '#FFB020', VE = '#39FF88', RO = '#FF5A5F', AZ = '#58A6FF', GR = '#8B949E';

// ---------------------------------------------------------------- piezas (vista frontal)
const Contactor = ({x, y, s = 1, et = 'KM1', on = false}) => (
  <g transform={`translate(${x},${y}) scale(${s})`}>
    <rect x={-70} y={-100} width={140} height={200} rx={10} fill="#C9CED6" stroke="#475467" strokeWidth={3} />
    <rect x={-66} y={-96} width={50} height={192} rx={8} fill="#FFFFFF" opacity={0.25} />
    {[-42, 0, 42].map((dx, i) => <g key={i}><rect x={dx - 17} y={-92} width={34} height={30} rx={3} fill="#98A2B3" /><Tornillo x={dx} y={-77} r={10} />
      <rect x={dx - 17} y={62} width={34} height={30} rx={3} fill="#98A2B3" /><Tornillo x={dx} y={77} r={10} />
      <text x={dx} y={-50} fontSize={11} fontWeight={800} fill="#344054" textAnchor="middle">{`${2 * i + 1}/L${i + 1}`}</text>
      <text x={dx} y={57} fontSize={11} fontWeight={800} fill="#344054" textAnchor="middle">{`${2 * i + 2}/T${i + 1}`}</text></g>)}
    <rect x={-40} y={-34} width={80} height={56} rx={6} fill="#98A2B3" stroke="#475467" strokeWidth={2} />
    <rect x={-22} y={-26} width={44} height={24} rx={3} fill={on ? '#12924F' : '#344054'} />
    <text x={0} y={-9} fontSize={13} fontWeight={900} fill="white" textAnchor="middle">{on ? 'I' : 'O'}</text>
    <text x={0} y={16} fontSize={16} fontWeight={900} fill="#101828" textAnchor="middle">{et}</text>
    <text x={-56} y={-40} fontSize={10} fontWeight={800} fill="#344054">A1</text><text x={46} y={-40} fontSize={10} fontWeight={800} fill="#344054">A2</text>
    {on && <rect x={-70} y={-100} width={140} height={200} rx={10} fill="none" stroke={VE} strokeWidth={5} opacity={0.9} />}
  </g>
);

const Termico = ({x, y, s = 1}) => (
  <g transform={`translate(${x},${y}) scale(${s})`}>
    <rect x={-70} y={-48} width={140} height={96} rx={8} fill="#D0D5DD" stroke="#475467" strokeWidth={3} />
    <circle cx={-28} cy={0} r={22} fill="#F2F4F7" stroke="#475467" strokeWidth={2} />
    <line x1={-28} y1={0} x2={-14} y2={-14} stroke="#101828" strokeWidth={4} />
    <circle cx={22} cy={-12} r={11} fill="#1D4ED8" /><text x={22} y={-8} fontSize={9} fontWeight={900} fill="white" textAnchor="middle">R</text>
    <rect x={38} y={-22} width={20} height={18} rx={3} fill="#E5484D" />
    {[-42, 0, 42].map((dx, i) => <Tornillo key={i} x={dx} y={36} r={8} />)}
    <text x={10} y={20} fontSize={10} fontWeight={800} fill="#344054">95 96 97 98</text>
  </g>
);

const Temporizador = ({x, y, on = false}) => (
  <g transform={`translate(${x},${y})`}>
    <rect x={-36} y={-90} width={72} height={180} rx={8} fill="#E4E7EC" stroke="#475467" strokeWidth={3} />
    <circle cx={0} cy={-20} r={22} fill="#F2F4F7" stroke="#475467" strokeWidth={2} />
    <line x1={0} y1={-20} x2={12} y2={-34} stroke="#101828" strokeWidth={4} />
    <text x={0} y={16} fontSize={13} fontWeight={900} fill="#344054" textAnchor="middle">KT · s</text>
    <circle cx={0} cy={36} r={7} fill={on ? AM : '#5A4A1E'} />
    <Tornillo x={-16} y={-72} r={7} /><Tornillo x={16} y={-72} r={7} /><Tornillo x={-16} y={72} r={7} /><Tornillo x={16} y={72} r={7} />
  </g>
);

const Suave = ({x, y, on = 0}) => (
  <g transform={`translate(${x},${y})`}>
    <rect x={-150} y={-190} width={300} height={380} rx={14} fill="#2B3038" stroke="#0E1116" strokeWidth={4} />
    {[...Array(9)].map((_, i) => <rect key={i} x={-140 + i * 31} y={-186} width={14} height={40} fill="#8A929C" />)}
    {[...Array(9)].map((_, i) => <rect key={i} x={-140 + i * 31} y={146} width={14} height={40} fill="#8A929C" />)}
    {['L1', 'L2', 'L3'].map((n, i) => <g key={n}><Tornillo x={-80 + i * 80} y={-120} r={13} /><text x={-80 + i * 80} y={-92} fontSize={16} fontWeight={900} fill="#E4E7EC" textAnchor="middle">{`${2 * i + 1}/${n}`}</text></g>)}
    {['T1', 'T2', 'T3'].map((n, i) => <g key={n}><Tornillo x={-80 + i * 80} y={120} r={13} /><text x={-80 + i * 80} y={102} fontSize={16} fontWeight={900} fill="#E4E7EC" textAnchor="middle">{`${2 * i + 2}/${n}`}</text></g>)}
    {[['t ARR', 0.6], ['U INI', 0.35], ['I LÍM', 0.5]].map(([n, a], i) => (
      <g key={n}><circle cx={-90 + i * 90} cy={-20} r={28} fill="#E4E7EC" stroke="#101828" strokeWidth={2} />
        <line x1={-90 + i * 90} y1={-20} x2={-90 + i * 90 + 20 * Math.cos(Math.PI * (1.25 - 1.5 * a))} y2={-20 - 20 * Math.sin(Math.PI * (1.25 - 1.5 * a))} stroke="#101828" strokeWidth={4} />
        <text x={-90 + i * 90} y={28} fontSize={14} fontWeight={900} fill="#E4E7EC" textAnchor="middle">{n}</text></g>))}
    <circle cx={-110} cy={64} r={8} fill={VE} /><text x={-96} y={69} fontSize={13} fontWeight={800} fill="#AEB6C2">ON</text>
    <circle cx={-40} cy={64} r={8} fill={on > 0.98 ? AM : '#5A4A1E'} /><text x={-26} y={69} fontSize={13} fontWeight={800} fill="#AEB6C2">BYPASS</text>
    <circle cx={60} cy={64} r={8} fill="#5A1A22" /><text x={74} y={69} fontSize={13} fontWeight={800} fill="#AEB6C2">FALLA</text>
    <text x={0} y={-150} fontSize={18} fontWeight={900} fill="#E4E7EC" textAnchor="middle">ARRANCADOR SUAVE</text>
  </g>
);

const Motor = ({x, y, s = 1, rpm = 0, t = 0}) => (
  <g transform={`translate(${x},${y}) scale(${s})`}>
    <rect x={-130} y={-70} width={230} height={140} rx={14} fill="#3E6A8C" stroke="#1F3A50" strokeWidth={3} />
    {[...Array(8)].map((_, i) => <line key={i} x1={-120} x2={90} y1={-55 + i * 16} y2={-55 + i * 16} stroke="#2B5070" strokeWidth={4} />)}
    <rect x={-190} y={-62} width={64} height={124} rx={20} fill="#34556F" stroke="#1F3A50" strokeWidth={3} />
    <rect x={100} y={-50} width={24} height={100} rx={6} fill="#5C8BB0" />
    <rect x={124} y={-14} width={70} height={28} fill="#C9CED6" stroke="#667085" strokeWidth={2} />
    <rect x={150} y={-14 + 10 * (1 + Math.sin(t * rpm / 60 * 2 * Math.PI)) } width={30} height={6} fill="#5B6472" />
    <rect x={-60} y={-100} width={90} height={34} rx={6} fill="#5C8BB0" stroke="#1F3A50" strokeWidth={2} />
    <rect x={-70} y={70} width={60} height={22} fill="#3E6A8C" /><rect x={40} y={70} width={60} height={22} fill="#3E6A8C" />
    <rect x={-50} y={-30} width={80} height={44} rx={3} fill="#E4E7EC" />
    <text x={-10} y={-12} fontSize={10} fontWeight={900} fill="#101828" textAnchor="middle">10 hp · 460 V</text>
    <text x={-10} y={4} fontSize={10} fontWeight={900} fill="#101828" textAnchor="middle">14 A · 1765 rpm</text>
  </g>
);

// ---------------------------------------------------------------- osciloscopio de corriente
const Osc = ({fn, prog, color = VE, titulo, marcas = [], y = 1030, h = 430, maxI = 8}) => {
  const x0 = 120, W = 860;
  const n = 300; let d = '';
  for (let i = 0; i <= n * prog; i++) { const u = i / n; const v = fn(u); d += `${i ? 'L' : 'M'}${x0 + u * W},${y + h - (v / maxI) * (h - 40)}`; }
  return (
    <g>
      <rect x={60} y={y - 60} width={960} height={h + 110} rx={22} fill="#06120B" stroke="#1F3A2A" strokeWidth={4} />
      {[...Array(9)].map((_, i) => <line key={i} x1={x0} x2={x0 + W} y1={y + h - i * (h - 40) / 8} y2={y + h - i * (h - 40) / 8} stroke="#123321" strokeWidth={2} />)}
      {[...Array(11)].map((_, i) => <line key={i} x1={x0 + i * W / 10} x2={x0 + i * W / 10} y1={y + 40} y2={y + h} stroke="#123321" strokeWidth={2} />)}
      {[0, 2, 4, 6, 8].map((v) => <text key={v} x={x0 - 14} y={y + h - (v / maxI) * (h - 40) + 8} fontSize={24} fontWeight={800} fill="#3E8E5E" textAnchor="end">{v}×</text>)}
      <text x={x0} y={y - 18} fontSize={30} fontWeight={900} fill={color}>{titulo}</text>
      <text x={x0 + W} y={y + h + 38} fontSize={24} fontWeight={800} fill="#3E8E5E" textAnchor="end">tiempo →</text>
      <path d={d} stroke={color} strokeWidth={14} opacity={0.18} fill="none" />
      <path d={d} stroke={color} strokeWidth={5} fill="none" />
      {marcas.map(([u, v, txt, c], i) => prog > u && <g key={i}><circle cx={x0 + u * W} cy={y + h - (v / maxI) * (h - 40)} r={10} fill={c} />
        <text x={x0 + u * W + 18} y={y + h - (v / maxI) * (h - 40) - 10} fontSize={30} fontWeight={900} fill={c}>{txt}</text></g>)}
    </g>
  );
};

const fDOL = (u) => u < 0.04 ? 0 : (u < 0.32 ? 7 - 0.6 * ((u - 0.04) / 0.28) : Math.max(1, 6.4 - (u - 0.32) * 40));
const fYD = (u) => u < 0.04 ? 0 : (u < 0.5 ? 2.3 - 0.9 * ((u - 0.04) / 0.46) : (u < 0.53 ? 4.6 : Math.max(1, 4.6 - (u - 0.53) * 30)));
const fSS = (u) => u < 0.04 ? 0 : (u < 0.2 ? lerp(0.6, 3, (u - 0.04) / 0.16) : (u < 0.6 ? 3 : Math.max(1, 3 - (u - 0.6) * 12)));

const Escena = ({lt, d, children}) => <AbsoluteFill style={{opacity: Math.min(ein(lt, 0, 0.35), eout(lt, d + 0.05, 0.3))}}>{children}</AbsoluteFill>;

const Etiq = ({top, left = 60, right = 60, color, children, o = 1}) => (
  <div style={{position: 'absolute', top, left, right, opacity: o, background: PANEL, borderLeft: `14px solid ${color}`, borderRadius: 14, padding: '18px 26px', color: 'white', fontWeight: 900, fontSize: 40}}>{children}</div>
);

export const R4 = (props) => {
  const t = useT();
  const S = Object.fromEntries(props.sec.map((s) => [s.k, s]));
  return (
    <AbsoluteFill style={{fontFamily: 'Montserrat', background: `linear-gradient(180deg, #11161D 0%, ${BG} 100%)`}}>
      <Voces props={props} />
      {props.sec.slice(1).map((s) => <Sfx key={s.k} at={s.ini - 0.25} name="whoosh" vol={0.22} />)}
      {/* barra de título tipo HMI */}
      <div style={{position: 'absolute', top: 70, left: 40, right: 40, height: 270, background: PANEL, border: '3px solid #30363D', borderRadius: 24}}>
        <div style={{position: 'absolute', top: 24, left: 34, color: GR, fontWeight: 900, fontSize: 40, letterSpacing: 3}}>{props.tit1}</div>
        <div style={{position: 'absolute', top: 78, left: 34, right: 30, color: AM, fontWeight: 900, fontSize: 56, lineHeight: 1.1, whiteSpace: 'pre'}}>{'DIRECTO · ESTRELLA-DELTA\n· SUAVE'}</div>
        <div style={{position: 'absolute', top: 30, right: 34, width: 22, height: 22, borderRadius: 11, background: Math.floor(t * 2) % 2 ? VE : '#14532D'}} />
      </div>
      {vis(t, S.gancho) && <Gancho lt={loc(t, S.gancho)} d={S.gancho.dur} t={t} />}
      {vis(t, S.p1) && <DOL lt={loc(t, S.p1)} d={S.p1.dur} t={t} />}
      {vis(t, S.p2) && <YD lt={loc(t, S.p2)} d={S.p2.dur} t={t} />}
      {vis(t, S.p3) && <SS lt={loc(t, S.p3)} d={S.p3.dur} t={t} />}
      {vis(t, S.p3b) && <Num lt={loc(t, S.p3b)} d={S.p3b.dur} />}
      {vis(t, S.p4) && <Resumen lt={loc(t, S.p4)} d={S.p4.dur} />}
      {t >= S.cierre.ini - 0.2 && <Cierre t={t} ini={S.cierre.ini} color={AM} texto="Directo · Estrella-delta · Suave" fondo="rgba(22,27,34,0.96)" />}
      <Sfx at={S.p1.ini + 2.0} name="pop" vol={0.4} />
    </AbsoluteFill>
  );
};

const Gancho = ({lt, d, t}) => (
  <Escena lt={lt} d={d}>
    <svg width={1080} height={1920} style={{position: 'absolute'}}>
      <Motor x={560} y={560} s={1.3} rpm={lt > 1 ? 1765 : 0} t={t} />
      <Osc fn={(u) => (u < 0.33 ? fDOL(u * 3) : u < 0.66 ? fYD((u - 0.33) * 3) : fSS((u - 0.66) * 3))} prog={clamp((lt - 0.6) / 4.8)} titulo="CORRIENTE DE ARRANQUE (× In)" color={VE} y={980} />
    </svg>
    <Etiq top={1580} color={AM} o={ein(lt, 3.5)}>3 métodos · 3 corrientes muy distintas</Etiq>
  </Escena>
);

const DOL = ({lt, d, t}) => (
  <Escena lt={lt} d={d}>
    <svg width={1080} height={1920} style={{position: 'absolute'}}>
      <Contactor x={230} y={560} s={1.5} et="KM1" on={lt > 1.8} />
      <Termico x={230} y={800} s={1.5} />
      <Motor x={740} y={640} s={1.15} rpm={lt > 1.8 ? 1765 : 0} t={t} />
      <path d="M335 560 C 450 560, 480 640, 560 640" stroke={lt > 1.8 ? VE : '#30363D'} strokeWidth={8} fill="none" />
      <text x={230} y={400} fontSize={34} fontWeight={900} fill={AZ} textAnchor="middle">voltaje pleno</text>
      <Osc fn={fDOL} prog={clamp((lt - 1.8) / 4.0)} titulo="DIRECTO" color={RO} y={1030}
        marcas={[[0.08, 7, '6 a 8 × In (IE3: más)', RO]]} />
    </svg>
    <Etiq top={1585} color={RO} o={ein(lt, 9.5)}>par máximo · golpe mecánico · caída de tensión</Etiq>
  </Escena>
);

const YD = ({lt, d, t}) => {
  const delta = lt > 9.5;
  const k = ein(lt, 9.5, 0.6);
  // devanados: estrella → delta
  const C = [850, 570], R = 115;
  const pts = [0, 1, 2].map((i) => [C[0] + R * Math.cos(-Math.PI / 2 + i * 2 * Math.PI / 3), C[1] + R * Math.sin(-Math.PI / 2 + i * 2 * Math.PI / 3)]);
  return (
    <Escena lt={lt} d={d}>
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        <Contactor x={125} y={580} s={1.05} et="KM1" on />
        <Contactor x={290} y={580} s={1.05} et="KM2 Y" on={!delta} />
        <Contactor x={455} y={580} s={1.05} et="KM3 Δ" on={delta} />
        <Temporizador x={600} y={580} on={!delta} />
        <text x={330} y={430} fontSize={28} fontWeight={900} fill={GR} textAnchor="middle">línea · estrella · delta + temporizador</text>
        {/* símbolo de conexión */}
        {pts.map((p, i) => {
          const q = pts[(i + 1) % 3];
          const a = [lerp(C[0], p[0], 1), lerp(C[1], p[1], 1)];
          return <g key={i}>
            <line x1={lerp(C[0], q[0], k)} y1={lerp(C[1], q[1], k)} x2={p[0]} y2={p[1]} stroke={delta ? AZ : AM} strokeWidth={10} strokeLinecap="round" />
          </g>;
        })}
        <text x={C[0]} y={C[1] + 190} fontSize={40} fontWeight={900} fill={delta ? AZ : AM} textAnchor="middle">{delta ? 'DELTA' : 'ESTRELLA'}</text>
        {!delta && <text x={C[0]} y={C[1] + 236} fontSize={30} fontWeight={800} fill="#E4E7EC" textAnchor="middle">V línea ÷ √3 por devanado</text>}
        <Osc fn={fYD} prog={clamp((lt - 2.0) / 12.0)} titulo="ESTRELLA-DELTA" color={AM} y={1030}
          marcas={[[0.1, 2.3, '≈ 1/3 de corriente y de par', AM], [0.53, 4.6, 'pico en la transición', RO]]} />
      </svg>
      <Etiq top={1585} color={AZ} o={ein(lt, 15.5)}>motor de 6 puntas · delta a tu voltaje de línea</Etiq>
    </Escena>
  );
};

const SS = ({lt, d, t}) => {
  const ramp = clamp((lt - 2.0) / 8.0);
  const alfa = lerp(0.75, 0.0, ramp);             // ángulo de disparo (fracción de semiciclo)
  const x0 = 620, y0 = 560, W = 380, A = 110;
  let dwf = '';
  for (let i = 0; i <= 240; i++) {
    const u = i / 240, ang = u * 4 * Math.PI, sem = (ang % Math.PI) / Math.PI;
    const v = sem < alfa ? 0 : Math.sin(ang);
    dwf += `${i ? 'L' : 'M'}${x0 + u * W},${y0 - v * A}`;
  }
  return (
    <Escena lt={lt} d={d}>
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        <Suave x={250} y={620} on={clamp((lt - 13) / 1)} />
        <rect x={x0 - 20} y={y0 - 150} width={W + 40} height={300} rx={18} fill="#06120B" stroke="#1F3A2A" strokeWidth={3} />
        <line x1={x0} x2={x0 + W} y1={y0} y2={y0} stroke="#123321" strokeWidth={2} />
        <path d={dwf} stroke={AZ} strokeWidth={5} fill="none" />
        <text x={x0 + W / 2} y={y0 + 190} fontSize={28} fontWeight={900} fill={AZ} textAnchor="middle">tiristores recortan la onda</text>
        <text x={x0 + W / 2} y={y0 + 230} fontSize={28} fontWeight={900} fill={AZ} textAnchor="middle">→ voltaje en rampa</text>
        <Osc fn={fSS} prog={clamp((lt - 2.0) / 11.0)} titulo="ARRANCADOR SUAVE" color={AZ} y={1030}
          marcas={[[0.3, 3, 'límite 3 a 4,5 × In', AZ]]} />
      </svg>
      <Etiq top={1585} color={AZ} o={ein(lt, 5.5)}>par ∝ V²: arranque progresivo, sin golpes</Etiq>
    </Escena>
  );
};

const Num = ({lt, d}) => {
  const filas = [['DIRECTO', 112, '> 100 A', RO, 1.5], ['ESTRELLA-DELTA', 37, '≈ 37 A', AM, 5.5], ['SUAVE (límite 3×)', 42, '42 A', AZ, 9.5]];
  return (
    <Escena lt={lt} d={d}>
      <div style={{position: 'absolute', top: 420, left: 60, right: 60, background: '#E4E7EC', borderRadius: 18, padding: '24px 30px', border: '4px solid #98A2B3'}}>
        <div style={{color: '#101828', fontWeight: 900, fontSize: 46}}>MOTOR 10 hp · 460 V</div>
        <div style={{color: '#344054', fontWeight: 900, fontSize: 64}}>In = 14 A</div>
        <div style={{color: '#475467', fontWeight: 800, fontSize: 26}}>NEC 2020 · Tabla 430.250</div>
      </div>
      {filas.map(([n, v, txt, c, a], i) => {
        const p = ease((lt - a) / 1.2);
        return (
          <div key={n} style={{position: 'absolute', top: 760 + i * 280, left: 60, right: 60, opacity: ein(lt, a - 0.2)}}>
            <div style={{color: c, fontWeight: 900, fontSize: 44}}>{n}</div>
            <div style={{display: 'flex', alignItems: 'center', gap: 20, marginTop: 8}}>
              <div style={{width: `${p * v / 112 * 640}px`, height: 70, background: c, borderRadius: 12}} />
              <div style={{color: 'white', fontWeight: 900, fontSize: 70}}>{p >= 0.99 ? txt : `${Math.round(p * v)} A`}</div>
            </div>
          </div>
        );
      })}
    </Escena>
  );
};

const Resumen = ({lt, d}) => {
  const cols = [['DIRECTO', RO, ['Corriente: máxima', 'Par: máximo', 'Golpe: fuerte'], 0.3],
                ['ESTRELLA-DELTA', AM, ['Corriente: ≈ 1/3', 'Par: ≈ 1/3', 'Arranque en vacío'], 3.5],
                ['SUAVE', AZ, ['Corriente: ajustable', 'Rampa sin golpes', 'Bombas · ventiladores · bandas'], 8.5]];
  return (
    <Escena lt={lt} d={d}>
      {cols.map(([n, c, it, a], i) => (
        <div key={n} style={{position: 'absolute', top: 420 + i * 330, left: 60, right: 60, opacity: ein(lt, a), transform: `translateX(${(1 - ein(lt, a)) * 60}px)`,
          background: PANEL, border: `4px solid ${c}`, borderRadius: 22, padding: '20px 30px'}}>
          <div style={{color: c, fontWeight: 900, fontSize: 52}}>{n}</div>
          {it.map((x) => <div key={x} style={{color: 'white', fontWeight: 800, fontSize: 38, marginTop: 6}}>• {x}</div>)}
        </div>
      ))}
      <Etiq top={1430} color={VE} o={ein(lt, 14.0)}>¿Variar la velocidad? Eso ya es un VARIADOR</Etiq>
    </Escena>
  );
};
