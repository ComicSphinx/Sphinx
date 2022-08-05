from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from sqlalchemy import true

from .forms import AddFieldForm
from .models import Budget

@login_required(login_url='/accounts/login/')
def budget_view(request):
    add_field_form = AddFieldForm()
    budget_fields = Budget.objects.filter(user_id=request.user)
    return render(request, 'budget.html', {'add_field_form': AddFieldForm, 'queryset': budget_fields})

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
    
    # TODO: Скорректировать, чтобы обязательные поля (id не нужно было явно указывать)
    # TODO: оно обрезает строку (имя и значение) после пробела, починить
    field = Budget(id=field_id)
    field.user_id = request.user
    field.field_id = field_id
    field.field_name = field_name
    field.field_value = field_value
    field.active = True
    field.save()
    return redirect('/budget/')