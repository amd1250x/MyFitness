from django.contrib import admin
from models import FitnessLog, BodyWeightLog, Workout, WorkoutExercise, WorkoutLog
# Register your models here.


admin.site.register(FitnessLog)
admin.site.register(BodyWeightLog)
admin.site.register(Workout)
admin.site.register(WorkoutExercise)
admin.site.register(WorkoutLog)
