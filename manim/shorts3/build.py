"""Shorts 3.0 (26-nov): gancho nuevo de ~3 s delante del cuerpo 2.0 + duración variable (quitar o no el p6).
Gancho = voz clonada nueva + el gancho visual 2.0 acelerado con la frase grande sobre la cabecera (sin título
estático en el segundo 0). Después sigue el cuerpo original. Tiempos de cada sección: LOG_VOZ (manim --dry_run).
Uso: python3 shorts3/build.py [claves...]"""
import os, sys, json, subprocess, re
os.environ.setdefault("FORMATO", "v")
os.environ.setdefault("VOZ", "eleven")
os.environ.setdefault("MARCA", "4")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import comun_e  # noqa: F401  (voz clonada primero)
from comun_e import audio, SUFIJO_VOZ
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

M = Path(__file__).resolve().parent.parent
AQ = M / "shorts3"
TMP = Path("/tmp/claude-0/r3")
OUT = Path("/mnt/attach/outputs/shorts_3.0")
FONT = "/usr/share/fonts/opentype/montserrat/Montserrat-Black.otf"
AT = Path("/mnt/attach/outputs")

# clave: (carpeta, salida, voz, pantalla (palabra en amarillo entre *), objetivo s)
S = {
 "f01": ("05", "F01_quien_enciende_las_luces_de_la_calle", "Nadie enciende esta lámpara. Se enciende sola.", "Nadie la enciende. *Se enciende sola.*", 65),
 "v22v2": ("05", "V22_toque_estatica_o_fuga_que_mata", "Este toque no hace nada. El otro mata.", "Este toque no hace nada. *El otro mata.*", 100),
 "v23v2": ("05", "V23_cambiar_2_cables_invierte_el_giro", "Cruzas dos cables y el motor cambia de giro.", "Cruzas 2 cables… *y cambia de giro.*", 75),
 "v24v2": ("05", "V24_por_que_zumban_las_lineas", "¿Escuchas ese zumbido? No es tu imaginación.", "¿Escuchas ese zumbido? *No es tu imaginación.*", 72),
 "v25v2": ("05", "V25_un_fusible_se_derrite_a_proposito", "Este metal se derrite a propósito.", "Este metal se derrite *a propósito.*", 85),
 "v26v2": ("05", "V26_mismo_trabajo_mas_corriente", "Mismo trabajo… y este pide más corriente.", "Mismo trabajo… *y este pide más corriente.*", 110),
 "v28v2": ("05", "V28_120V_en_240V_esto_pasa", "Doble voltaje, cuatro veces la potencia.", "Doble voltaje = *4 veces la potencia*", 68),
 "v29v2": ("05", "V29_se_bajan_las_luces_cuando_arranca", "Arranca la refri… y bajan las luces.", "Arranca la refri… *y bajan las luces.*", 90),
 "v30v2": ("05", "V30_que_te_cobran_en_el_recibo", "Tu recibo no te cobra vatios.", "Tu recibo *no te cobra vatios.*", 62),
 "v32v2": ("05", "V32_6_bornes_3_fases_estrella_o_triangulo", "Tres fases… pero seis bornes. ¿Por qué?", "3 fases… *pero 6 bornes.*", 88),
 "v33v2": ("05", "V33_IP65_o_IP67_cual_aguanta_agua", "Esta caja aguanta chorros. Esta no.", "Esta aguanta chorros. *Esta no.*", 70),
 "a01": ("06", "A01_el_motor_sigue_si_sueltas_el_boton", "Suelto el botón… y el motor no se apaga.", "Suelto el botón… *y no se apaga.*", 72),
 "a02": ("06", "A02_motor_26A_breaker_80A_esta_mal", "Motor de veintiséis punto cinco amperios. Breaker de ochenta.", "Motor de 26,5 A. *Breaker de 80 A.*", 98),
 "a03": ("06", "A03_el_rele_termico_mide_con_calor", "Este relé mide la corriente con calor.", "Mide la corriente… *con calor.*", 80),
 "a04": ("06", "A04_contactor_32A_no_alcanza", "Contactor de treinta y dos amperios… y no alcanza.", "Contactor de 32 A… *y no alcanza.*", 90),
 "a05": ("06", "A05_prueba_de_2_minutos_antes_de_energizar", "Esta prueba de dos minutos salva tu breaker.", "2 minutos que *salvan tu breaker.*", 85),
 "a06": ("06", "A06_la_pinza_marca_cero", "El motor trabaja… y la pinza marca cero.", "El motor trabaja… *y la pinza marca 0.*", 65),
 "a07": ("06", "A07_motor_de_9_puntas_a_208V", "Nueve cables… y solo tres fases.", "9 cables… *y solo 3 fases.*", 108),
 "a08": ("06", "A08_inversion_de_giro_dos_contactores", "Un botón adelante. Otro, atrás.", "Un botón adelante. *Otro, atrás.*", 90),
 "a09": ("06", "A09_lo_que_evita_el_cortocircuito", "Si cierran los dos: cortocircuito.", "Si cierran los dos: *cortocircuito.*", 76),
 "a10": ("06", "A10_cuanto_tiempo_en_estrella_triangulo", "Mal ajustado, este dial castiga al motor.", "Mal ajustado, *castiga al motor.*", 95),
 "a11": ("06", "A11_para_que_sirve_la_puntera", "Sin este tubito, el cable se afloja.", "Sin este tubito, *el cable se afloja.*", 60),
 "a12": ("06", "A12_por_que_los_cables_tienen_colores", "Negro, rojo, azul: no es gusto.", "Negro, rojo, azul: *no es gusto.*", 70),
 "a13": ("06", "A13_una_bobina_pequena_mueve_38A", "Una bobina pequeña mueve treinta y ocho amperios.", "Una bobina pequeña *mueve 38 A.*", 84),
 "a14": ("06", "A14_guardamotor_o_breaker_mas_termico", "Dos aparatos… en uno solo.", "Dos aparatos… *en uno solo.*", 102),
 "a15": ("06", "A15_que_significan_13_14_y_21_22", "Lee estos números y sabes qué contacto es.", "Lee estos números… *y sabes qué contacto es.*", 68),
}


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True).stdout)


