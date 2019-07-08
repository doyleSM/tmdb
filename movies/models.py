from django.db import models


class Movie(models.Model):
    idmovie = models.IntegerField()
    playlist = models.ForeignKey(
        "playlist.Playlist", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.idmovie)
