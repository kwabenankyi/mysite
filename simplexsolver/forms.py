from django import forms
from .models import ObjectiveFunction, Constraint

class ObjectiveFunctionForm(forms.Form):
    objective_function = forms.CharField(max_length=200, required=True)

class ConstraintForm(forms.Form):
    constraint = forms.CharField(max_length=200, required=True)

ConstraintsFormSet = forms.formset_factory(ConstraintForm, max_num=2, min_num=2, validate_min=True)