#!/bin/bash
# hoja_t.sh video salida.png t1 t2 ...  → hoja de contacto en los tiempos dados
V=$1; O=$2; shift 2
D=$(mktemp -d); i=0
for t in "$@"; do i=$((i+1)); ffmpeg -loglevel error -y -ss $t -i $V -frames:v 1 -vf scale=270:-1 $D/$(printf %02d $i).png; done
python3 -c "
import glob,sys
from PIL import Image
fs=sorted(glob.glob('$D/*.png')); ims=[Image.open(f) for f in fs]
w,h=ims[0].size; c=10; r=(len(ims)+c-1)//c
o=Image.new('RGB',(w*c,h*r))
for i,im in enumerate(ims): o.paste(im,((i%c)*w,(i//c)*h))
o.save('$O')"
rm -rf $D
