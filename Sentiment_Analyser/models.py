from django.db import models


class User(models.Model):
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.name, self.password

class Time(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.CharField(max_length=200)

    def __str__(self):
        return self.time

class Render(models.Model):
    time = models.ForeignKey(Time, on_delete=models.CASCADE)
    rd = models.CharField(max_length=300)
    
    def __str__(self):
        return self.rd