from django import forms

class AddFieldForm(forms.Form):
    field_name = forms.CharField(label='field name:', max_length=30)
    field_value = forms.CharField(label='field value', max_length=30)