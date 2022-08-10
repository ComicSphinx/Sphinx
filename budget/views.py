from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from sqlalchemy import true
import plotly.graph_objects as go

from .forms import AddFieldForm
from .models import Budget

# TODO изменить field на expenditure ?

@login_required(login_url='/accounts/login/')
def budget_view(request):
    add_field_form = AddFieldForm()
    budget_fields = Budget.objects.filter(user_id=request.user, active=True)
    return render(request, 'budget.html', {'add_field_form': AddFieldForm, 'queryset': budget_fields, 'pie': draw_pie(budget_fields)})

# TODO refactor it (name, at least)
@login_required(login_url='/accounts/login/')
def add_field_to_db(request):
    field_name = request.POST['field_name']
    field_value = request.POST['field_value']
    record = Budget(user_id=request.user, field_name=field_name, field_value=field_value, active=True)
    record.save()
    return redirect('/budget/')

@login_required(login_url='/accounts/login/')
def update_field(request):
    field_id = request.POST['field_id']
    field_name = request.POST['field_name']
    field_value = request.POST['field_value']
    
    field = Budget.objects.get(id=field_id)
    field.field_name = field_name
    field.field_value = field_value
    field.save()
    return redirect('/budget/')

@login_required(login_url='/accounts/login/')
def delete_field(request):
        field_id = request.POST['field_id']
        field = Budget.objects.get(id=field_id)
        field.active = False
        field.save()
        return redirect('/budget/')

def draw_pie(budget_fields):# TODO: сделать отображение названий
    labels = []
    values = []

    for i in budget_fields:
        labels.append(i.field_name)
        values.append(i.field_value)
    
    figure = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+percent')])
    return(figure.to_html(figure, include_plotlyjs=True, full_html=False))