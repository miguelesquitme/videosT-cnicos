// Reel R3 · SENSOR ÓPTICO: ¿CUÁL MODO USAR?  Diseño "selección de personaje" (neón, tarjetas de estadísticas).
import React from 'react';
import {AbsoluteFill} from 'remotion';
import {useT, ein, eout, clamp, lerp, ease, secOf, loc, vis, Voces, Sfx, Tornillo, Cierre} from './lib';

const MAG = '#FF2BD6', CY = '#18F0FF', AM = '#FFC21A', VE = '#3DFF8F', RO = '#FF3B5C', BG = '#07060F';
const CX = 540, YT = 700, YB = 1000, YC = (YT + YB) / 2;   // banda transportadora (vista superior)

// ---------------------------------------------------------------- piezas (vista superior)
const SensorTop = ({x, y, dir = 1, tipo = 'emisor', out = false, ld = 'D', w = 128, h = 176}) => {
  // dir = 1: el lente apunta hacia abajo; -1: hacia arriba
  const top = dir === 1 ? y - h : y;        // la cara del lente queda en y
  const lensY = dir === 1 ? y - 12 : y + 12;
  const rearY = dir === 1 ? top : top + h;
  return (
    <g>
      {/* cable y conector M8 */}
      <rect x={x - 9} y={dir === 1 ? rearY - 60 : rearY} width={18} height={60} fill="#20242C" />
      <rect x={x - 22} y={dir === 1 ? rearY - 46 : rearY + 4} width={44} height={42} rx={6} fill="#8A929C" stroke="#475467" strokeWidth={2} />
      {[...Array(7)].map((_, i) => <line key={i} x1={x - 18 + i * 6} x2={x - 18 + i * 6} y1={dir === 1 ? rearY - 44 : rearY + 6} y2={dir === 1 ? rearY - 6 : rearY + 44} stroke="#5B6472" strokeWidth={2} />)}
      {/* cuerpo */}
      <rect x={x - w / 2} y={top} width={w} height={h} rx={14} fill="#2A2F38" stroke="#0E1116" strokeWidth={3} />
      <rect x={x - w / 2 + 6} y={top + 6} width={w * 0.42} height={h - 12} rx={10} fill="#FFFFFF" opacity={0.05} />
      {/* agujeros de montaje */}
      <Tornillo x={x - w / 2 + 22} y={top + h / 2} r={11} />
      <Tornillo x={x + w / 2 - 22} y={top + h / 2} r={11} />
      {/* indicadores y ajustes (en la cara superior) */}
      <circle cx={x - 22} cy={dir === 1 ? top + 30 : top + h - 30} r={8} fill={VE} />
      <circle cx={x + 2} cy={dir === 1 ? top + 30 : top + h - 30} r={8} fill={out ? '#FF9F1C' : '#4A3A1C'} />
      {out && <circle cx={x + 2} cy={dir === 1 ? top + 30 : top + h - 30} r={18} fill="#FF9F1C" opacity={0.35} />}
      <text x={x - 22} y={dir === 1 ? top + 54 : top + h - 46} fill="#AEB6C2" fontSize={11} fontWeight={800} textAnchor="middle">PWR</text>
      <text x={x + 2} y={dir === 1 ? top + 54 : top + h - 46} fill="#AEB6C2" fontSize={11} fontWeight={800} textAnchor="middle">OUT</text>
      {tipo !== 'emisor' && (
        <g>
          <circle cx={x + 34} cy={dir === 1 ? top + 30 : top + h - 30} r={11} fill="#98A2B3" stroke="#101828" strokeWidth={2} />
          <line x1={x + 27} x2={x + 41} y1={dir === 1 ? top + 30 : top + h - 30} y2={dir === 1 ? top + 30 : top + h - 30} stroke="#101828" strokeWidth={3} />
          <rect x={x + 18} y={dir === 1 ? top + 62 : top + h - 86} width={34} height={22} rx={4} fill="#101828" />
          <rect x={ld === 'L' ? x + 20 : x + 35} y={dir === 1 ? top + 64 : top + h - 84} width={15} height={18} rx={3} fill="#E4E7EC" />
          <text x={x + 35} y={dir === 1 ? top + 98 : top + h - 92} fill="#AEB6C2" fontSize={10} fontWeight={800} textAnchor="middle">L / D</text>
        </g>
      )}
      {/* lente(s) en la cara frontal */}
      {tipo === 'emisor' || tipo === 'receptor' ? (
        <rect x={x - 30} y={lensY - 8} width={60} height={16} rx={6} fill={tipo === 'emisor' ? '#5A1A22' : '#132A3A'} stroke="#0E1116" strokeWidth={2} />
      ) : (
        <g>
          <rect x={x - 46} y={lensY - 8} width={40} height={16} rx={6} fill="#5A1A22" stroke="#0E1116" strokeWidth={2} />
          <rect x={x + 6} y={lensY - 8} width={40} height={16} rx={6} fill="#132A3A" stroke="#0E1116" strokeWidth={2} />
        </g>
      )}
      <rect x={x - w / 2 + 10} y={dir === 1 ? top + h - 50 : top + 36} width={w - 20} height={20} rx={4} fill="#E4E7EC" />
      <text x={x} y={dir === 1 ? top + h - 35 : top + 51} fill="#101828" fontSize={11} fontWeight={900} textAnchor="middle">
        {tipo === 'emisor' ? 'EMISOR' : tipo === 'receptor' ? 'RECEPTOR' : tipo === 'retro' ? 'RETRO POLARIZADO' : 'DIFUSO'}
      </text>
    </g>
  );
};

