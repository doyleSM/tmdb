from django.urls import path
from .views import playlists, show, new, search, new_movie_playlist, delete_from_playlist, delete_playlist, compartilhar

app_name = 'playlists'
urlpatterns = [
    path('', playlists, name="list"),
    path('show/<int:pk>', show, name="show"),
    path('new', new, name='new'),
    path('search/<int:pk>', search, name='search'),
    path('add/<int:pk>', new_movie_playlist, name="addmovie"),
    path('delete/<int:playlist>', delete_from_playlist, name="delete_from_pl"),
    path('deleteplaylist', delete_playlist, name="delete_pl"),
    path('compartilhar', compartilhar, name="compartilhar")
]
