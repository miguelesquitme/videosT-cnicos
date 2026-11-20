// Reel R5 · ¿QUÉ ES UN RELÉ? Y POR QUÉ NO ES UN CONTACTOR.  Diseño "plano técnico" (fondo azul de plano).
import React from 'react';
import {AbsoluteFill} from 'remotion';
import {useT, ein, eout, clamp, lerp, ease, loc, vis, Voces, Sfx, Tornillo, Cierre} from './lib';

const BP = '#0A3A7E', LN = '#5C8FD6', BL = '#FFFFFF', AM = '#FFD60A', RO = '#FF6B6B', VE = '#7CFFB2', CY = '#7FE7FF';

const Plano = ({t}) => (
  <svg width={1080} height={1920} style={{position: 'absolute'}}>
    {[...Array(55)].map((_, i) => <line key={'h' + i} x1={0} x2={1080} y1={i * 36} y2={i * 36} stroke={LN} strokeWidth={i % 5 ? 0.8 : 1.8} opacity={0.35} />)}
    {[...Array(31)].map((_, i) => <line key={'v' + i} x1={i * 36} x2={i * 36} y1={0} y2={1920} stroke={LN} strokeWidth={i % 5 ? 0.8 : 1.8} opacity={0.35} />)}
    <rect x={24} y={24} width={1032} height={1872} fill="none" stroke={BL} strokeWidth={4} opacity={0.6} />
  </svg>
);

