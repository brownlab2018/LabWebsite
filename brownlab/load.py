import struct
import numpy as np
import scipy
import hashlib
import os
import re
import tempfile
import zipfile
import collections
import shutil
import imghdr

from scipy import io
from datetime import date, datetime
from PIL import Image
from django.core.files.storage import default_storage


def read_sm4(filename):
	with default_storage.open(filename, 'rb') as f:
		psize = struct.unpack('h', f.read(2))[0] # -> 56
		# print('psize: ', psize)
		hdr = f.read(psize + 4) # -> b'S\x00T\x00i\x00M\x00a\x00g\x00e\x00 \x000\x000\x005\x00.\x000\x000\x004\x00 \x001\x00\x00\x00\x04\x00\x00\x00\x03\x00\x00\x00\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00'
		# print('hdr: ', hdr)
		total_page_count = struct.unpack('i', hdr[36:40])[0] # -> 4
		# print('total_page_count: ', total_page_count)
		obj_offset = struct.unpack('i', f.read(4))[0] # -> 94
		# print('obj_offset: ', obj_offset)
		f.seek(obj_offset + 20) # -> 114
		# print('first_seek: ', f.seek(obj_offset + 20))
		pia_offset = struct.unpack('i', f.read(4))[0] # -> 122
		# print('pia_offset: ', pia_offset)
		f.seek(pia_offset) # -> 122
		# print('second_seek: ', f.seek(pia_offset))

		page_offset = [] # -> []
		# print('page_offset: ', page_offset)
		page_size = [] # -> []
		# print('page_size: ', page_size)

		for p in range(0, total_page_count):
			f.seek(24, os.SEEK_CUR) # -> 170, 218, 266, 314
			# print('third_seek: ', f.seek(24, os.SEEK_CUR))
			page_olc = struct.unpack('i', f.read(4))[0] # -> 4, 262144, -545658365, 6
			# print('page_olc: ', page_olc)
			f.seek(4, os.SEEK_CUR) # -> 158, 194, 230, 266
			# print('fourth_seek: ', f.seek(4, os.SEEK_CUR))
			this_po = [] # -> [], [], [], []
			# print('this_po: ', this_po)
			this_ps = [] # -> [], [], [], []
			# print('this_ps: ', this_ps)

			for o in range(0, page_olc):
				f.seek(4, os.SEEK_CUR)
				# print('fifth_seek: ', f.seek(4, os.SEEK_CUR))
				this_po.append(struct.unpack('i', f.read(4))[0])
				# print('this_po.append: ', this_po)
				this_ps.append(struct.unpack('i', f.read(4))[0])
				# print('this_ps.append: ', this_ps)

			page_offset.append(this_po)
			# print('page_offset.append: ', page_offset)
			page_size.append(this_ps)
			# print('page_size.append: ', page_size)

		f.seek(page_offset[0][0]) # -> 5242
		# print('sixth_seek: ', f.seek(page_offset[0][0]))
		header = f.read(page_size[0][0]) # -> b'\xb4\x00\x13\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\xd0\x82?\xaf\xd0\x82?\xaf\xb0\x0f!\xa5\x00\x00\x00\x00\x1b\x9e%\xb5\xc2\x88\x1e5\x00\x00\x00\x00\x08Y\x9a:\x99\x99\x19\xbf\xff\xe6\xdb\xae\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x18\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
		# print('header: ', header)
		string_count = struct.unpack('h', header[2:4])[0] # -> 19
		# print('string_count: ', string_count)
		xypixels = struct.unpack('iiii', header[16:32])[2] # -> 256
		# print('xypixels: ', xypixels)
		xyz_scale = struct.unpack('fff', header[56:68]) # -> (-1.7417822739673738e-10, -1.7417822739673738e-10, -1.3969839113357318e-16)
		# print('xyz_scale: ', xyz_scale)
		xyz_offset = struct.unpack('fff', header[72:84]) # -> (-6.16973636624607e-07, 5.905859552512993e-07, 0.0)
		# print('xyz_offset: ', xyz_offset)
		bias = struct.unpack('f', header[88:92])[0] # -> -0.5999999642372131
		# print('bias: ', bias)
		current = struct.unpack('f', header[92:96])[0] # -> -1.000000013351432e-10
		# print('current: ', current)

		file_strings = [] # -> []
		# print('file_strings: ', file_strings)
		f.seek(5630) # -> 5630
		# print('seventh_seek: ', f.seek(5630))

		for s in range(0, string_count):
			ssize = struct.unpack('h', f.read(2))[0]
			# print('ssize: ', ssize)
			instr = f.read(ssize * 2).decode('latin-1')
			# print('instr: ', instr)
			file_strings.append(''.join([instr[2 * x] for x in range(0, ssize)]))
			# print('file_strings.append: ', file_strings)

		acq_date = datetime.date(datetime.strptime(file_strings[14], '%m/%d/%y')) # -> 2019-11-13
		# print('acq_date: ', acq_date)
		acq_time = datetime.time(datetime.strptime(file_strings[15], '%H:%M:%S')) # -> 13:02:36
		# print('acq_time: ', acq_time)
		comment = file_strings[11] # -> TCPP on HOPG, 3 ul spun-up at 500 rpm for 30 s, waited 20 s after dose before spun
		# print('comment: ', comment)

		xysize_nm = int(abs(xypixels * xyz_scale[0] * 1e09) * 100) / 100.0

		xysize_ang = int(abs(xypixels * xyz_scale[0] * 1e10) * 100) / 100.0 # 256 * -1.7417822739673738e-10 and converts it to angstroms -> 445.89
		# print('xysize: ', xysize)

		xoffset = xyz_offset[0] * 1e10 # Converts to angstroms -> -6169.73636624607
		# print('xoffset: ', xoffset)
		yoffset = xyz_offset[1] * 1e10 # Converts to angstroms -> 5905.859552512993
		# print('yoffset: ', yoffset)

		setpoint = current * 1e09 # Converts current from amps to nanoamps -> -0.1000000013351432
		# print('setpoint: ', setpoint)

		# Adds the data to the Params model
		# entry = Params(acq_date=acq_date, acq_time=acq_time, xysize=xysize, xoffset=xoffset, yoffset=yoffset, setpoint=setpoint, bias=bias, comment=comment, md5='')

		f.seek(page_offset[0][1]) # -> 6216
		# print('eigth_seek: ', f.seek(page_offset[0][1]))
		im = Image.new("F", (xypixels, xypixels)) # Creates a new image in mode F that is 256x256 pixels -> <PIL.Image.Image image mode=F size=256x256 at 0x7FDF55D12190>
		# print('im: ', im)
		imdata = struct.unpack('i' * xypixels * xypixels, f.read(xypixels * xypixels * 4))
		# print('imdata: ', imdata)
		im.putdata(imdata, xyz_scale[2] * 1e10, xyz_offset[2] * 1e10)
		# print('im: ', im)
		rawdata = np.asarray(im)
		# print('rawdata: ', rawdata)

		return acq_date, acq_time, xysize_nm, xysize_ang, xoffset, yoffset, setpoint, bias, rawdata, comment


	f.closed


