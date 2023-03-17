from django.db import models

# Create your models here.
class Comapny(models.Model):
    name =  models.CharField(max_length = 100)

    def __str__(self) -> str:
        return self.name

class Person(models.Model):
    comapny = models.ForeignKey(Comapny,null = True, blank=True, on_delete= models.CASCADE, related_name= 'company')
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self) -> str:
        return self.name