const Reflector = ({x, y}) => (
  <g>
    <rect x={x - 70} y={y} width={140} height={58} rx={8} fill="#B4142B" stroke="#5A0A15" strokeWidth={3} />
    {[...Array(7)].map((_, i) => [...Array(3)].map((__, j) => (
      <polygon key={`${i}-${j}`} points={[0, 1, 2, 3, 4, 5].map((k) => {
        const a = Math.PI / 3 * k + Math.PI / 6, cx = x - 54 + i * 18 + (j % 2) * 9, cy = y + 12 + j * 16;
        return `${cx + 8 * Math.cos(a)},${cy + 8 * Math.sin(a)}`;
      }).join(' ')} fill="#E0243F" stroke="#7A0F1E" strokeWidth={1.2} />
    )))}
    <rect x={x - 12} y={y + 58} width={24} height={30} fill="#8A929C" />
    <Tornillo x={x} y={y + 76} r={8} />
    <text x={x} y={y + 110} fill="#FFB3C0" fontSize={20} fontWeight={900} textAnchor="middle">REFLECTOR PRISMÁTICO</text>
  </g>
);

const Banda = ({t, vel = 120}) => {
  const off = (t * vel) % 60;
  return (
    <g>
      <rect x={0} y={YT - 34} width={1080} height={26} fill="#5B6472" stroke="#2A2F38" strokeWidth={2} />
      <rect x={0} y={YB + 8} width={1080} height={26} fill="#5B6472" stroke="#2A2F38" strokeWidth={2} />
      {[...Array(10)].map((_, i) => <g key={i}><Tornillo x={60 + i * 108} y={YT - 21} r={7} /><Tornillo x={60 + i * 108} y={YB + 21} r={7} /></g>)}
      <rect x={0} y={YT - 8} width={1080} height={YB - YT + 16} fill="#1B1F27" />
      {[...Array(20)].map((_, i) => <line key={i} x1={i * 60 + off - 60} x2={i * 60 + off - 60} y1={YT - 6} y2={YB + 6} stroke="#262B34" strokeWidth={10} />)}
      <polygon points={`${980},${YC - 18} ${1020},${YC} ${980},${YC + 18}`} fill="#3A414C" />
    </g>
  );
};

