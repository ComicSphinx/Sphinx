from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from sqlalchemy import true
import plotly.graph_objects as go
import datetime

from .forms import AddFieldForm
from .models import Budget, BudgetByMonths, BudgetByYears

# TODO изменить field на expenditure ?

@login_required(login_url='/accounts/login/')
def budget_view(request):
    add_field_form = AddFieldForm()
    budget_fields = Budget.objects.filter(user_id=request.user, active=True)
    return render(request, 'budget.html', {'add_field_form': AddFieldForm, 'queryset': budget_fields, 'pie': draw_pie(budget_fields), 'bar_by_months': draw_historical_months_bar(request.user)})

# TODO refactor it (name, at least)
@login_required(login_url='/accounts/login/')
def add_field_to_db(request):
    field_name = request.POST['field_name']
    field_value = request.POST['field_value']
    budget = Budget(user_id=request.user, field_name=field_name, field_value=field_value, active=True)
    budget.save()
    BudgetByMonths(user_id=request.user, field_id=budget, field_name=field_name, field_value=field_value, month_number=datetime.datetime.now().month, active=True).save()
    BudgetByYears(user_id=request.user, field_id=budget, field_name=field_name, field_value=field_value, year_number=datetime.datetime.now().year, active=True).save()
    return redirect('/budget/')

@login_required(login_url='/accounts/login/')
def update_field(request):
    field_id = request.POST['field_id']
    field_name = request.POST['field_name']
    field_value = request.POST['field_value']
    
    budget = Budget.objects.get(id=field_id)
    budget.field_name = field_name
    budget.field_value = field_value
    budget.save()

    # TODO: refactoring
    # сделать исключение, если не найдено, то создать
    try:
        budget_by_months = BudgetByMonths.objects.get(field_id=budget.id, month_number = datetime.now().month)
        budget_by_months.field_name = field_name
        budget_by_months.field_value = field_value
        budget_by_months.save()
    except model.DoesNotExist:
        BudgetByMonths(user_id=request.user, field_id=budget.id, field_name=field_name, field_value=field_value, month_number=datetime.now().month, active=True).save()

    try:
        budget_by_years = BudgetByYears.objects.get(field_id=budget.id, year_number = datetime.now().year)
        budget_by_years.field_name = field_name
        budget_by_years.field_value = field_value
        budget_by_years.save()
    except model.DoesNotExist:
        BudgetByYears(user_id=request.user, field_id=budget.id, field_name=field_name, field_value=field_value, year_number=datetime.now().year, active=True).save()

    return redirect('/budget/')

@login_required(login_url='/accounts/login/')
def delete_field(request):
    field_id = request.POST['field_id']
    field = Budget.objects.get(id=field_id)
    field.active = False
    field.save()
    return redirect('/budget/')

def draw_pie(budget_fields):
    labels = []
    values = []

    for i in budget_fields:
        labels.append(i.field_name)
        values.append(i.field_value)
    
    figure = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+percent', insidetextorientation='radial', textposition='inside')])
    return(figure.to_html(figure, include_plotlyjs=True, full_html=False))

def draw_historical_months_bar(user_id):
    months = BudgetByMonths.objects.filter(user_id=user_id, active=True).values_list('month_number').distinct()
        
    figure = go.Figure()
    for i in months:
        name, values = BudgetByMonths.objects.filter(user_id=user_id, active=True, month_number=i).values_list('field_name', 'field_value')
        figure.add_trace(x=i, y=values)

    figure.update_layout(barmode='stack')
    
    return(figure.to_html(figure, include_plotlyjs=True, full_html=False))