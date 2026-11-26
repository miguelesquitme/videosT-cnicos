from PIL import Image, ImageDraw, ImageFont, ImageChops
import os,glob
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)
def trim(im):
    im=im.convert('RGB'); bg=Image.new('RGB',im.size,(255,255,255))
    diff=ImageChops.difference(im,bg).convert('L').point(lambda p:255 if p>12 else 0)
    bb=diff.getbbox(); return im.crop(bb) if bb else im
def panel(path,cap,S=300):
    c=Image.new('RGB',(S,S+28),'white')
    im=trim(Image.open(path)); im.thumbnail((S-16,S-16),Image.LANCZOS)
    c.paste(im,((S-im.width)//2,(S-im.height)//2))
    d=ImageDraw.Draw(c); w=d.textlength(cap,font=F); d.text(((S-w)/2,S+5),cap,fill=(90,100,115),font=F)
    return c
def sheet(code,items):
    ps=[panel(p,c) for p,c in items if p and os.path.exists(p)]
    W=sum(p.width for p in ps)+8*(len(ps)-1)
    out=Image.new('RGB',(W,ps[0].height),'white'); x=0
    for p in ps: out.paste(p,(x,0)); x+=p.width+8
    out.save(f'th/{code}.jpg',quality=88); return len(ps)
R='r3d/out/'
OF='Oficial (fabricante)'; A='3D · vista frontal'; B='3D · vista trasera'; P='Plano acotado'
def sie(m):
    return [(f'raw/sie/{m}_v1.jpg',OF),(R+f'{m}_0.png',A),(R+f'{m}_1.png',B),(f'raw/sie/{m}_d.jpg',P)]
def ifm(c):
    return [(f'raw/ifm/{c}_p.jpg',OF),(R+f'{c}_0.png',A),(R+f'{c}_1.png',B),(f'raw/ifm/{c}_d.jpg',P)]
S=['3SE5232-0HD03','3SE5312-0SD11','3SE2903-1AB20','3SE7150-1BD04','3RA2415-8XF31-1AB0','3RF3320-1AA04','3RV2917-1A','5TT4101-0','5SE2316','5SG1301','5ST3610','4NC5117-2CC21','7LF4521-0','7KT5803','8WH1000-1MG88','8WH1020-0AF00','8MR6423-6LV30','8MR2132-5AB','8MR2170-2KA','8MR2200-0B','6EP4134-3AB00-0AY0','6GK5005-0BA00-1AB2','6ES7155-6AU01-0BN0','3RT2916-1BB00','3UF7010-1AU00-0']
for m in S: print(m, sheet(m,sie(m)))
for c in ['O1D100','UGT500','MK5101','VVB001','O2D500','DTI410','JN2100','LMT100','LR2050','OPU200','OBF500','SD6000','AL1100','EVC001','EBC113','DP2200','DI6001']: print(c, sheet(c,ifm(c)))
se='raw/se/'
print(sheet('ATV320U15M2C',[(se+'ATV320U15M2C_v0.jpg','Oficial · frente'),(se+'ATV320U15M2C_v1.jpg','Oficial · lateral'),(se+'ATV320U15M2C_v2.jpg',P)]))
print(sheet('NSYS3D4320',[(se+'NSYS3D4320_v0.jpg','Oficial · cerrado'),(se+'NSYS3D4320_v1.jpg','Oficial · detalle'),(se+'NSYS3D4320_v2.jpg',P)]))
print(sheet('ABL6TS10U',[(se+'ABL6TS10U_v0.jpg','Oficial · frente'),(se+'ABL6TS10U_v1.jpg','Oficial · lateral'),(se+'ABL6TS10U_v2.jpg','Oficial · arriba')]))
print(sheet('PKF16M434',[(se+'PKF16M434_v0.jpg',OF),(se+'PKF16M434_v1.jpg','Vista explotada oficial')]))
for r in ['BLRCH104A125B48','VPL12N','BMH0701T06A2A','LV847123']: print(sheet(r,[(se+f'{r}_v0.jpg',OF)]))
print(sheet('W22-215T',[('r3d/motor_0.png','3D · lado del eje'),('r3d/motor_1.png','3D · lado del ventilador'),('r3d/motor_2.png','3D · lateral')]))