const Caja = ({x, y = YC, s = 1, color = '#C89A5A'}) => (
  <g transform={`translate(${x},${y}) scale(${s})`}>
    <rect x={-80} y={-80} width={160} height={160} rx={6} fill={color} stroke="#7A5A2A" strokeWidth={3} />
    <rect x={-10} y={-80} width={20} height={160} fill="#E6C88A" opacity={0.85} />
    <line x1={-80} x2={80} y1={0} y2={0} stroke="#7A5A2A" strokeWidth={2} opacity={0.5} />
  </g>
);
const Lata = ({x, y = YC, brillo = 0}) => (
  <g transform={`translate(${x},${y})`}>
    <defs><radialGradient id="lat" cx="0.35" cy="0.35" r="0.7"><stop offset="0" stopColor="#FFFFFF" /><stop offset="0.35" stopColor="#D0D5DD" /><stop offset="1" stopColor="#6B7280" /></radialGradient></defs>
    <circle r={70} fill="url(#lat)" stroke="#475467" strokeWidth={3} />
    <circle r={58} fill="none" stroke="#98A2B3" strokeWidth={4} />
    <ellipse cx={-14} cy={-6} rx={24} ry={14} fill="#E4E7EC" stroke="#98A2B3" strokeWidth={2} />
    <circle r={70 + 30 * brillo} fill="#FFFFFF" opacity={0.25 * brillo} />
  </g>
);
const Negro = ({x, y = YC}) => (
  <g transform={`translate(${x},${y})`}><rect x={-75} y={-75} width={150} height={150} rx={10} fill="#0B0B0E" stroke="#3A3F47" strokeWidth={3} /><text y={8} fill="#5B6472" fontSize={22} fontWeight={900} textAnchor="middle">NEGRO MATE</text></g>
);
const Botella = ({x, y = YC}) => (
  <g transform={`translate(${x},${y})`}>
    <circle r={66} fill="#BFE9FF" opacity={0.18} stroke="#BFE9FF" strokeWidth={3} />
    <circle r={50} fill="none" stroke="#BFE9FF" strokeWidth={2} opacity={0.5} />
    <circle r={24} fill="#1D4ED8" stroke="#0B3A7A" strokeWidth={3} />
  </g>
);

// ---------------------------------------------------------------- tarjeta de "personaje"
const Tarjeta = ({lt, nombre, sub, color, stats, nota}) => {
  const p = ein(lt, 0.2, 0.5);
  return (
    <div style={{position: 'absolute', left: 60, right: 60, top: 1110, opacity: p, transform: `translateY(${(1 - p) * 60}px)`,
      background: 'rgba(20,16,40,0.92)', border: `4px solid ${color}`, borderRadius: 28, padding: '26px 34px', boxShadow: `0 0 40px ${color}55`}}>
      <div style={{display: 'flex', alignItems: 'baseline', gap: 18}}>
        <div style={{color, fontWeight: 900, fontSize: 64, letterSpacing: 2, textShadow: `0 0 18px ${color}`}}>{nombre}</div>
        <div style={{color: '#C9C2E8', fontWeight: 800, fontSize: 30}}>{sub}</div>
      </div>
      {stats.map(([lab, v], i) => {
        const q = ease((lt - 0.8 - i * 0.35) / 0.6) * v;
        return (
          <div key={lab} style={{display: 'flex', alignItems: 'center', gap: 16, marginTop: 14}}>
            <div style={{width: 300, color: '#FFFFFF', fontWeight: 800, fontSize: 27}}>{lab}</div>
            <div style={{flex: 1, height: 26, background: '#2A2440', borderRadius: 14, overflow: 'hidden'}}>
              <div style={{width: `${q}%`, height: '100%', background: `linear-gradient(90deg, ${color}, #FFFFFF)`, borderRadius: 14}} />
            </div>
          </div>
        );
      })}
      {nota && <div style={{marginTop: 16, color: AM, fontWeight: 900, fontSize: 28, opacity: ein(lt, nota[0], 0.4)}}>{nota[1]}</div>}
    </div>
  );
};

const Hud = ({t, props, round, color}) => (
  <>
    <div style={{position: 'absolute', top: 110, left: 0, right: 0, textAlign: 'center'}}>
      <div style={{color: '#FFFFFF', fontWeight: 900, fontSize: 58, letterSpacing: 3}}>{props.tit1}</div>
      <div style={{color: MAG, fontWeight: 900, fontSize: 92, textShadow: `0 0 26px ${MAG}`, marginTop: -6}}>{props.tit2}</div>
    </div>
    <div style={{position: 'absolute', top: 330, left: 60, right: 60, height: 14, background: '#1C1830', borderRadius: 8}}>
      <div style={{width: `${clamp(t / props.total) * 100}%`, height: '100%', background: `linear-gradient(90deg, ${CY}, ${MAG})`, borderRadius: 8}} />
    </div>
    {round && <div style={{position: 'absolute', top: 372, left: 60, color, fontWeight: 900, fontSize: 40, letterSpacing: 4, textShadow: `0 0 16px ${color}`}}>{round}</div>}
  </>
);