def zexc(im, zexcval):
	sortedvals = np.sort(im, axis=None)
	slen = sortedvals.size
	minmax = {}
	minmax[0] = sortedvals[int(slen * zexcval)]
	minmax[1] = sortedvals[int(slen * (1 - zexcval)) - 1]
	# minmax = im.getextrema()
	sc = 1.0 / (minmax[1] - minmax[0])
	offs = -minmax[0] * sc
	out = im.point(lambda i: i * sc + offs)
	out = out.point(lambda i: i * 255 + 1)
	out = out.convert("L")
	return out


def planesub(rawdata):
	xysize = rawdata.shape[0]
	imrange = np.array(range(0, xysize)) - (xysize - 1) / 2.0
	xplane, yplane = np.meshgrid(imrange, imrange)
	xpn = xplane * xplane
	planenorm = np.sqrt(xpn.sum())
	xpn = xplane / planenorm
	ypn = yplane / planenorm
	xcoef = xpn * rawdata
	ycoef = ypn * rawdata
	psdata = rawdata - xcoef.sum() * xpn - ycoef.sum() * ypn
	return psdata


def xoffset(rawdata):
	xysize = rawdata.shape[0]
	offsets = rawdata.sum(axis=1) / xysize
	output = rawdata - np.outer(offsets, np.ones((1, xysize)))
	return output