from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.views.generic import DeleteView
from forms import UserForm, LoginForm, FitnessLogForm, DelLogForm, BodyWeightLogForm, DelBodyWeightLogForm, \
                WorkoutExerciseForm, WorkoutLogForm, WorkoutForm, DelWorkoutLogForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.template import RequestContext
from models import FitnessLog, BodyWeightLog, WorkoutLog, WorkoutExercise, Workout
import datetime
import uuid

# REST API stuff
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from serializers import FitnessLogSerializer, UserSerializer, BodyweightLogSerializer
from rest_framework import generics
from rest_framework import permissions
from permissions import IsOwnerOrReadOnly


# Create your views here.
from django.http import HttpResponse

token = uuid.uuid4()


def index(request):
    fitness_logs = FitnessLog.objects.all()
    weight_logs = BodyWeightLog.objects.all()

    workout_exercises = WorkoutExercise.objects.all()
    exercises = []
    for w in workout_exercises:
        if w.ename not in exercises:
            exercises.append(w.ename)

    time_label = []
    for e in fitness_logs:
        if e.date.strftime("%m/%d/%Y") not in time_label:
            time_label.append(e.date.strftime("%m/%d/%Y"))

    today = datetime.datetime.today()

    sorted_fit = []
    for f in fitness_logs:
        if f.owner == request.user:
            sorted_fit.append(f)
    sorted_fit.sort(key=lambda x: x.ename, reverse=False)

    class Day:
        def __init__(self, date):
            self.date = date
            self.display = self.date.strftime("%m/%d/%Y")
            self.w_display = self.date.strftime("%A")
            self.has_items = False
            self.is_today = False
            self.is_active = False

    days_pm2 = [Day(today - datetime.timedelta(3)),
                Day(today - datetime.timedelta(2)),
                Day(today - datetime.timedelta(1)),
                Day(today),
                Day(today + datetime.timedelta(1)),
                Day(today + datetime.timedelta(2)),
                Day(today + datetime.timedelta(3))]

    days_bt = [Day(today - datetime.timedelta(3)),
                Day(today - datetime.timedelta(2)),
                Day(today - datetime.timedelta(1))]

    days_at = [Day(today + datetime.timedelta(1)),
                Day(today + datetime.timedelta(2)),
                Day(today + datetime.timedelta(3))]

    days_t = [Day(today)]

    days_pm2[3].is_today = True

    for item in fitness_logs:
        for i in range(len(days_pm2)):
            if item.date.day == days_pm2[i].date.day and item.owner == request.user:
                days_pm2[i].has_items = True

    today_morning_weight = "--"
    today_afternoon_weight = "--"
    for w in weight_logs:
        if w.user == request.user.username:
            if w.date == today.date():
                if w.tod == 1:
                    today_morning_weight = w
                elif w.tod == 2:
                    today_afternoon_weight = w

    form = BodyWeightLogForm()
    if request.method == 'POST':
        if request.POST['action'] == 'Submit Weight':
            form = BodyWeightLogForm(request.POST)
            if form.is_valid():
                form_data = form.cleaned_data
                form_data['user'] = request.user.username
                new_weight = BodyWeightLog.objects.create(**form_data)
                new_weight.save()
            return HttpResponseRedirect('/')
    else:
        form = BodyWeightLogForm()

    return render(request, 'MyFitness/index.html', {'user': request.user,
                                                    'fitness_logs': sorted_fit,
                                                    'days_pm2': days_pm2,
                                                    'days_bt': days_bt,
                                                    'days_at': days_at,
                                                    'days_t': days_t ,
                                                    'token': token,
                                                    'form': form,
                                                    'today': today,
                                                    'weight_logs': weight_logs,
                                                    'tmw': today_morning_weight,
                                                    'taw': today_afternoon_weight,
                                                    'exercises': workout_exercises,
                                                    'time_label': time_label},)


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
        form = LoginForm()
    return render(request, 'MyFitness/login_user.html', {'form': form})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


