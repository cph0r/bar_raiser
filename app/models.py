from django.db import models

class user(models.Model):
    id = models.AutoField(primary_key=True)

    class Meta(object):
        ordering = ["id"]
    def __str__(self):
        return self.id