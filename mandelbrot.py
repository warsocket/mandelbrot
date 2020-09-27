#!/usr/bin/env python3

#pypy is signinifcantly faster
#!/usr/bin/env pypy3 

import os
import sys
from io import BytesIO
from PIL import Image, ImagePalette
import shutil
# from math import sin, cos, tan

_, XRANGE,YRANGE,TX,TY,ZF = sys.argv
XRANGE,YRANGE = map(int, [XRANGE, YRANGE])
TX,TY,ZF = map(float, [TX,TY,ZF])

NPROC=64
RANGE = min(XRANGE, YRANGE)
ZF = RANGE / 2.0 * ZF
XDX = (-XRANGE / 2.0) + TX*ZF
YDX = (-YRANGE / 2.0) + TY*ZF

rangesa = [0]
rangesb = []

acc = 0
step = YRANGE // NPROC
for r in range(NPROC-1):
	acc += step
	rangesa.append(acc)
	rangesb.append(acc)

rangesb.append(YRANGE)

ranges = list(zip(rangesa,rangesb))



def mkpalette():
	pal = []
	for x in range(0x100):
		pal.append([x,0,0])

	for x in range(0x100):
		pal.append([255,x,0])

	for x in range(0x100):
		pal.append([255-x,255,0])

	for x in range(0x100):
		pal.append([0,255,x])

	for x in range(0x100):
		pal.append([0,255-x,255])

	for x in range(0x100):
		pal.append([x,0,255])

	for x in range(0x100):
		pal.append([255,x,255])

	return pal


palette = mkpalette()
pallen = len(palette)


dibs = b''
for tid in range(NPROC):
	if not os.fork():
		dibline = []
		for py in range(*ranges[tid]):
			for px in range(XRANGE):
				x = (px + XDX) / ZF
				y = (py + YDX) / ZF

				###########
				# c = 0.25*(cos(x*3.1416*15)+1) + 0.25*(cos(y*3.1416*10)+1)
				# print(x)
				# c = [0,255][x**1+y**1<1]
				const = x+y*1j
				coord = 0j
				c=0
				for c in range(pallen):
					coord **= 2
					coord += const
					if (coord.imag**2 + coord.real**2) > 4:
						break
				c = max(0,min(c,pallen))
				c = pallen-c-1
				# c=0
				###########
				

				# pix[px,py] = int(255*c)
				# pi[px+py*1000] = c

				dibline.append(palette[c][0])
				dibline.append(palette[c][1])
				dibline.append(palette[c][2])
		with open("{}.dib".format(tid), "wb") as f:
			# f.write(bytearray(pi))
			f.write(bytearray(dibline))
		exit()



for tid in range(NPROC):
	os.waitpid(0, os.WUNTRACED)
	# print("done")

# print("done, emitting png")
dib = b''

for tid in range(NPROC):
	with open("{}.dib".format(tid), "rb") as f:
		dib += f.read()


im = Image.frombuffer("RGB", (XRANGE,YRANGE), dib, 'raw', "RGB", 0, 1)
x = BytesIO()
im.save(x, "png")
x.seek(0)
shutil.copyfileobj(x, sys.stdout.buffer)