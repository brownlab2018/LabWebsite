from django.contrib import admin

from .models import FileUpload, FileData

# Register your models here.
admin.site.register(FileUpload)
admin.site.register(FileData)
