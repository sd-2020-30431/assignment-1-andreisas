from django.db import models

class User(models.Model):
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    cals = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class GList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    date = models.DateTimeField()

    def __str__(self):
        return self.name

class Item(models.Model):
    glist = models.ForeignKey(GList, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    exp_date = models.DateTimeField()
    cals = models.IntegerField(default=0)

    def __str__(self):
        return self.name