// ---------------------------------------------------------------- composición
export const R3 = (props) => {
  const t = useT();
  const S = Object.fromEntries(props.sec.map((s) => [s.k, s]));
  const fondo = (
    <AbsoluteFill style={{background: `radial-gradient(circle at 50% 35%, #1A0F3A 0%, ${BG} 60%)`}}>
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        {[...Array(30)].map((_, i) => <line key={i} x1={-400 + i * 70 + ((t * 30) % 70)} y1={1920} x2={i * 70 + ((t * 30) % 70)} y2={0} stroke="#1A1530" strokeWidth={2} />)}
      </svg>
    </AbsoluteFill>
  );
  let round = null, rcol = CY;
  if (t >= S.p1.ini - 0.2) { round = 'ROUND 1 · BARRERA'; rcol = CY; }
  if (t >= S.p2.ini - 0.2) { round = 'ROUND 2 · RETRORREFLECTIVO'; rcol = MAG; }
  if (t >= S.p3.ini - 0.2) { round = 'ROUND 3 · DIFUSO'; rcol = AM; }
  if (t >= S.p4.ini - 0.2) { round = 'POWER-UP · SUPRESIÓN DE FONDO'; rcol = VE; }
  if (t >= S.p5.ini - 0.2) { round = '¿QUIÉN GANA?'; rcol = RO; }
  if (t >= S.p6.ini - 0.2) { round = 'CONFIGURA · LIGHT ON / DARK ON'; rcol = CY; }
  if (t >= S.cierre.ini - 0.2) round = null;

  return (
    <AbsoluteFill style={{fontFamily: 'Montserrat'}}>
      {fondo}
      <Voces props={props} />
      {props.sec.slice(1).map((s) => <Sfx key={s.k} at={s.ini - 0.25} name="whoosh" vol={0.25} />)}
      <Hud t={t} props={props} round={round} color={rcol} />
      {vis(t, S.gancho) && <Gancho t={loc(t, S.gancho)} />}
      {vis(t, S.p1) && <Barrera t={t} lt={loc(t, S.p1)} d={S.p1.dur} />}
      {vis(t, S.p2) && <Retro t={t} lt={loc(t, S.p2)} d={S.p2.dur} />}
      {vis(t, S.p3) && <Difuso t={t} lt={loc(t, S.p3)} d={S.p3.dur} />}
      {vis(t, S.p4) && <Fondo lt={loc(t, S.p4)} d={S.p4.dur} />}
      {vis(t, S.p5) && <Gana lt={loc(t, S.p5)} d={S.p5.dur} />}
      {vis(t, S.p6) && <LightDark lt={loc(t, S.p6)} d={S.p6.dur} />}
      {t >= S.cierre.ini - 0.2 && <Cierre t={t} ini={S.cierre.ini} color={CY} texto="Barrera · Retro polarizado · Difuso" />}
      {<Sfx at={S.p1.ini + 6.0} name="tic" vol={0.4} />}
    </AbsoluteFill>
  );
};

const Escena = ({lt, d, children}) => {
  const o = Math.min(ein(lt, 0, 0.35), eout(lt, d + 0.05, 0.3));
  return <AbsoluteFill style={{opacity: o}}>{children}</AbsoluteFill>;
};

const Gancho = ({t}) => {
  const tx = 520 + (t - 2.2) * 260;
  const alarma = t > 4.2 && Math.floor(t * 6) % 2 === 0;
  return (
    <Escena lt={t} d={6.4}>
      <div style={{position: 'absolute', top: 470, left: 0, right: 0, textAlign: 'center'}}>
        <div style={{fontSize: 150, fontWeight: 900, color: '#FFFFFF', transform: `scale(${lerp(1.4, 1, ein(t, 0, 0.4))})`, opacity: ein(t, 0, 0.3), textShadow: `0 0 30px ${CY}`}}>3 SENSORES</div>
        <div style={{fontSize: 92, fontWeight: 900, color: CY, opacity: ein(t, 1.0, 0.4)}}>3 FORMAS DE VER</div>
      </div>
      <svg width={1080} height={1920} style={{position: 'absolute', opacity: ein(t, 2.0, 0.4)}}>
        <g transform="translate(0,420)"><Banda t={t} vel={t < 4.2 ? 220 : 0} /><Botella x={tx > 760 && t > 4.2 ? 760 : Math.min(tx, 760)} /></g>
      </svg>
      <div style={{position: 'absolute', top: 1560, left: 80, right: 80, textAlign: 'center', opacity: ein(t, 4.2, 0.2),
        background: alarma ? RO : '#5A0F1E', color: 'white', fontSize: 64, fontWeight: 900, borderRadius: 24, padding: '18px 0'}}>⚠ LÍNEA DETENIDA</div>
    </Escena>
  );
};

