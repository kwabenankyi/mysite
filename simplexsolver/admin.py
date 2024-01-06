from django.contrib import admin
from .models import ObjectiveFunction, Constraint
# Register your models here.
admin.site.register(ObjectiveFunction)
admin.site.register(Constraint)