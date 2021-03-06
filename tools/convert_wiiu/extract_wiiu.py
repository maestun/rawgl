#!/usr/bin/env python
#
# Extract data files from the WiiU version of 'Another World 20th Anniversary Edition'.
#
# liblz4.so is required to decompress the game data.
#

import ctypes
import io
import os
import os.path
import struct
import sys
from PIL import Image

fname = 'content/archive.bin'
if len(sys.argv) > 1:
	fname = sys.argv[1]

f = open(fname, 'rb')
f.seek(-8, io.SEEK_END)
pos   = struct.unpack('>I', f.read(4))[0]
count = struct.unpack('>I', f.read(4))[0]

def read_cstr(f):
	str = ''
	while True:
		chr = f.read(1)
		if ord(chr) == 0:
			break
		str += chr
	return str

for i in range(0, count):
	f.seek(pos)

	fname        = read_cstr(f)
	uncompressed = struct.unpack('>I', f.read(4))[0]
	size         = struct.unpack('>I', f.read(4))[0]
	offset       = struct.unpack('>I', f.read(4))[0]
	flags        = struct.unpack('>I', f.read(4))[0]
	assert flags == 0 or flags == 1

	pos = f.tell()

	print "%s %d %d 0x%x 0x%x" % (fname, uncompressed, size, offset, flags)

	fn = os.path.join('dump', fname)
	try:
		os.makedirs(os.path.dirname(fn))
	except:
		pass

	f.seek(offset)

	if uncompressed != size:
		liblz4 = ctypes.cdll.LoadLibrary('liblz4.so')
		src = f.read(size)
		dst = ctypes.create_string_buffer(uncompressed)
		ret = liblz4.LZ4_decompress_safe(src, dst, size, uncompressed)
		if ret != uncompressed:
			print 'LZ4_decompress_safe returned %d, expected %d' % (ret, uncompressed)
			continue
		o = open(fn, 'wb')
		o.write(dst.raw)
		o.close()
	else:
		o = open(fn, 'wb')
		o.write(f.read(size))
		o.close()

	# background textures
	if fn.endswith('.awt'):
		awt = open(fn)
		# 12 bytes footer
		#   08 08 08 08 LE16(w) LE16(h) LE16(w) LE16(h)
		awt.seek(-8, io.SEEK_END)
		w = struct.unpack('>H', awt.read(2))[0]
		h = struct.unpack('>H', awt.read(2))[0]
		awt.seek(0)
		image = Image.frombytes('RGBA', (w, h), awt.read(w * h * 4))
		image.save(os.path.splitext(fn)[0] + '.png')

	# low resolution (original 320x200) background pictures
	elif fn.endswith('.bms'):
		os.rename(fn, os.path.splitext(fn)[0] + '.bmp')

	# game code (bytecode)
	elif fn.endswith('.mac'):
		asm = os.path.splitext(fn)[0] + '.asm'
		os.system('../disasm/disasm %s > %s' % (fn, asm))
