from django import forms
from .models import ObjectiveFunction, Constraint

class ObjectiveFunctionForm(forms.ModelForm):
    class Meta:
        model = ObjectiveFunction
        fields = ['objective_function']

class ConstraintForm(forms.ModelForm):
    class Meta:
        model = Constraint
        fields = ['constraint']

ConstraintsFormSet = forms.modelformset_factory(Constraint, fields=('constraint',), extra=0, min_num=2, validate_min=True)