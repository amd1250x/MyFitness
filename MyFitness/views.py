from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404

from forms import UserForm, LoginForm, FitnessLogForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.template import RequestContext
from models import FitnessLog

# Create your views here.
from django.http import HttpResponse


def index(request):
    return render_to_response('MyFitness/index.html',
                              {'user': request.user},
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
            exer = form.save(commit=False)
            exer.user = request.user
            new_exer = FitnessLog.objects.create(**form.cleaned_data)
            new_exer.save()
            return HttpResponseRedirect('/')
    else:
        form = FitnessLogForm()
    return render(request, 'MyFitness/add_fitness_log.html', {'form': form})