// ---------------------------------------------------------------- relé de interfaz enchufable (vista frontal, tapa transparente)
const Rele = ({x, y, s = 1, on = 0, led = false, diodo = true}) => {
  // on: 0..1 posición de la armadura / contacto
  const ang = lerp(0, -9, on);
  const cx = lerp(0, 1, on);
  return (
    <g transform={`translate(${x},${y}) scale(${s})`}>
      {/* riel DIN */}
      <rect x={-170} y={-18} width={340} height={36} fill="#9AA3AF" /><rect x={-170} y={-10} width={340} height={20} fill="#C9CED6" />
      {/* base */}
      <rect x={-110} y={-250} width={220} height={500} rx={14} fill="#3A414C" stroke="#11151A" strokeWidth={4} />
      {/* bornes superiores 11 12 14 */}
      {[['12', -62], ['11', 0], ['14', 62]].map(([n, dx]) => <g key={n}><rect x={dx - 26} y={-240} width={52} height={56} rx={6} fill="#C9CED6" stroke="#475467" strokeWidth={2} /><Tornillo x={dx} y={-212} r={15} />
        <text x={dx} y={-162} fontSize={22} fontWeight={900} fill={BL} textAnchor="middle">{n}</text></g>)}
      {/* bornes inferiores A1 A2 */}
      {[['A1', -40], ['A2', 40]].map(([n, dx]) => <g key={n}><rect x={dx - 26} y={184} width={52} height={56} rx={6} fill="#C9CED6" stroke="#475467" strokeWidth={2} /><Tornillo x={dx} y={212} r={15} />
        <text x={dx} y={176} fontSize={22} fontWeight={900} fill={n === 'A1' ? RO : CY} textAnchor="middle">{n === 'A1' ? 'A1 +' : 'A2 −'}</text></g>)}
      {/* LED y diodo en la base */}
      <circle cx={-78} cy={140} r={10} fill={led ? '#3DFF8F' : '#1E4D2E'} />
      {led && <circle cx={-78} cy={140} r={22} fill="#3DFF8F" opacity={0.35} />}
      <text x={-78} y={120} fontSize={14} fontWeight={800} fill={BL} textAnchor="middle">LED</text>
      {diodo && <g><rect x={50} y={128} width={44} height={20} rx={8} fill="#101828" /><rect x={84} y={128} width={6} height={20} fill="#C9CED6" /><text x={72} y={120} fontSize={14} fontWeight={800} fill={BL} textAnchor="middle">diodo</text></g>}
      {/* relé enchufable con tapa transparente */}
      <rect x={-92} y={-140} width={184} height={250} rx={10} fill="#BFE9FF" opacity={0.16} stroke="#E4F6FF" strokeWidth={3} />
      {/* bobina con núcleo */}
      <rect x={-70} y={-30} width={70} height={110} rx={8} fill="#B5651D" stroke="#7A3B12" strokeWidth={3} />
      {[...Array(9)].map((_, i) => <line key={i} x1={-68} x2={-2} y1={-22 + i * 12} y2={-22 + i * 12} stroke="#7A3B12" strokeWidth={2} />)}
      <rect x={-46} y={-44} width={22} height={18} fill="#8A929C" />
      {/* armadura (pivota en el yugo) */}
      <g transform={`rotate(${ang}, 10, -56)`}>
        <rect x={-62} y={-62} width={78} height={12} rx={3} fill="#98A2B3" stroke="#475467" strokeWidth={2} />
        <line x1={10} y1={-56} x2={30} y2={-90} stroke="#98A2B3" strokeWidth={6} />
      </g>
      <rect x={10} y={-56} width={10} height={140} fill="#8A929C" />
      {/* resorte */}
      <path d="M-58 -62 l6 -10 l6 10 l6 -10 l6 10 l6 -10" stroke="#E4E7EC" strokeWidth={3} fill="none" transform="translate(0,-8)" />
      {/* contactos: fijo NC (12), fijo NA (14), lámina móvil (11) */}
      <rect x={30} y={-128} width={50} height={10} fill="#C8743F" />
      <rect x={30} y={-78} width={50} height={10} fill="#C8743F" />
      <text x={86} y={-118} fontSize={16} fontWeight={900} fill={BL}>12 NC</text>
      <text x={86} y={-66} fontSize={16} fontWeight={900} fill={BL}>14 NA</text>
      <line x1={36} y1={lerp(-112, -84, cx)} x2={78} y2={lerp(-112, -84, cx)} stroke="#E0A86E" strokeWidth={8} strokeLinecap="round" />
      <line x1={36} y1={lerp(-112, -84, cx)} x2={30} y2={-90} stroke="#98A2B3" strokeWidth={4} />
      <circle cx={70} cy={lerp(-112, -84, cx) + (cx < 0.5 ? -6 : 6)} r={6} fill="#D9DDE3" />
      <rect x={-88} y={88} width={176} height={18} fill="#F2F4F7" />
      <text x={0} y={102} fontSize={13} fontWeight={900} fill="#101828" textAnchor="middle">24 V DC · 1 C/O · 250 V~</text>
    </g>
  );
};

const Plc = ({x, y, s = 1, q = false}) => (
  <g transform={`translate(${x},${y}) scale(${s})`}>
    <rect x={-150} y={-150} width={300} height={300} rx={12} fill="#D0D5DD" stroke="#475467" strokeWidth={4} />
    <rect x={-130} y={-130} width={260} height={46} rx={6} fill="#344054" />
    {[...Array(8)].map((_, i) => <circle key={i} cx={-110 + i * 31} cy={-107} r={8} fill={i === 0 && q ? '#3DFF8F' : '#1E4D2E'} />)}
    <text x={0} y={-56} fontSize={18} fontWeight={900} fill="#101828" textAnchor="middle">SALIDAS 24 V DC · 0,5 A</text>
    {[...Array(8)].map((_, i) => <g key={i}><rect x={-128 + i * 32} y={-40} width={28} height={40} rx={3} fill="#4E8A57" /><Tornillo x={-114 + i * 32} y={-26} r={8} /><text x={-114 + i * 32} y={18} fontSize={11} fontWeight={800} fill="#101828" textAnchor="middle">{`Q${i}`}</text></g>)}
    <text x={0} y={80} fontSize={44} fontWeight={900} fill="#475467" textAnchor="middle">PLC</text>
    <circle cx={-110} cy={120} r={9} fill="#3DFF8F" /><text x={-92} y={126} fontSize={16} fontWeight={800} fill="#344054">RUN</text>
  </g>
);