def cuerpo(k):
    d = "f01_fotocelda" if k == "f01" else k
    for p in (M / f"media/videos/{d}/1920p30/cuerpo_{k}.mp4", M / f"media/videos/reels_arr/1920p30/cuerpo_{k}.mp4"):
        if p.exists():
            return p
    raise FileNotFoundError(k)


def tiempos(k):
    f = TMP / (f"vt_{k}.jsonl" if k[0] in "fv" else f"voz_{k}.jsonl")
    return {c: t for _, c, t in (json.loads(x) for x in open(f))}


def portada(k):
    if k[0] == "a":
        return next((AT / "reels_arranques").glob(f"V*_{k.upper()}_*_portada.png"))
    return AT / (f"{k[:3].upper()}v2_portada.png" if k != "f01" else "F01_portada.png")


def placa(texto, ruta):
    """Banda de 1080×430 que tapa la cabecera: frase grande, la parte entre * en amarillo."""
    W, H = 1080, 430
    im = Image.new("RGBA", (W, H), (7, 10, 16, 255))
    d = ImageDraw.Draw(im)
    partes = re.split(r"(\*[^*]+\*)", texto)
    tokens = []
    for p in partes:
        col = (255, 212, 0) if p.startswith("*") else (255, 255, 255)
        for w in p.strip("*").split():
            tokens.append((w, col))
    for size in range(96, 40, -4):
        f = ImageFont.truetype(FONT, size)
        lines, cur, wcur = [], [], 0
        for w, c in tokens:
            ww = d.textlength(w + " ", font=f)
            if wcur + ww > W - 90 and cur:
                lines.append(cur); cur, wcur = [], 0
            cur.append((w, c, ww)); wcur += ww
        lines.append(cur)
        if len(lines) <= 3 and len(lines) * size * 1.15 < H - 70:
            break
    y = (H - len(lines) * size * 1.15) / 2 + 10
    for ln in lines:
        x = (W - sum(t[2] for t in ln)) / 2
        for w, c, ww in ln:
            d.text((x, y), w, font=f, fill=c)
            x += ww
        y += size * 1.15
    d.rectangle((0, H - 8, W, H), fill=(0, 200, 230, 255))
    im.save(ruta)


