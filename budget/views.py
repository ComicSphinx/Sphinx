from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from sqlalchemy import true

from math import pi
import plotly.graph_objects as go
from bokeh.palettes import Category20c
from bokeh.plotting import figure
from bokeh.transform import cumsum
from bokeh.resources import CDN
from bokeh.embed import components
import pandas as pd

from datetime import datetime as datetime
from django.core.exceptions import ObjectDoesNotExist

from .forms import AddFieldForm
from .models import Budget, BudgetByMonths, BudgetByYears

# TODO изменить field на expenditure ?

@login_required(login_url='/accounts/login/')
def budget_view(request):
    add_field_form = AddFieldForm()
    budget_fields = Budget.objects.filter(user_id=request.user, active=True)
    budget_by_months = BudgetByMonths.objects.filter(user_id=request.user, active=True)
    budget_by_years = BudgetByYears.objects.filter(user_id=request.user, active=True)
    script, div = draw_historical_months_bar(budget_by_months)

    return render(request, 'budget.html', 
                    {'add_field_form': AddFieldForm, 'queryset': budget_fields, 
                    'pie': draw_pie(budget_fields), 
                    'script': script, 'div': div})

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

# переписать на draw_pie (отрисовывает пирог)
# def draw_historical_months_bar(budget_by_months):
#     x = {}
    
#     for i in budget_by_months:
#         x.update({i.month_number: i.field_value})
#     chart_colors = ['#44e5e2', '#e29e44', '#e244db',
#             '#d8e244', '#eeeeee', '#56e244', '#007bff', 'black'] # надо сделать data['color'] = Category20c[len(x)]

#     data = pd.Series(x).reset_index(name='value').rename(columns={'index': 'country'})
#     data['angle'] = data['value']/data['value'].sum() * 2*pi
#     data['color'] = chart_colors[:len(x)]

#     p = figure(height=350, title='Статьи бюджета по месяцам', toolbar_location=None,
#                     tools='hover', tooltips="@country: @value", x_range=(-0.5, 1.0))

#     p.wedge(x=0, y=1, radius=0.4, 
#                 start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'), 
#                 fill_color='color', legend_field='country', source=data)

#     p.axis.axis_label = None
#     p.axis.visible = False
#     p.grid.grid_line_color = None

#     return components(p, CDN)

def draw_historical_months_bar(budget_by_months):
    months  = ['August', 'September']
    fields  = ['На квартиру', 'Акции']
    colors = ["#c9d9d3", "#718dbf"] # не нужно хардкодить цвета, если будет больше или меньше 2 статей бюджета, будет ошибка
    data = {'months'    : months,
            'На квартиру'      : [100, 200],
            'Акции'      : [100, 200]}

    plot = figure(x_range=months, height=500, title='Статьи бюджета по месяцам',
                    toolbar_location=None, tools='hover', tooltips='$name @months: @$name')
    plot.vbar_stack(fields, x='months', width=0.9, color=colors, source=data, legend_label=fields)
    plot.y_range.start = 0
    # plot.x_range.range_padding = 0.1
    plot.xgrid.grid_line_color = None
    plot.axis.minor_tick_line_color = None
    plot.outline_line_color = None
    plot.legend.location = 'top_left'
    plot.legend.orientation = 'horizontal'

    return components(plot, CDN)

# def draw_historical_months_bar(budget_by_months):
#     fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
#     years = ["2015", "2016", "2017"]
#     colors = ["#c9d9d3", "#718dbf", "#e84d60"]

#     data = {'fruits' : fruits,
#             '2015'   : [2, 1, 4, 3, 2, 4],
#             '2016'   : [5, 3, 4, 2, 4, 6],
#             '2017'   : [3, 2, 4, 4, 5, 3]}

#     p = figure(x_range=fruits, height=250, title="Fruit Counts by Year",
#                toolbar_location=None, tools="hover", tooltips="$name @fruits: @$name")

#     p.vbar_stack(years, x='fruits', width=0.9, color=colors, source=data,
#                  legend_label=years)

#     p.y_range.start = 0
#     p.x_range.range_padding = 0.1
#     p.xgrid.grid_line_color = None
#     p.axis.minor_tick_line_color = None
#     p.outline_line_color = None
#     p.legend.location = "top_left"
#     p.legend.orientation = "horizontal"

#     return components(p, CDN)