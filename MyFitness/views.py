from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404


# Create your views here.
from django.http import HttpResponse


def index(request):
    return render_to_response('MyFitness/index.html')


