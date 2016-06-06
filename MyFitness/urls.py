from django.conf.urls import url
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add-user', views.add_user, name='add_user'),
    url(r'^login-user', views.login_user, name='login_user'),
    url(r'^logout-user', views.logout_user, name='logout_user'),
    url(r'^add-fitness', views.add_fitness_log, name='add_fitness_log'),
]
