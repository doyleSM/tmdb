from django.contrib.auth.decorators import login_required
from .forms import PlaylistForm
from movies.models import Movie
from .models import Playlist
from django.shortcuts import render, redirect, get_object_or_404
import requests
from .share_bot import send_to_all
import datetime
from django.contrib import messages

# Create your views here.

SITE_URL = 'http://127.0.0.1:8000/'


class Details:
    title = None
    vote_average = None
    runtime = None
    id_movie = None
    poster_path = None
    release_date = None
    genre = []
    id_db = None
    imdb = None


key = 'api_key=0c6d96dc4c081f6c309a563acbcbd996'
base = 'http://api.tmdb.org/3/'

'''
retorna as playlists do usuário (logado)
'''


@login_required
def playlists(request):
    playlists = Playlist.objects.filter(user_id=request.user.pk)
    return render(request, "playlist/playlists.html", {"playlists": playlists})


def show(request, pk):
    playlist = get_object_or_404(Playlist, pk=pk)
    objs = Movie.objects.filter(playlist_id=pk)
    movies = []
    for m in objs:
        url = base+'movie/'+str(m.idmovie)+'?'+key
        r = requests.get(url).json()
        detail = get_details(r, m)
        movies.append(detail)
        detail = None
    return render(request, 'playlist/movies_playlist.html', {"movies": movies, "playlist": playlist})


@login_required
def new(request):
    if request.method == 'GET':
        form = PlaylistForm()
        return render(request, 'playlist/new.html', {'form': form})
    else:
        form = PlaylistForm(request.POST)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.user = request.user
            playlist.save()
            messages.success(request, 'Playlist criada!')
        else:
            messages.error(request, 'Erro ao criar playlist')
    return redirect("playlists:list")


@login_required
def search(request, pk):
    playlist = get_object_or_404(Playlist, pk=pk, user_id=request.user.pk)

    if request.method == 'GET':
        return render(request, "playlist/search_movie.html", {"playlist": playlist})
    search_movie = request.POST.get('busca', None)
    if search_movie is "":
        return render(request, 'playlist/search_movie.html', {"playlist": playlist})
    else:
        movie = search_movie.replace(' ', '+')
        url = base+'search/movie?'+key+'&query='+movie
        r = requests.get(url).json()
        movies = []
        for i in r['results']:
            movies.append(i)
        return render(request, "playlist/search_movie.html", {"busca": movies, "playlist": playlist})


@login_required
def new_movie_playlist(request, pk):
    if request.method == 'GET':
        return redirect("playlists:search", pk=pk)
    else:
        playlist = get_object_or_404(Playlist, pk=pk, user_id=request.user.pk)
        movies_add = request.POST.getlist('movies[]')
        for m in movies_add:
            movie = Movie()
            movie.idmovie = m
            movie.playlist = playlist
            movie.save()
    return redirect("playlists:list")


@login_required
def delete_from_playlist(request, playlist):
    try:
        id_movie = request.POST.get("movie")
        movie = get_object_or_404(Movie, pk=id_movie)
        playlist_obj = get_object_or_404(Playlist, pk=movie.playlist_id)
        if(request.user == playlist_obj.user):
            movie.delete()
            messages.success(request, 'Filme removido!')
        return redirect("playlists:show", pk=playlist)
    except:
        messages.success(request, 'Erro ao remover filme!')
    return redirect("playlists:show", pk=playlist)


@login_required
def delete_playlist(request):
    try:
        id_playlist = request.POST.get("playlist")
        playlist = get_object_or_404(
            Playlist, pk=id_playlist, user_id=request.user.pk)
        playlist.delete()
        messages.success(request, 'Playlist Removida!')
        return redirect("playlists:list")
    except:
        messages.error(request, 'Erro ao remover playlist!')
        return redirect("playlists:list")


@login_required
def compartilhar(request):

    try:
        pk = request.POST.get("share")
        playlist_url = SITE_URL+'playlists/show/'+pk
        send_to_all(playlist_url, request.user.username)
        messages.success(request, 'Playlist compartilhada!')
        return redirect("playlists:list")
    except:
        messages.error(request, 'Erro ao compartilhar playlist!')
        return redirect("playlists:list")


def get_details(json, m):
    detail = Details()
    detail.title = json['title']
    detail.vote_average = json['vote_average']
    detail.runtime = json['runtime']
    detail.idmovie = json['id']
    detail.poster_path = json['poster_path']
    detail.release_date = json['release_date']
    detail.release_date = datetime.datetime.strptime(
        detail.release_date, "%Y-%m-%d").strftime("%d/%m/%Y")
    detail.id_db = m.id
    detail.imdb = json['imdb_id']
    # for genre in json['genres']:
    #    detail.genre.append(genre['name'])
    genres = json['genres']
    g = [d['name'] for d in genres]
    detail.genre = g
    return detail