const Valvula = ({x, y, s = 1, on = false}) => (
  <g transform={`translate(${x},${y}) scale(${s})`}>
    <rect x={-160} y={60} width={320} height={50} fill="#9AA3AF" stroke="#475467" strokeWidth={3} />
    <rect x={-70} y={30} width={140} height={110} rx={10} fill="#C9A227" stroke="#7A5A10" strokeWidth={3} />
    <rect x={-50} y={-120} width={100} height={150} rx={10} fill="#1F2430" stroke="#000" strokeWidth={3} />
    <rect x={-40} y={-170} width={80} height={56} rx={6} fill="#2B3038" />
    <text x={0} y={-40} fontSize={18} fontWeight={900} fill={on ? AM : '#AEB6C2'} textAnchor="middle">230 V~</text>
    <text x={0} y={-16} fontSize={14} fontWeight={800} fill="#AEB6C2" textAnchor="middle">bobina</text>
    {on && <rect x={-50} y={-120} width={100} height={150} rx={10} fill="none" stroke={AM} strokeWidth={6} />}
    <text x={0} y={185} fontSize={24} fontWeight={900} fill={BL} textAnchor="middle">ELECTROVÁLVULA</text>
  </g>
);

const Contactor = ({x, y, s = 1, on = false}) => (
  <g transform={`translate(${x},${y}) scale(${s})`}>
    <rect x={-90} y={-130} width={180} height={260} rx={12} fill="#C9CED6" stroke="#475467" strokeWidth={4} />
    {[-54, 0, 54].map((dx, i) => <g key={i}><Tornillo x={dx} y={-104} r={13} /><Tornillo x={dx} y={104} r={13} />
      {[...Array(4)].map((_, j) => <rect key={j} x={dx - 18} y={-74 + j * 9} width={36} height={5} fill="#475467" />)}</g>)}
    <rect x={-50} y={-30} width={100} height={64} rx={6} fill="#98A2B3" />
    <rect x={-26} y={-20} width={52} height={26} rx={3} fill={on ? '#12924F' : '#344054'} />
    <text x={0} y={-2} fontSize={14} fontWeight={900} fill="white" textAnchor="middle">{on ? 'I' : 'O'}</text>
    <text x={0} y={24} fontSize={16} fontWeight={900} fill="#101828" textAnchor="middle">AC-3</text>
    {on && <rect x={-90} y={-130} width={180} height={260} rx={12} fill="none" stroke={VE} strokeWidth={6} />}
  </g>
);

const Motor = ({x, y, s = 1, on = false, t = 0}) => (
  <g transform={`translate(${x},${y}) scale(${s})`}>
    <rect x={-110} y={-60} width={190} height={120} rx={12} fill="#3E6A8C" stroke="#1F3A50" strokeWidth={3} />
    {[...Array(7)].map((_, i) => <line key={i} x1={-100} x2={70} y1={-46 + i * 15} y2={-46 + i * 15} stroke="#2B5070" strokeWidth={4} />)}
    <rect x={-160} y={-54} width={54} height={108} rx={16} fill="#34556F" />
    <rect x={80} y={-12} width={60} height={24} fill="#C9CED6" />
    <rect x={100} y={-12 + (on ? 9 * (1 + Math.sin(t * 25)) : 0)} width={24} height={6} fill="#5B6472" />
  </g>
);

const Escena = ({lt, d, children}) => <AbsoluteFill style={{opacity: Math.min(ein(lt, 0, 0.35), eout(lt, d + 0.05, 0.3))}}>{children}</AbsoluteFill>;
const Nota = ({top, color, o = 1, children, size = 40}) => (
  <div style={{position: 'absolute', top, left: 60, right: 60, opacity: o, background: 'rgba(5,30,70,0.92)', border: `3px solid ${color}`, borderRadius: 16, padding: '16px 26px', color: BL, fontWeight: 900, fontSize: size}}>{children}</div>
);
const Cota = ({x1, y1, x2, y2, txt, color = BL}) => (
  <g><line x1={x1} y1={y1} x2={x2} y2={y2} stroke={color} strokeWidth={3} /><circle cx={x2} cy={y2} r={7} fill={color} />
    <text x={x1} y={y1 - 10} fontSize={30} fontWeight={900} fill={color} textAnchor="middle">{txt}</text></g>
);

