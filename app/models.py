from django.db import models


class Circle(models.Model):
    name = models.CharField(max_length=20)
    color = models.CharField(max_length=10)
    x = models.FloatField()
    y = models.FloatField()

    def __str__(self):
        return self.name

    def save(self):
        print(self)
        return None