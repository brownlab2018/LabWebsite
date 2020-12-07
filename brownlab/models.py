from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class FileUpload(models.Model):
	title = models.CharField(max_length=100, blank=True, null=True)
	file = models.FileField(blank=True, null=True)
	date_uploaded = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

	def __str__(self):
		return str(self.file)


class FileData(models.Model):
	file_name = models.ForeignKey(FileUpload, on_delete=models.CASCADE, blank=True, null=True)
	name = models.CharField(max_length=100, blank=True, null=True)
	acq_date = models.DateField(blank=True, null=True)
	acq_time = models.TimeField(blank=True, null=True)
	xysize_nm = models.FloatField(blank=True, null=True)
	xysize_ang = models.FloatField(blank=True, null=True)
	xoffset = models.FloatField(blank=True, null=True)
	yoffset = models.FloatField(blank=True, null=True)
	setpoint = models.FloatField(blank=True, null=True)
	bias = models.FloatField(blank=True, null=True)
	comment = models.TextField(max_length=500, blank=True, null=True)
	image = models.ImageField(default='noimage.png', blank=True, null=True)
	xoimage = models.ImageField(default='noimage.png', blank=True, null=True)

	def __str__(self):
		return str(self.name)

	def get_absolute_url(self):
		return reverse('browse-detail', kwargs={'id': self.id})