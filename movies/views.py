from django.shortcuts import render
from .models import Movie

import requests

key = 'api_key=0c6d96dc4c081f6c309a563acbcbd996'
base = 'http://api.tmdb.org/3/'
# Create your views here.


def show(request, id):


http: // api.tmdb.org/3/movie/63441?api_key = 0c6d96dc4c081f6c309a563acbcbd996