export const R5 = (props) => {
  const t = useT();
  const S = Object.fromEntries(props.sec.map((s) => [s.k, s]));
  return (
    <AbsoluteFill style={{fontFamily: 'Montserrat', background: BP}}>
      <Plano t={t} />
      <Voces props={props} />
      {props.sec.slice(1).map((s) => <Sfx key={s.k} at={s.ini - 0.25} name="whoosh" vol={0.22} />)}
      {/* cajetín de título tipo plano */}
      <div style={{position: 'absolute', top: 80, left: 60, right: 60, height: 250, border: `4px solid ${BL}`, background: 'rgba(5,30,70,0.85)'}}>
        <div style={{position: 'absolute', top: 22, left: 30, color: BL, fontWeight: 900, fontSize: 76}}>{props.tit1}</div>
        <div style={{position: 'absolute', top: 118, left: 30, right: 20, color: AM, fontWeight: 900, fontSize: 46, whiteSpace: 'nowrap'}}>{props.tit2}</div>
        <div style={{position: 'absolute', top: 196, left: 30, color: LN, fontWeight: 800, fontSize: 24}}>PLANO E-01 · CONTROL · ESC. 1:1</div>
      </div>
      {vis(t, S.gancho) && <Gancho lt={loc(t, S.gancho)} d={S.gancho.dur} />}
      {vis(t, S.p1) && <P1 lt={loc(t, S.p1)} d={S.p1.dur} />}
      {vis(t, S.p2) && <P2 lt={loc(t, S.p2)} d={S.p2.dur} />}
      {vis(t, S.p3) && <P3 lt={loc(t, S.p3)} d={S.p3.dur} />}
      {vis(t, S.p3b) && <P3b lt={loc(t, S.p3b)} d={S.p3b.dur} />}
      {vis(t, S.p4) && <P4 lt={loc(t, S.p4)} d={S.p4.dur} t={t} />}
      {t >= S.cierre.ini - 0.2 && <Cierre t={t} ini={S.cierre.ini} color={AM} texto="Relé: señales · Contactor: potencia" fondo="rgba(5,30,70,0.96)" />}
      <Sfx at={S.p1.ini + 5.0} name="tic" vol={0.5} />
    </AbsoluteFill>
  );
};

const Gancho = ({lt, d}) => (
  <Escena lt={lt} d={d}>
    <svg width={1080} height={1920} style={{position: 'absolute'}}>
      <Plc x={290} y={640} s={1.1} q={lt > 1} />
      <Valvula x={800} y={700} s={1.0} />
      <line x1={420} y1={640} x2={720} y2={640} stroke={RO} strokeWidth={6} strokeDasharray="18 12" opacity={ein(lt, 3)} />
      {lt > 3.5 && <g opacity={ein(lt, 3.5)}><line x1={530} y1={560} x2={610} y2={720} stroke={RO} strokeWidth={12} /><line x1={610} y1={560} x2={530} y2={720} stroke={RO} strokeWidth={12} /></g>}
    </svg>
    <Nota top={980} color={CY} o={ein(lt, 0.8)}>Salida del PLC: 24 V DC · ~0,5 A</Nota>
    <Nota top={1110} color={RO} o={ein(lt, 3.5)}>Electroválvula: bobina de 230 V~</Nota>
    <Nota top={1260} color={AM} o={ein(lt, 7.0)} size={60}>→ para eso existe el RELÉ</Nota>
  </Escena>
);

