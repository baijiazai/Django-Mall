from django.db import models


class Upload(models.Model):
    img = models.ImageField(upload_to='demo/%Y/%m/%d')