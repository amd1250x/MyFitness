from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.views.generic import DeleteView
from forms import UserForm, LoginForm, FitnessLogForm, DelLogForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.template import RequestContext
from models import FitnessLog
import datetime
import uuid


# Create your views here.
from django.http import HttpResponse

token = uuid.uuid4()


def index(request):
    fitness_logs = FitnessLog.objects.all()
    today = datetime.datetime.today()

    class Day:
        def __init__(self, date):
            self.date = date
            self.display = self.date.strftime("%m/%d/%Y")
            self.w_display = self.date.strftime("%A")
            self.has_items = False

    days_pm2 = [Day(today - datetime.timedelta(3)),
                Day(today - datetime.timedelta(2)),
                Day(today - datetime.timedelta(1)),
                Day(today),
                Day(today + datetime.timedelta(1)),
                Day(today + datetime.timedelta(2)),
                Day(today + datetime.timedelta(3))]

    for item in fitness_logs:
        for i in range(len(days_pm2)):
            if item.date.day == days_pm2[i].date.day:
                days_pm2[i].has_items = True

    return render_to_response('MyFitness/index.html',
                              {'user': request.user,
                               'fitness_logs': fitness_logs,
                               'days_pm2': days_pm2,
                               'token': token},
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


def del_fitness_log(request, eid):
    if request.method == 'POST':
        form = DelLogForm(request.POST)
        if form.is_valid():
            entry = get_object_or_404(FitnessLog, pk=eid).delete()
            return HttpResponseRedirect('/')
    else:
        form = DelLogForm()
    return render(request, 'MyFitness/del_fitness_log.html', {'form': form})
