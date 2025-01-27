import os

from django.contrib import messages
from django.contrib.auth import login, logout
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect

from MusicPortal import settings
from .forms import RegistrationForm, LoginForm, ArtistRegistrationForm, PhotoUploadForm, ArtistBio, SongAddForm, \
    AlbumCreation, AlbumPhotoUploadForm, UserBio
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile, Artist, Song

from .models import Album
from .service.service import file_rename, list_of_songs, album_data, \
    list_of_missing_items, list_of_albums, song_data


def home(request):
    if request.user.is_authenticated:
        try:
            current_user_default_object = request.user
            current_user = UserProfile.objects.get(user=current_user_default_object)

        except:
            return redirect('logout')
    else:
        current_user = None

    new_songs_qs = Song.objects.order_by('?').filter()[:4]


    new_songs = []
    for song in new_songs_qs:
        new_songs.append(song_data(song, current_user))

    new_albums_qs = (
        Album.objects.annotate(song_count=Count('songs'))
        .filter(song_count__gt=0)
        .order_by('-release_date')
        [:2]
    )

    new_albums = []
    for current_album in new_albums_qs:
        new_albums.append(album_data(current_album, current_user))


    return render(request, 'main/home.html', {'new_songs': new_songs, 'new_albums': new_albums})


@csrf_exempt
def registration(request):
    if request.method == 'POST':
        registration_listener_form = RegistrationForm(request.POST)
        if registration_listener_form.is_valid():
            user = registration_listener_form.save()
            login(request, user)
            return redirect('home')
        else:
            for field, errors in registration_listener_form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        registration_listener_form = RegistrationForm()
    return render(request, 'main/registration.html', {"form":registration_listener_form})


@csrf_exempt
def log_in(request):
    if request.method == 'POST':
        login_form = LoginForm(request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('home')
        else:
            for field, errors in login_form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        login_form = LoginForm()

    return render(request, 'main/login.html', {"form":login_form})


def album(request, album_id):
    try:
        if request.user.is_authenticated:
            current_user = UserProfile.objects.get(user=request.user)
        else:
            current_user = False
        current_album = Album.objects.get(pk=album_id)
        songs = list_of_songs(current_album, current_user)
        current_album_data = album_data(current_album, current_user)

    except:
        return redirect('home')

    current_artist = Artist.objects.filter(user=request.user).first()
    if str(current_artist) not in current_album_data['artists']:
        is_allowed_to_edit = False
    else:
        is_allowed_to_edit = True

    if request.method == 'POST':
        album_photo_form = AlbumPhotoUploadForm(request.POST, request.FILES, instance=current_album)
        old_photo_url = current_album.image.url if current_album.image else None

        if album_photo_form.is_valid():
            image = album_photo_form.cleaned_data['image']
            print(image)

            if image:
                new_filename = file_rename(image.name)
                print(new_filename)
                current_album.image.name = new_filename

            if old_photo_url:
                old_photo_path = os.path.join(settings.MEDIA_ROOT, old_photo_url[7:])

                if os.path.isfile(old_photo_path):
                    os.remove(old_photo_path)

            album_photo_form.save()
        else:
            print(album_photo_form.errors)
        return redirect('album', album_id=album_id)

    return render(request, 'main/album.html', {'album': current_album_data, 'songs': songs, 'is_allowed_to_edit':is_allowed_to_edit})


def user(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        favorite_songs_qs = user_profile.favorite_songs.all()
        favorite_albums_qs = user_profile.favorite_albums.all()

        favorite_songs = []
        for song in favorite_songs_qs:
            favorite_songs.append(song_data(song, user_profile))

        favorite_albums = []
        for album in favorite_albums_qs:
            favorite_albums.append(album_data(album, user_profile))

        return render(request, 'main/user.html', {"user_profile":user_profile, "songs": favorite_songs,
                                                  'albums': favorite_albums})
    else:
        return redirect('login')


def cabinet(request):
    try:
        current_user_default_object = request.user
        artist = Artist.objects.filter(user=current_user_default_object).first()
    except:
        return redirect('home')


    if artist:
        current_user = UserProfile.objects.get(user=current_user_default_object)
        songs = list_of_songs(artist, current_user)
        albums = list_of_albums(artist)
        print(albums)
        if request.method == 'POST':
            print('we are here')
            photo_form = PhotoUploadForm(request.POST, request.FILES, instance=artist)
            old_photo_url = artist.image.url if artist.image else None

            if photo_form.is_valid():
                print('correct')
                image = photo_form.cleaned_data['image']
                print(image)

                if image:
                    new_filename = file_rename(image.name)
                    print(new_filename)
                    artist.image.name = new_filename

                if old_photo_url:
                    old_photo_path = os.path.join(settings.MEDIA_ROOT, old_photo_url[7:])

                    if os.path.isfile(old_photo_path):
                        os.remove(old_photo_path)

                photo_form.save()
            else:
                print(photo_form.errors)
            return redirect('cabinet')

        else:
            photo_form = PhotoUploadForm(instance=artist)

        return render(request, 'main/cabinet.html', {'artist': artist, 'photo_form': photo_form, 'songs': songs, 'albums': albums})

    else:
        return redirect('artist_registration')


def bio(request):
    artist = get_object_or_404(Artist, user=request.user)
    if request.method == 'POST':
        form = ArtistBio(request.POST, instance=artist)

        if form.is_valid():
            form.save()
            return redirect('cabinet')

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)

    else:
        form = ArtistBio(instance=artist)

    return render(request, 'main/bio_creation.html', {'form': form})


def user_bio(request):
    current_user = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = UserBio(request.POST, instance=current_user)

        if form.is_valid():
            form.save()
            return redirect('user')

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)

    else:
        form = UserBio(instance=current_user)

    return render(request, 'main/user_bio.html', {'form': form})