const Barrera = ({t, lt, d}) => {
  const xo = lerp(-180, 1260, clamp((lt - 1.5) / 6.5));
  const xb = lerp(-180, 1260, clamp((lt - 11.0) / 6.0));
  const corta = Math.abs(xo - CX) < 80;
  return (
    <Escena lt={lt} d={d}>
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        <Banda t={t} />
        <Caja x={xo} />
        <Botella x={xb} />
        <line x1={CX} x2={CX} y1={YT - 30} y2={corta ? (YC - 80) : YB + 30} stroke={RO} strokeWidth={10} opacity={0.9} />
        <line x1={CX} x2={CX} y1={YT - 30} y2={corta ? (YC - 80) : YB + 30} stroke="#FFB3C0" strokeWidth={3} />
        <SensorTop x={CX} y={YT - 36} dir={1} tipo="emisor" />
        <SensorTop x={CX} y={YB + 36} dir={-1} tipo="receptor" out={corta} />
      </svg>
      <Tarjeta lt={lt} nombre="BARRERA" sub="emisor + receptor" color={CY}
        stats={[['Alcance', 95], ['Margen de ganancia', 95], ['Tolera polvo', 90], ['Transparentes', 22], ['Facilidad de montaje', 35]]}
        nota={[11.5, '⚠ el transparente deja pasar el haz']} />
    </Escena>
  );
};

const Retro = ({t, lt, d}) => {
  const xo = lerp(-180, 1260, clamp((lt - 6.0) / 8.0));
  const pol = lt > 10.0;
  const enHaz = Math.abs(xo - CX) < 70;
  const engana = enHaz && !pol;
  return (
    <Escena lt={lt} d={d}>
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        <Banda t={t} />
        <Lata x={xo} brillo={enHaz ? 1 : 0} />
        <line x1={CX - 26} x2={CX - 26} y1={YT - 30} y2={enHaz ? YC - 70 : YB + 20} stroke={MAG} strokeWidth={8} />
        <line x1={CX + 26} x2={CX + 26} y1={enHaz ? YC - 70 : YB + 20} y2={YT - 30} stroke={CY} strokeWidth={8} strokeDasharray="22 12" strokeDashoffset={-t * 80} />
        <SensorTop x={CX} y={YT - 36} dir={1} tipo="retro" out={enHaz && pol} />
        <Reflector x={CX} y={YB + 30} />
        {lt > 2.5 && <text x={CX + 90} y={YT + 120} fill="#FFFFFF" fontSize={30} fontWeight={900} opacity={ein(lt, 2.5)}>el haz va y regresa</text>}
        {pol && (
          <g opacity={ein(lt, 10.0)}>
            <circle cx={CX - 300} cy={YT - 130} r={46} fill="none" stroke={VE} strokeWidth={5} />
            {[...Array(5)].map((_, i) => <line key={i} x1={CX - 336 + i * 18} x2={CX - 336 + i * 18} y1={YT - 165} y2={YT - 95} stroke={VE} strokeWidth={4} />)}
            <text x={CX - 300} y={YT - 60} fill={VE} fontSize={26} fontWeight={900} textAnchor="middle">FILTRO POLARIZADO</text>
          </g>
        )}
        {engana && <text x={CX} y={YC + 140} fill={RO} fontSize={44} fontWeight={900} textAnchor="middle">EL BRILLO LO ENGAÑA</text>}
        {enHaz && pol && <text x={CX} y={YC + 140} fill={VE} fontSize={44} fontWeight={900} textAnchor="middle">DETECTA LA LATA ✓</text>}
      </svg>
      <Tarjeta lt={lt} nombre="RETRO" sub="un solo cuerpo + reflector" color={MAG}
        stats={[['Alcance', 65], ['Margen de ganancia', 40], ['Brillantes (polarizado)', 85], ['Transparentes', 25], ['Facilidad de montaje', 75]]} />
    </Escena>
  );
};

