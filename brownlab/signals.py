from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import FileUpload, FileData
from .load import read_sm4, planesub, xoffset, zexc
from PIL import Image


@receiver(post_save, sender=FileUpload)
def create_file_data(sender, instance, created, **kwargs):
	if created:
		img_data = read_sm4(str(instance))
		acq_date = img_data[0]
		acq_time = img_data[1]
		xysize_nm = img_data[2]
		xysize_ang = img_data[3]
		xoffset_value = img_data[4]
		yoffset = img_data[5]
		setpoint = img_data[6]
		bias = img_data[7]
		rawdata = img_data[8]
		comment = img_data[9]

		planedata = planesub(rawdata)
		psim = Image.fromarray(planedata)
		psout = zexc(psim, 0.01)

		psout.save(str(instance).replace('.sm4', '_ps.png'))

		xodata = xoffset(planedata)
		xoim = Image.fromarray(xodata)
		xout = zexc(xoim, 0.01)

		xout.save(str(instance).replace('.sm4', '_xo.png'))


		params = FileData(name=str(instance).replace('.sm4', ''), acq_date=acq_date, acq_time=acq_time, xysize_nm=xysize_nm, xysize_ang=xysize_ang, xoffset=xoffset_value, yoffset=yoffset, setpoint=setpoint, bias=bias, comment=comment, image= str(instance).replace('.sm4', '_ps.png'), xoimage= str(instance).replace('.sm4', '_xo.png'))

		params.save()