from django.db import models

# Create your models here.
class Entry(models.Model):
    title = models.CharField(max_length=50, null=True)
    content = models.TextField(null=True)
    thumbnail = models.ImageField(null=True, blank=False, upload_to="media/")