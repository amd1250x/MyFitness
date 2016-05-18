from django.http import HttpResponse


def index(request):
    return HttpResponse("Welcome to MyFitness. Work in Progress.")