def add_fitness_log(request):
    if request.method == 'POST':
        form = FitnessLogForm(request.POST, user=request.user)
        if form.is_valid():
            form_data = form.cleaned_data
            form_data['owner'] = request.user
            form_data['workout'] = "None"
            if form_data['ename_str'] != "":
                form_data['ename'] = form_data['ename_str']
                form_data['ename_str'] = ""
            new_exer = FitnessLog.objects.create(**form_data)
            new_exer.save()
            return HttpResponseRedirect('/')
    else:
        form = FitnessLogForm(user=request.user, initial={'w_units': '1',
                                                          'weight': '0',
                                                          'r_units': '3',
                                                          'activity': '1'})
    return render(request, 'MyFitness/add_fitness_log.html', {'form': form})


def add_workout(request):
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            form_data['owner'] = request.user
            new_exer = Workout.objects.create(**form_data)
            new_exer.save()
            return HttpResponseRedirect('/')
    else:
        form = WorkoutForm()
    return render(request, 'MyFitness/add_workout.html', {'form': form})


def add_workout_exercise(request):
    if request.method == 'POST':
        form = WorkoutExerciseForm(request.POST, user=request.user)
        if form.is_valid():
            form_data = form.cleaned_data
            form_data['owner'] = request.user
            new_exer = WorkoutExercise.objects.create(**form_data)
            new_exer.save()
            return HttpResponseRedirect('/')
    else:
        form = WorkoutExerciseForm(user=request.user)
    return render(request, 'MyFitness/add_workout_exercise.html', {'form': form})


def add_workout_log(request, workout_id):
    if request.method == 'POST':
        form = WorkoutLogForm(request.POST, user=request.user, workout_id=workout_id)
        if form.is_valid():
            form_data = form.cleaned_data
            # create a fitness log for each exercise in the workout
            workout = WorkoutExercise.objects.all().filter(workout=Workout.objects.get(id=workout_id))
            for c, w in enumerate(workout):
                FitLog = FitnessLog(ename=w.ename,
                                    ename_str=w.ename,
                                    date=form_data['date'],
                                    activity=w.activity,
                                    reps=w.reps,
                                    r_units=w.r_units,
                                    sets=w.sets,
                                    weight=[x.strip() for x in form_data['weights'].split(',')][c],
                                    w_units=form_data['w_units'],
                                    fromworkout=True,
                                    owner=request.user)
                FitLog.save()
            form_data['owner'] = request.user
            form_data['workout'] = Workout.objects.get(id=workout_id).name
            new_exer = WorkoutLog.objects.create(**form_data)
            new_exer.save()
            return HttpResponseRedirect('/')
    else:
        form = WorkoutLogForm(user=request.user, workout_id=workout_id)
    return render(request, 'MyFitness/add_workout_log.html', {'form': form})


def del_workout_log(request, workout_id):
    if request.method == 'POST':
        form = DelWorkoutLogForm(request.POST)
        if form.is_valid():
            entry = get_object_or_404(WorkoutLog, id=workout_id).delete()
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
    else:
        form = DelWorkoutLogForm()
    return render(request, 'MyFitness/del_workout_log.html', {'form': form})


def del_fitness_log(request, eid):
    if request.method == 'POST':
        form = DelLogForm(request.POST)
        if form.is_valid():
            entry = get_object_or_404(FitnessLog, pk=eid).delete()
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
    else:
        form = DelLogForm()
    return render(request, 'MyFitness/del_log.html', {'form': form})


def view_all_entries(request):
    entries = FitnessLog.objects.all()
    n_entries = []
    for e in entries:
        if e.owner == request.user:
            n_entries.append(e)
    return render(request, 'MyFitness/view_all_entries.html',
                              {'entries': n_entries})


def del_weight_log(request, id):
    if request.method == 'POST':
        form = DelBodyWeightLogForm(request.POST)
        if form.is_valid():
            entry = get_object_or_404(BodyWeightLog, pk=id).delete()
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
    else:
        form = DelBodyWeightLogForm()
    return render(request, 'MyFitness/del_log.html', {'form': form})




# More REST API stuff
class fitness_log_list(generics.ListCreateAPIView):
    queryset = FitnessLog.objects.all()
    serializer_class = FitnessLogSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class fitness_log_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = FitnessLog.objects.all()
    serializer_class = FitnessLogSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)


class bodyweight_log_list(generics.ListCreateAPIView):
    queryset = BodyWeightLog.objects.all()
    serializer_class = BodyweightLogSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



class bodyweight_log_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BodyWeightLog.objects.all()
    serializer_class = BodyweightLogSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