const Difuso = ({t, lt, d}) => {
  const fase2 = lt > 8.0;
  const yObj = fase2 ? YT + 110 : YB - 90;
  const xo = lerp(-180, 1260, clamp(((fase2 ? lt - 8.0 : lt - 1.5)) / 6.0));
  const cerca = Math.abs(xo - CX) < 80;
  const det = cerca;
  return (
    <Escena lt={lt} d={d}>
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        <Banda t={t} />
        <polygon points={`${CX - 40},${YT - 30} ${CX + 40},${YT - 30} ${CX + 160},${YB - 10} ${CX - 160},${YB - 10}`} fill={AM} opacity={0.12} />
        <polygon points={`${CX - 40},${YT - 30} ${CX + 40},${YT - 30} ${CX + 110},${fase2 ? YT + 200 : YB - 10} ${CX - 110},${fase2 ? YT + 200 : YB - 10}`} fill={AM} opacity={0.22} />
        {fase2 ? <Negro x={xo} y={yObj} /> : <Caja x={xo} y={yObj} s={0.9} color="#F2F4F7" />}
        {det && [...Array(6)].map((_, i) => <line key={i} x1={xo - 50 + i * 20} y1={yObj - 70} x2={CX + 26} y2={YT - 30} stroke={AM} strokeWidth={3} opacity={fase2 ? 0.35 : 0.8} />)}
        <SensorTop x={CX} y={YT - 36} dir={1} tipo="difuso" out={det} />
        <text x={CX} y={YB + 90} fill={AM} fontSize={40} fontWeight={900} textAnchor="middle" opacity={ein(lt, 4.0)}>basta un 2 % de la luz emitida</text>
        {fase2 && <text x={CX} y={YB + 150} fill="#FFFFFF" fontSize={36} fontWeight={900} textAnchor="middle" opacity={ein(lt, 9.0)}>negro mate: solo de cerca</text>}
      </svg>
      <Tarjeta lt={lt} nombre="DIFUSO" sub="sin reflector" color={AM}
        stats={[['Alcance', 30], ['Depende del color', 90], ['Margen de ganancia', 55], ['Costo bajo', 85], ['Facilidad de montaje', 95]]} />
    </Escena>
  );
};

const Fondo = ({lt, d}) => {
  const ang = (dist) => Math.atan2(dist, 120);
  const dObj = 260;
  return (
    <Escena lt={lt} d={d}>
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        <g transform="translate(0,40)">
          <rect x={0} y={1060} width={1080} height={40} fill="#C9CED6" />
          <text x={540} y={1150} fill="#C9CED6" fontSize={30} fontWeight={900} textAnchor="middle">FONDO BRILLANTE (se ignora)</text>
          <SensorTop x={420} y={560} dir={1} tipo="difuso" out={lt > 3} />
          <line x1={400} y1={560} x2={400} y2={560 + dObj} stroke={AM} strokeWidth={8} />
          <line x1={400} y1={560 + dObj} x2={446} y2={560} stroke={VE} strokeWidth={6} />
          <line x1={400} y1={560} x2={400} y2={1060} stroke={AM} strokeWidth={3} strokeDasharray="10 10" opacity={0.5} />
          <line x1={400} y1={1060} x2={446} y2={560} stroke="#5B6472" strokeWidth={4} strokeDasharray="12 10" />
          <Caja x={400} y={560 + dObj + 60} s={0.55} color="#F2F4F7" />
          <line x1={150} x2={930} y1={900} y2={900} stroke={RO} strokeWidth={6} strokeDasharray="24 14" />
          <text x={930} y={885} fill={RO} fontSize={32} fontWeight={900} textAnchor="end">límite ajustado</text>
          <text x={700} y={760} fill={VE} fontSize={34} fontWeight={900} opacity={ein(lt, 2)}>triangulación:</text>
          <text x={700} y={805} fill={VE} fontSize={30} fontWeight={800} opacity={ein(lt, 2)}>el ángulo de regreso</text>
          <text x={700} y={845} fill={VE} fontSize={30} fontWeight={800} opacity={ein(lt, 2)}>indica la distancia</text>
        </g>
      </svg>
      <div style={{position: 'absolute', left: 60, right: 60, top: 1260, opacity: ein(lt, 5.5), background: 'rgba(20,16,40,0.92)', border: `4px solid ${VE}`, borderRadius: 28, padding: '24px 34px'}}>
        <div style={{color: VE, fontWeight: 900, fontSize: 50}}>+ ignora el fondo</div>
        <div style={{color: RO, fontWeight: 900, fontSize: 46, marginTop: 8}}>− menos alcance</div>
      </div>
    </Escena>
  );
};

