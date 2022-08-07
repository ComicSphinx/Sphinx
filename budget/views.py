from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from sqlalchemy import true
import plotly.express as px
import plotly.io as pio

from .forms import AddFieldForm
from .models import Budget

@login_required(login_url='/accounts/login/')
def budget_view(request):
    add_field_form = AddFieldForm()
    budget_fields = Budget.objects.filter(user_id=request.user)
    return render(request, 'budget.html', {'add_field_form': AddFieldForm, 'queryset': budget_fields, 'pie': draw_pie()})

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

def draw_pie():
    df = ['A', 'B', 'C'] # сюда положить названия колонок
    val = [50, 60, 70]
    fig = px.pie(df, title='Кошелёк', values=val)
    return(pio.to_html(fig, include_plotlyjs=True, full_html=False))