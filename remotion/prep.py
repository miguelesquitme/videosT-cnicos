"""Copia voces y efectos de un reel a public/ y escribe las props con los tiempos de cada sección."""
import sys, json, shutil, subprocess
from pathlib import Path
sys.path.insert(0, '/home/claude/elec')
from guiones_r import R
clave = sys.argv[1]
GAP, INI = 0.45, 0.35
src = Path(f'/home/claude/elec/voz_{clave}_GMbq1m_eleven')
dst = Path(f'/home/claude/remo/public/{clave}'); dst.mkdir(parents=True, exist_ok=True)
sec = []; t = INI
for k in R[clave][2]:
    w = src / f'{k}.wav'
    shutil.copy(w, dst / f'{k}.wav')
    d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(w)], capture_output=True, text=True).stdout)
    sec.append({'k': k, 'ini': round(t, 3), 'dur': round(d, 3)}); t += d + GAP
sfx = Path('/home/claude/remo/public/sfx'); sfx.mkdir(exist_ok=True)
for f in Path('/home/claude/elec/sfx').glob('*.wav'):
    shutil.copy(f, sfx / f.name)
props = {'clave': clave, 'tit1': R[clave][0], 'tit2': R[clave][1], 'sec': sec, 'total': round(t + 2.2, 2)}
Path(f'/home/claude/remo/props_{clave}.json').write_text(json.dumps(props, ensure_ascii=False, indent=1))
print(json.dumps(props, ensure_ascii=False))
