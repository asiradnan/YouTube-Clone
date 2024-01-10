from django.db import models

class Video(models.Model):
    thumbnail = models.ImageField(upload_to='thumbnails/')
    video = models.FileField(upload_to='videos/')
    title = models.CharField(max_length= 255)


