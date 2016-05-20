from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404

from forms import UserForm, LoginForm, FitnessLogForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.template import RequestContext
from models import FitnessLog
import datetime

# Create your views here.
from django.http import HttpResponse


def index(request):
    fitness_logs = FitnessLog.objects.all()
    today = datetime.datetime.today()
    yesterday = today - datetime.timedelta(1)
    tomorrow = today + datetime.timedelta(1)
    tod_has_items = False
    yes_has_items = False
    tom_has_items = False
    no_items = False
    for item in fitness_logs:
        if item.date.day == today.day:
            tod_has_items = True
        elif item.date.day == yesterday.day:
            yes_has_items = True
        elif item.date.day == tomorrow.day:
            tom_has_items = True
        else:
            no_items = True

    return render_to_response('MyFitness/index.html',
                              {'user': request.user,
                               'fitness_logs': fitness_logs,
                               'tod_has_items': tod_has_items,
                               'yes_has_items': yes_has_items,
                               'tom_has_items': tom_has_items,
                               'today': today,
                               'yesterday': yesterday,
                               'tomorrow': tomorrow},
                              context_instance=RequestContext(request))


def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            new_user.save()
            return HttpResponseRedirect('/')
    else:
        form = UserForm()
    return render(request, 'MyFitness/add_user.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse('Disabled account')
        else:
            return HttpResponse('invalid login')
    else:
        form = LoginForm
    return render(request, 'MyFitness/login_user.html', {'form': form})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


def add_fitness_log(request):
    if request.method == 'POST':
        form = FitnessLogForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            form_data['user'] = request.user.username
            new_exer = FitnessLog.objects.create(**form_data)
            new_exer.save()
            return HttpResponseRedirect('/')
    else:
        form = FitnessLogForm()
    return render(request, 'MyFitness/add_fitness_log.html', {'form': form})

