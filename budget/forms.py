from django import forms

class AddFieldForm(forms.Form):
    field_name = forms.CharField(label='field name:', max_length=30)