const P1 = ({lt, d}) => {
  const on = ease((lt - 5.0) / 0.25);
  return (
    <Escena lt={lt} d={d}>
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        <Rele x={540} y={900} s={1.55} on={on} led={lt > 5} />
        {lt > 5 && [...Array(3)].map((_, i) => <ellipse key={i} cx={540 - 54} cy={900 + 38} rx={80 + i * 26} ry={120 + i * 26} fill="none" stroke={AM} strokeWidth={3} opacity={0.5 - i * 0.12} />)}
        <g opacity={ein(lt, 1.0)}><Cota x1={220} y1={1250} x2={430} y2={1185} txt="bobina" color={AM} /></g>
        <g opacity={ein(lt, 4.5)}><Cota x1={870} y1={700} x2={680} y2={790} txt="armadura" color={CY} /></g>
        <g opacity={ein(lt, 8.0)}><Cota x1={840} y1={480} x2={660} y2={725} txt="contacto conmutado" color={VE} /></g>
      </svg>
      <Nota top={1450} color={VE} o={ein(lt, 11.5)} size={38}>11 común · 12 normalmente cerrado · 14 normalmente abierto</Nota>
    </Escena>
  );
};

const P2 = ({lt, d}) => {
  const k = ease((lt - 9.0) / 0.3);
  const pico = (u) => (u < 0.4 ? 1 : u < 0.42 ? -8 * (1 - k * 0.9) : -8 * (1 - k * 0.9) * Math.exp(-(u - 0.42) * 30));
  const x0 = 140, W = 800, y0 = 1430;
  let dd = '';
  for (let i = 0; i <= 200; i++) { const u = i / 200; dd += `${i ? 'L' : 'M'}${x0 + u * W},${y0 - pico(u) * 22}`; }
  return (
    <Escena lt={lt} d={d}>
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        <rect x={60} y={380} width={460} height={760} fill={CY} opacity={0.08} />
        <rect x={560} y={380} width={460} height={760} fill={RO} opacity={0.08} />
        <line x1={540} x2={540} y1={380} y2={1140} stroke={BL} strokeWidth={4} strokeDasharray="20 14" />
        <text x={290} y={430} fontSize={36} fontWeight={900} fill={CY} textAnchor="middle">CONTROL 24 V DC</text>
        <text x={790} y={430} fontSize={36} fontWeight={900} fill={RO} textAnchor="middle">CARGA 230 V~</text>
        <Rele x={540} y={780} s={1.15} on={1} led />
        <text x={540} y={1180} fontSize={32} fontWeight={900} fill={BL} textAnchor="middle" opacity={ein(lt, 2)}>aislamiento galvánico</text>
        <g opacity={ein(lt, 7.5)}>
          <rect x={80} y={1240} width={920} height={300} rx={16} fill="rgba(5,30,70,0.92)" stroke={AM} strokeWidth={3} />
          <line x1={x0} x2={x0 + W} y1={y0} y2={y0} stroke={LN} strokeWidth={2} />
          <path d={dd} stroke={k > 0.5 ? VE : RO} strokeWidth={6} fill="none" />
          <text x={x0} y={1280} fontSize={28} fontWeight={900} fill={AM}>voltaje en la bobina al desenergizar</text>
          <text x={x0 + W} y={1520} fontSize={28} fontWeight={900} fill={k > 0.5 ? VE : RO} textAnchor="end">{k > 0.5 ? 'con diodo: pico absorbido' : 'sin diodo: pico inductivo'}</text>
        </g>
      </svg>
    </Escena>
  );
};

