from rest_framework import serializers
from .models import FitnessLog, BodyWeightLog
from django.contrib.auth.models import User


class FitnessLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessLog
        fields = ('id', 'ename', 'date', 'activity', 'reps', 'r_units', 'sets', 'weight', 'w_units', 'workout')


class BodyweightLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyWeightLog
        fields = ('id', 'weight', 'w_units', 'tod')


class UserSerializer(serializers.ModelSerializer):
    fitness_logs = serializers.PrimaryKeyRelatedField(many=True, queryset=FitnessLog.objects.all())
    bodyweight_logs = serializers.PrimaryKeyRelatedField(many=True, queryset=BodyWeightLog.objects.all())
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = User
        fields = ('id', 'username', 'fitness_logs', 'bodyweight_logs', 'owner')
