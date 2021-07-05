from django.db import models

class videos(models.Model):
    title = models.CharField(max_length=500,null=True)
    description = models.CharField(max_length=2000,null=True)
    date = models.DateField(null=True)
    photo = models.DateField(null=True)
    url = models.DateField(null=True)


class api_keys(models.Model):
    api_key = models.CharField(max_length=300,null=True)