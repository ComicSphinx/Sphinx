from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required(login_url='/accounts/login/')
def index(request):
    return HttpResponse("budget. You are logged in")