@csrf_exempt
def new_song(request):
    if request.method == 'POST':
        form = SongAddForm(request.POST, request.FILES)
        if form.is_valid():

            current_artist = Artist.objects.filter(user=request.user).first()
            new_artists = []
            if current_artist not in form.cleaned_data['artists']:
                for artist in form.cleaned_data['artists']:
                    new_artists.append(artist)
                new_artists.append(current_artist)
                form.cleaned_data['artists'] = new_artists

            form.save()
            return redirect('cabinet')

        else:
            print(form.errors)
    else:
        form = SongAddForm()
    return render(request, 'main/song_add.html', {'form': form})


def album_expansion(request, album_id):
    current_album = Album.objects.get(pk=album_id)
    if request.method == 'POST':
        form = SongAddForm(request.POST, request.FILES)
        if form.is_valid():
            song = form.save(commit=False)
            current_artist = Artist.objects.filter(user=request.user).first()
            current_album_artists = list(current_album.artists.all())
            new_artists = []
            if current_artist not in form.cleaned_data['artists']:

                for artist in form.cleaned_data['artists']:
                    new_artists.append(artist)
                new_artists.append(current_artist)
                form.cleaned_data['artists'] = new_artists

            song.album = current_album
            form.save()

            new_song_artists = list(song.artists.all())
            album_artists = list(current_album.artists.all())
            set_of_missing_artists = list_of_missing_items(new_song_artists, album_artists)
            current_album.artists.add(*set_of_missing_artists)

            new_song_genres = list(song.genres.all())
            album_genres = list(current_album.genres.all())
            set_of_new_genres = list_of_missing_items(new_song_genres, album_genres)
            current_album.genres.add(*set_of_new_genres)

            return redirect('album', album_id)

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = SongAddForm()

    return render(request, 'main/song_album_add.html', {'form': form, 'album': current_album})


@csrf_exempt
def artist_registration(request):
    if request.method == 'POST':
        artist_creation_form = ArtistRegistrationForm(request.POST)
        if artist_creation_form.is_valid():
            artist_creation_form.save(user=request.user)
            return redirect('cabinet')
        else:
            for field, errors in artist_creation_form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        artist_creation_form = ArtistRegistrationForm()

    return render(request, 'main/artist_creation.html', {"form": artist_creation_form})


@csrf_exempt
def cabinet_photo(request):
    if request.method == 'POST':
        pass
    else:
        form = PhotoUploadForm()
    return render(request, 'main/bio_creation.html', {"form": form})


def log_out(request):
    logout(request)
    return redirect('home')


@csrf_exempt
def new_album(request):
    if request.method == 'POST':
        form = AlbumCreation(request.POST)
        if form.is_valid():
            artist = Artist.objects.filter(user=request.user).first()
            saved_album = form.save(commit=False)
            saved_album.save()
            saved_album.artists.add(artist)
            return redirect('album', album_id=saved_album.id)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = AlbumCreation()
    return render(request, 'main/album_creation.html', {'form': form})


def song_like(request, song_id):
    if request.user.is_authenticated:

        song = Song.objects.get(pk=song_id)
        current_user_default_object = request.user
        current_user = get_object_or_404(UserProfile, user=current_user_default_object)

        is_current_song_favorite = current_user.favorite_songs.filter(id=song.id).exists()

        if is_current_song_favorite:
            current_user.favorite_songs.remove(song)

        else:
            current_user.favorite_songs.add(song)

    else:
        return redirect('login')

    next_url = request.GET.get('next', 'home')
    return redirect(next_url)


def album_like(request, album_id):
    if request.user.is_authenticated:

        current_album = Album.objects.get(pk=album_id)
        current_user_default_object = request.user
        current_user = get_object_or_404(UserProfile, user=current_user_default_object)

        is_current_album_favorite = current_user.favorite_albums.filter(id=current_album.id).exists()

        if is_current_album_favorite:
            current_user.favorite_albums.remove(current_album)

        else:
            current_user.favorite_albums.add(current_album)

    else:
        return redirect('login')

    next_url = request.GET.get('next', 'home')
    return redirect(next_url)