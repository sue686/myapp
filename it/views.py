from django.shortcuts import render
from .tables import BirthdayTable
from .models import Staffbirthday
from .forms import BirthdayaddForm
import datetime
from django.utils import timezone
from .filters import BirthdayFilter
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
import platform    # For getting the operating system name
import subprocess  # For executing a shell command
from django.views.decorators.csrf import csrf_exempt
import paramiko
import time
# Create your views here.
@login_required
def IThome_view(request):
    context = {
    #     'posts':Post.objects.all()
    }

    return render(request,'it/system.html',context)