const Gana = ({lt, d}) => {
  const filas = [['Polvo y mucha distancia', 'BARRERA', CY, 0.6], ['Un solo lado + objetos brillantes', 'RETRO POLARIZADO', MAG, 4.4], ['Objeto cerca, sin espacio para reflector', 'DIFUSO + SUPRESIÓN DE FONDO', AM, 8.0]];
  return (
    <Escena lt={lt} d={d}>
      {filas.map(([esc, gan, col, a], i) => (
        <div key={i} style={{position: 'absolute', left: 60, right: 60, top: 480 + i * 360, opacity: ein(lt, a), transform: `translateX(${(1 - ein(lt, a)) * -80}px)`,
          background: 'rgba(20,16,40,0.92)', border: `4px solid ${col}`, borderRadius: 28, padding: '26px 34px'}}>
          <div style={{color: '#C9C2E8', fontWeight: 800, fontSize: 34}}>ESCENARIO {i + 1}</div>
          <div style={{color: '#FFFFFF', fontWeight: 900, fontSize: 44, marginTop: 4}}>{esc}</div>
          <div style={{color: col, fontWeight: 900, fontSize: 52, marginTop: 10, textShadow: `0 0 18px ${col}`, opacity: ein(lt, a + 1.2), transform: `scale(${lerp(1.3, 1, ein(lt, a + 1.2))})`, transformOrigin: 'left'}}>🏆 {gan}</div>
        </div>
      ))}
    </Escena>
  );
};

const LightDark = ({lt, d}) => {
  const W = 840, x0 = 160, ys = [620, 860, 1100];
  const pres = (u) => (u > 0.3 && u < 0.6);
  const path = (fn, y) => {
    let s = `M${x0},${y}`; const n = 200;
    for (let i = 0; i <= n; i++) { const u = i / n; const v = fn(u) ? -110 : 0; s += ` L${x0 + u * W},${y + v}`; }
    return s;
  };
  const prog = clamp((lt - 1.0) / 6.0);
  return (
    <Escena lt={lt} d={d}>
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        <defs><clipPath id="cp"><rect x={0} y={0} width={x0 + prog * W + 4} height={1920} /></clipPath></defs>
        {[['objeto en el haz', '#FFFFFF', (u) => pres(u)], ['LIGHT ON', VE, (u) => !pres(u)], ['DARK ON', AM, (u) => pres(u)]].map(([lab, col, fn], i) => (
          <g key={i} opacity={ein(lt, 0.3 + i * 0.4)}>
            <text x={60} y={ys[i] - 140} fill={col} fontSize={38} fontWeight={900}>{lab}</text>
            <line x1={x0} x2={x0 + W} y1={ys[i]} y2={ys[i]} stroke="#3A3550" strokeWidth={3} />
            <path d={path(fn, ys[i])} stroke={col} strokeWidth={8} fill="none" clipPath="url(#cp)" />
          </g>
        ))}
        <text x={60} y={ys[1] + 60} fill={VE} fontSize={30} fontWeight={800} opacity={ein(lt, 3)}>salida activa cuando RECIBE luz</text>
        <text x={60} y={ys[2] + 60} fill={AM} fontSize={30} fontWeight={800} opacity={ein(lt, 6)}>salida activa cuando DEJA de recibirla</text>
      </svg>
      <div style={{position: 'absolute', left: 60, right: 60, top: 1290, opacity: ein(lt, 9.5), background: 'rgba(20,16,40,0.92)', border: `4px solid ${AM}`, borderRadius: 28, padding: '24px 34px'}}>
        <div style={{color: '#FFFFFF', fontWeight: 900, fontSize: 40}}>Barrera y retro:</div>
        <div style={{color: AM, fontWeight: 900, fontSize: 50}}>usa DARK ON para que la salida se active con el objeto</div>
      </div>
    </Escena>
  );
};
