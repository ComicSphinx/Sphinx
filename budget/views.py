from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from sqlalchemy import true

from .forms import AddFieldForm
from .models import Budget

@login_required(login_url='/accounts/login/')
def budget_view(request):
    form = AddFieldForm()
    budget_fields = Budget.objects.filter(user=request.user)
    return render(request, 'budget.html', {'form': form}, budget_fields)

# TODO refactor it (name, at least)
def add_field_to_db(request):
    field_name = request.POST['field_name']
    field_value = request.POST['field_value']
    record = Budget(user=request.user, field_name=field_name, field_value=field_value, active=True)
    record.save()
    return redirect('/budget/')