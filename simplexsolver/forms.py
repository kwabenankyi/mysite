from django import forms
from .models import ObjectiveFunction, Constraint

class ObjectiveFunctionForm(forms.Form):
    objective_function = forms.CharField(max_length=200)

class ConstraintForm(forms.ModelForm):
    constraint = forms.CharField(max_length=200)

ConstraintsFormSet = forms.modelformset_factory(Constraint, fields=('constraint',), extra=0, min_num=2, validate_min=True)