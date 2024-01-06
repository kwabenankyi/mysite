from django.db import models

# Create your models here.
class ObjectiveFunction(models.Model):
    objective_function = models.CharField(max_length=200)
    def __str__(self):
        return self.objective_function

class Constraint(models.Model):
    constraint = models.CharField(max_length=200)
    def __str__(self):
        return self.constraint