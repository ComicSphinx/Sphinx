from django import forms

class AddFieldForm(forms.Form):
    field_name = forms.CharField(label='Название поля:', max_length=30)
    field_value = forms.CharField(label='Значение', max_length=30)