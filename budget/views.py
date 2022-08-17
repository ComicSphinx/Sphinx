from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from sqlalchemy import true
import plotly.graph_objects as go
from datetime import datetime as datetime
from django.core.exceptions import ObjectDoesNotExist

from .forms import AddFieldForm
from .models import Budget, BudgetByMonths, BudgetByYears

# TODO изменить field на expenditure ?

@login_required(login_url='/accounts/login/')
def budget_view(request):
    add_field_form = AddFieldForm()
    budget_fields = Budget.objects.filter(user_id=request.user, active=True)
    return render(request, 'budget.html', 
                    {'add_field_form': AddFieldForm, 'queryset': budget_fields, 
                    'pie': draw_pie(budget_fields), 'bar_by_months': draw_historical_months_bar(request.user), 
                    'bar_by_years': draw_historical_years_bar(request.user)})

# TODO refactor it (name, at least)
@login_required(login_url='/accounts/login/')
def add_field_to_db(request):
    field_name = request.POST['field_name']
    field_value = request.POST['field_value']
    budget = Budget(user_id=request.user, field_name=field_name, field_value=field_value, active=True)
    budget.save()
    BudgetByMonths(user_id=request.user, field_id=budget, field_name=field_name, field_value=field_value, month_number=datetime.now().month, active=True).save()
    BudgetByYears(user_id=request.user, field_id=budget, field_name=field_name, field_value=field_value, year_number=datetime.now().year, active=True).save()
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

    # TODO: refactoring
    try:
        field_by_months = BudgetByMonths.objects.get(field_id=field, month_number=datetime.now().month)
        field_by_months.field_name = field_name
        field_by_months.field_value = field_value
        field_by_months.save()
    except BudgetByMonths.DoesNotExist:
        BudgetByMonths(user_id=request.user, field_id=field, field_name=field_name, field_value=field_value, month_number=datetime.now().month, active=True).save()

    try:
        field_by_years = BudgetByYears.objects.get(field_id=field, year_number = datetime.now().year)
        field_by_years.field_name = field_name
        field_by_years.field_value = field_value
        field_by_years.save()
    except BudgetByYears.DoesNotExist:
        BudgetByYears(user_id=request.user, field_id=field, field_name=field_name, field_value=field_value, year_number=datetime.now().year, active=True).save()

    return redirect('/budget/')

@login_required(login_url='/accounts/login/')
def delete_field(request):
    field_id = request.POST['field_id']

    field = Budget.objects.get(id=field_id)
    field.active = False
    field.save()

    budget_by_months = BudgetByMonths.objects.get(field_id=field, month_number=datetime.now().month)
    budget_by_months.active=False
    budget_by_months.save()

    budget_by_years = BudgetByYears.objects.get(field_id=field, year_number=datetime.now().year)
    budget_by_years.active=False
    budget_by_years.save()

    return redirect('/budget/')

def draw_pie(budget_fields):
    labels = []
    values = []

    for i in budget_fields:
        labels.append(i.field_name)
        values.append(i.field_value)
    
    figure = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+percent', insidetextorientation='radial', textposition='inside')])
    return(figure.to_html(figure, include_plotlyjs=True, full_html=False))

# TODO: Сделать так, чтобы цвета совпадали с круговым графиком
# TODO: Если статья не обновлялась в месяце, то она и не будет отображаться для него. Надо сделать так, 
#       чтобы оно автоматически целпяло сумму последнего зафиксированного месяца, если статья еще активна. 
#       Либо добавлять записи о каждой активной статье с наступлением месяца. Если статья для текущего месяца не найдена (и если она не active=False), 
#       то добавлять в массив запись с прошлого месяца
# TODO: Также необходимо отображать статью во всех месяцах, когда она была активна, и не отображать, когда она была удалена. Работает ли это сейчас?
# TODO: Когда я сделаю вывод месяцев в виде названий, сделать сортировку по X (чтобы месяца по порядку появлялись, можно по дате создания сортировать)
# TODO: Сделать нормальное отображение значений в боксе при наведении на сегмент
# TODO: этот метод можно сделать универсальныМ, передавая в него параметры, и сразу получать в одной функции и график по месяцам, и по годам
def draw_historical_months_bar(user):
    names = BudgetByMonths.objects.filter(user_id=user, active=True).values_list('field_name').values_list('field_name', flat=True).distinct()
    figure = go.Figure()

    for i in names:
        values = BudgetByMonths.objects.filter(user_id=user, active=True, field_name=i).values_list('field_value', flat=True).distinct()
        months = BudgetByMonths.objects.filter(user_id=user, active=True, field_name=i).values_list('month_number', flat=True).distinct()
        figure.add_trace(go.Bar(x=list(months), y=list(values), name=i))

    figure.update_layout(barmode='stack', xaxis={'categoryorder':'category ascending'})
    return(figure.to_html(figure, include_plotlyjs=True, full_html=False))

# TODO: Сделать так, чтобы цвета совпадали с круговым графиком
# TODO: Если статья не обновлялась в месяце, то она и не будет отображаться для него. Надо сделать так, 
#       чтобы оно автоматически целпяло сумму последнего зафиксированного месяца, если статья еще активна. 
#       Либо добавлять записи о каждой активной статье с наступлением месяца. Если статья для текущего месяца не найдена (и если она не active=False), 
#       то добавлять в массив запись с прошлого месяца
# TODO: Также необходимо отображать статью во всех месяцах, когда она была активна, и не отображать, когда она была удалена. Работает ли это сейчас?
# TODO: Когда я сделаю вывод месяцев в виде названий, сделать сортировку по X (чтобы месяца по порядку появлялись, можно по дате создания сортировать)
# TODO: Сделать нормальное отображение значений в боксе при наведении на сегмент
def draw_historical_years_bar(user):
    names = BudgetByYears.objects.filter(user_id=user, active=True).values_list('field_name').values_list('field_name', flat=True).distinct()
    figure = go.Figure()

    for i in names:
        values = BudgetByYears.objects.filter(user_id=user, active=True, field_name=i).values_list('field_value', flat=True).distinct()
        years = BudgetByYears.objects.filter(user_id=user, active=True, field_name=i).values_list('year_number', flat=True).distinct()
        figure.add_trace(go.Bar(x=list(years), y=list(values), name=i))

    figure.update_layout(barmode='stack', xaxis={'categoryorder':'category ascending'})
    return(figure.to_html(figure, include_plotlyjs=True, full_html=False))