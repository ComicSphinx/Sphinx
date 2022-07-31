from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import AddFieldForm

@login_required(login_url='/accounts/login/')
def budget_view(request):
    form = AddFieldForm()
    return render(request, 'budget.html', {'form': form})