def construir(k, drop):
    car, nom, voz_txt, pant, _ = S[k]
    t = tiempos(k)
    src = cuerpo(k)
    tot = dur(src)
    wav, dh = audio(M / f"voz3_{k}_{SUFIJO_VOZ}", "gancho3", voz_txt)
    hl = round(dh + 0.45, 3)                      # duración del gancho 3.0
    g = t["p1"]                                    # fin del gancho 2.0
    sp = 2.5
    a0 = max(0.0, g - hl * sp)
    w = TMP / f"w3_{k}"; w.mkdir(parents=True, exist_ok=True)
    placa(pant, w / "placa.png")
    # cortes del cuerpo: [0, p6) + [cierre, fin]  ó  [0, fin]
    segs = [(0.0, t[drop[0]]), (t["cierre"], tot)] if drop else [(0.0, tot)]
    ins = ["-ss", f"{a0}", "-to", f"{g}", "-i", str(src), "-i", str(wav), "-i", str(w / "placa.png")]
    fc = [f"[0:v]setpts=(PTS-STARTPTS)/{sp},trim=0:{hl},setpts=PTS-STARTPTS[gv0];[gv0][2:v]overlay=0:0[gv];"
          f"[1:a]aresample=48000,apad,atrim=0:{hl},asetpts=PTS-STARTPTS[ga]"]
    lab, n = "[gv][ga]", 0
    for a, b in segs:
        i = 3 + n
        ins += ["-ss", f"{a}", "-to", f"{b}", "-i", str(src)]
        fc.append(f"[{i}:v]setpts=PTS-STARTPTS[v{n}];[{i}:a]aresample=48000,asetpts=PTS-STARTPTS[a{n}]")
        lab += f"[v{n}][a{n}]"; n += 1
    fc.append(f"{lab}concat=n={n + 1}:v=1:a=1[v][a]")
    c3 = w / f"cuerpo3_{k}.mov"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *ins,
                    "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]", "-r", "30", "-c:v", "libx264", "-crf", "16",
                    "-preset", "medium", "-c:a", "pcm_s16le", str(c3)], check=True)
    c3 = Path(str(c3).replace(".mp4", ".mov"))
    dest = OUT / ("05 Instalaciones generales 3.0" if car == "05" else "06 Refedencias de arranques con contactor - Mejora 3.0")
    dest.mkdir(parents=True, exist_ok=True)
    sal = dest / f"{nom}.mp4"
    subprocess.run(["python3", str(M / "final_e.py"), str(c3), "v", str(sal), str(portada(k))], check=True, cwd=M)
    return sal, dur(sal)


def plan(ks, usados=None):
    """Elige qué párrafos quitar (ninguno, p6, o p5+p6 si el objetivo es corto) para acercarse al objetivo sin
    repetir duraciones (±1,5 s) ni caer en 1:32–1:34."""
    usados, res = list(usados or []), {}
    for k in ks:
        t = tiempos(k); tot = dur(cuerpo(k)); obj = S[k][4]
        opc = [((), tot + 3.6)]
        if "p6" in t:
            opc.append((("p6",), tot + 3.6 - (t["cierre"] - t["p6"])))
            if obj < 80 and "p5" in t:
                opc.append((("p5", "p6"), tot + 3.6 - (t["cierre"] - t["p5"])))
        ok = [o for o in opc if not (91.5 <= o[1] <= 94.5) and o[1] >= 60 and all(abs(o[1] - u) > 1.5 for u in usados)]
        drop, d = min(ok or opc, key=lambda o: abs(o[1] - obj))
        res[k] = drop; usados.append(d)
        print(k, "quita " + "+".join(drop) if drop else "completo", round(d, 1))
    return res


if __name__ == "__main__":
    ks = sys.argv[1:] or list(S)
    prev = [dur(f) for f in OUT.glob("*/*.mp4") if not any(S[k][1] == f.stem for k in ks)]
    p = plan(ks, prev)
    for k in ks:
        s, d = construir(k, p[k])
        print("OK", s.name, round(d, 1))
