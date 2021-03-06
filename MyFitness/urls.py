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
    url(r'^edit-fitness/(?P<eid>\d+)/$', views.edit_fitness_log, name='edit_fitness_log'),
    url(r'^del-fitness/(?P<eid>\d+)/$', views.del_fitness_log, name='del_fitness_log'),
    url(r'^all-fitness', views.view_all_entries, name='view_all_entries'),
    url(r'^del-weight/(?P<id>\d+)/$', views.del_weight_log, name='del_weight_log'),
    url(r'^add-wlog/(?P<workout_id>\d+)/$', views.add_workout_log, name='add_workout_log'),
    url(r'^edit-wlog/(?P<workout_id>\d+)/(?P<wid>\d+)/$', views.edit_workout_log, name='edit_workout_log'),
    url(r'^del-wlog/(?P<workout_id>\d+)/$', views.del_workout_log, name='del_workout_log'),
    url(r'^add-workout-exer', views.add_workout_exercise, name='add_workout_exercise'),
    url(r'^edit-workout-exer/(?P<wid>\d+)/$', views.edit_workout_exercise, name='edit_workout_exercise'),
    url(r'^del-workout-exer/(?P<wid>\d+)/$', views.del_workout_exercise, name='del_workout_exercise'),
    url(r'^new-workout', views.add_workout, name='add_workout'),
    url(r'^edit-workout/(?P<wid>\d+)/$', views.edit_workout, name='edit_workout'),


    # RESTapi URLs
    url(r'^fitness-logs/$', views.fitness_log_list.as_view(), name='fitness_log_list'),
    url(r'^fitness-logs/(?P<pk>[0-9]+)$', views.fitness_log_detail.as_view(), name='fitness_log_detail'),
    url(r'^bodyweight-logs/$', views.bodyweight_log_list.as_view(), name='bodyweight_log_list'),
    url(r'^bodyweight-logs/(?P<pk>[0-9]+)$', views.bodyweight_log_detail.as_view(), name='bodyweight_log_detail'),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),

]
