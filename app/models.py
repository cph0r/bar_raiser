from django.db import models

class status(models.Model):
    id = models.AutoField(primary_key=True)
    value = models.CharField(null=True,max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True,null=True)

    class Meta(object):
            ordering = ["id"]
    def __str__(self):
        return str(self.id)

class user(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True,null=True)
    status = models.ForeignKey(status,on_delete=models.CASCADE,null=True,default=1)
    class Meta(object):
        ordering = ["id"]
    def __str__(self):
        return str(self.id)

class product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(null=True,max_length=20)
    description =  models.CharField(null=True,max_length=500)
    price = models.IntegerField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True,null=True)

    class Meta(object):
        ordering = ["id"]
    def __str__(self):
        return str(self.id)

class deals(models.Model):
    id = models.AutoField(primary_key=True)
    start = models.DateTimeField(null=True)
    end  = models.DateTimeField(null=True)
    status = models.ForeignKey(status,on_delete=models.CASCADE,null=True,default=1)
    product = models.ForeignKey(product,on_delete=models.CASCADE,null=True)
    max_deals = models.IntegerField(null=True)
    current_deals = models.IntegerField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True,null=True)

    class Meta(object):
        ordering = ["id"]
    def __str__(self):
        return str(self.id)

class deal_transaction(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(user,on_delete=models.CASCADE,null=True)
    deal = models.ForeignKey(deals,on_delete=models.CASCADE,null=True)
    timestamp = models.DateTimeField(auto_now_add=True,null=True)

    class Meta(object):
        ordering = ["id"]
    def __str__(self):
        return str(self.id)