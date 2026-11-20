import json, sys, importlib
srt, guion = sys.argv[1], sys.argv[2]
G = importlib.import_module(guion).GUION
d = json.load(open(srt))
out = {}
for k, t in G.items():
    ini = " ".join(t.split()[:7])
    for a, b, x in d:
        if x == ini:
            out[k] = a; break
for k, a in sorted(out.items(), key=lambda z: z[1]):
    print(f"{int(a//60)}:{int(a%60):02d}\t{k}")
