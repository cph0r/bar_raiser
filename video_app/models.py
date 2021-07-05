from django.db import models

class videos(models.Model):
    video_id = models.CharField(max_length=200,null=True,unique=True)
    title = models.CharField(max_length=500,null=True)
    description = models.CharField(max_length=2000,null=True)
    date = models.DateTimeField(null=True)
    photo = models.CharField(max_length=100,null=True)
    url = models.CharField(max_length=500,null=True)

    def __str__(self):
        return self.title


class api_keys(models.Model):
    api_key = models.CharField(max_length=300,null=True)

    def __str__(self):
        return self.api_key