const P3 = ({lt, d}) => {
  const filas = [['Corriente de contactos', 'hasta ~10 A', 'polos de potencia'], ['Cámaras apagachispas', 'no', 'sí'], ['Categoría', 'AC-15 · DC-13', 'AC-3 (motores)'], ['Auxiliares', 'no', 'sí']];
  return (
    <Escena lt={lt} d={d}>
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        <Rele x={290} y={700} s={0.95} on={0} />
        <Contactor x={790} y={690} s={1.25} />
        <text x={290} y={1000} fontSize={42} fontWeight={900} fill={AM} textAnchor="middle">RELÉ</text>
        <text x={790} y={1000} fontSize={42} fontWeight={900} fill={VE} textAnchor="middle">CONTACTOR</text>
      </svg>
      {filas.map(([a, b, c], i) => (
        <div key={a} style={{position: 'absolute', top: 1040 + i * 120, left: 60, right: 60, opacity: ein(lt, [5, 8, 11, 17][i]), display: 'flex', alignItems: 'center',
          background: 'rgba(5,30,70,0.92)', border: `2px solid ${LN}`, borderRadius: 12, padding: '10px 18px'}}>
          <div style={{width: 340, color: BL, fontWeight: 800, fontSize: 28}}>{a}</div>
          <div style={{width: 280, color: AM, fontWeight: 900, fontSize: 32, textAlign: 'center'}}>{b}</div>
          <div style={{flex: 1, color: VE, fontWeight: 900, fontSize: 32, textAlign: 'center'}}>{c}</div>
        </div>
      ))}
      <div style={{position: 'absolute', top: 1540, left: 60, right: 60, color: LN, fontWeight: 800, fontSize: 24, opacity: ein(lt, 12)}}>IEC 60947-5-1 (dispositivos de control) · IEC 60947-4-1 (contactores)</div>
    </Escena>
  );
};

const P3b = ({lt, d}) => {
  const inv = lt > 7.0;
  return (
    <Escena lt={lt} d={d}>
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        <Rele x={540} y={820} s={1.2} on={inv ? 0 : 1} led={!inv} />
        <text x={540} y={1180} fontSize={40} fontWeight={900} fill={inv ? RO : VE} textAnchor="middle">{inv ? 'A1 − / A2 +  (invertida)' : 'A1 + / A2 −  (correcta)'}</text>
        {inv && <g opacity={ein(lt, 7.5)}>
          <path d="M 590 980 C 700 1000, 700 900, 640 900" stroke={RO} strokeWidth={10} fill="none" />
          <circle cx={652} cy={980} r={70} fill="none" stroke={RO} strokeWidth={8} />
        </g>}
      </svg>
      <Nota top={1260} color={inv ? RO : VE} o={ein(lt, 0.5)} size={38}>{inv ? 'el diodo conduce: CORTO en la salida del PLC' : 'módulo con diodo: respeta la polaridad'}</Nota>
    </Escena>
  );
};

const P4 = ({lt, d, t}) => {
  const a1 = lt > 7.0, a2 = lt > 9.0, a3 = lt > 11.0;
  return (
    <Escena lt={lt} d={d}>
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        <Plc x={250} y={560} s={0.75} q={a1} />
        <Rele x={250} y={1040} s={0.75} on={a1 ? 1 : 0} led={a1} />
        <Contactor x={780} y={600} s={1.0} on={a2} />
        <Motor x={780} y={1060} s={1.2} on={a3} t={t} />
        <path d="M 360 560 L 420 560 L 420 900 L 250 900" stroke={a1 ? CY : LN} strokeWidth={8} fill="none" />
        <path d="M 330 860 L 600 860 L 600 600 L 690 600" stroke={a2 ? AM : LN} strokeWidth={8} fill="none" />
        <path d="M 780 730 L 780 960" stroke={a3 ? RO : LN} strokeWidth={10} fill="none" />
        <text x={250} y={400} fontSize={30} fontWeight={900} fill={CY} textAnchor="middle">1 · PLC</text>
        <text x={250} y={1275} fontSize={30} fontWeight={900} fill={AM} textAnchor="middle">2 · RELÉ (señal)</text>
        <text x={780} y={440} fontSize={30} fontWeight={900} fill={VE} textAnchor="middle">3 · CONTACTOR (potencia)</text>
        <text x={780} y={1180} fontSize={30} fontWeight={900} fill={RO} textAnchor="middle">4 · MOTOR</text>
      </svg>
      <Nota top={1330} color={AM} o={ein(lt, 0.4)} size={40}>Relé: señales y bobinas · Contactor: la potencia</Nota>
    </Escena>
  );
};
