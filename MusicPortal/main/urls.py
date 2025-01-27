from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('album/<int:album_id>', views.album, name='album'),
    path('user/', views.user, name='user'),
    path('cabinet/', views.cabinet, name='cabinet'),
    path('artist_registration/', views.artist_registration, name='artist_registration'),
    path('photo/', views.cabinet_photo, name='cabinet_photo'),
    path('bio/', views.bio, name='bio'),
    path('userbio/', views.user_bio, name='user_bio'),
    path('new_song', views.new_song, name='new_song'),
    path('new_album', views.new_album, name='new_album'),
    path('album/<int:album_id>', views.album, name='album'),
    path('expansion/<int:album_id>', views.album_expansion, name='album_expansion'),
    path('song_like/<int:song_id>', views.song_like, name='song_like'),
    path('album_like/<int:album_id>', views.album_like, name='album_like'),
]