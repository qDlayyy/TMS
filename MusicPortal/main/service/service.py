import uuid

def file_rename(file_name):
    ext = file_name.split('.')[-1]
    new_filename = f"{uuid.uuid4()}.{ext}"
    return new_filename

def length_determination(array):
    return len(array)


def song_artists(song):
    artists_qs = list(song.artists.all())
    artists = [artist.name for artist in artists_qs]
    return artists


def list_of_songs(model_object, current_user):
    songs = model_object.songs.all()
    list_of_songs = []
    for song in songs:
        array_of_artists = list(song.artists.all())
        artists_names = [artist.name for artist in array_of_artists]

        if length_determination(artists_names) > 1:
            artists = ' & '.join(artists_names)
        else:
            artists = artists_names[0]

        if current_user:
            is_favorite = current_user.favorite_songs.filter(id=song.id).exists()
        else:
            is_favorite = False

        song_data = {
            'id': song.id,
            'title': song.title,
            'album_id': song.album_id,
            'audio': song.audio,
            'release_date': song.release_date,
            'artists': artists,
            'is_favorite': is_favorite,
        }
        list_of_songs.append(song_data)
    return list_of_songs


def list_of_albums(model_object):
    albums = model_object.albums.all()
    print(albums)

    list_of_albums = []

    for album in albums:

        album_artists_qs = album.artists.all()
        album_artists_list = [artist.name for artist in album_artists_qs]
        album_artists = ' & '.join(album_artists_list)

        current_album_data = {
            'id': album.id,
            'title': album.title,
            'artists': album_artists,
            'image': album.image,
            'release_date': album.release_date,
        }
        list_of_albums.append(current_album_data)

    return list_of_albums


def song_data(song, current_user):
    if not current_user:
        is_favorite = False
    else:
        is_favorite = current_user.favorite_songs.filter(id=song.id).exists()

    artists_names = song_artists(song)

    if length_determination(artists_names) > 1:
        artists = ' & '.join(artists_names)
    else:
        artists = artists_names[0]

    data = {
        'id': song.id,
        'title': song.title,
        'audio': song.audio,
        'artists': artists,
        'is_favorite': is_favorite,
        'release_date': song.release_date,
    }

    return data


def album_data(current_album, current_user):
    current_album_artists = list(current_album.artists.all())
    list_of_artists = [artist.name for artist in current_album_artists]

    if length_determination(list_of_artists) > 1:
        artists = ' & '.join(list_of_artists)
    elif length_determination(list_of_artists) == 1:
        artists = list_of_artists[0]
    else:
        return None

    current_album_genres = list(current_album.genres.all())
    list_of_genres = [genre.name for genre in current_album_genres]

    if current_user:
        is_favorite = current_user.favorite_albums.filter(id=current_album.id).exists()
    else:
        is_favorite = False

    dict_of_data = {
        'id': current_album.id,
        'title': current_album.title,
        'artists': artists,
        'bio': current_album.bio,
        'genres': list_of_genres,
        'image': current_album.image,
        'is_favorite': is_favorite,
        'release_date': current_album.release_date,
    }

    return dict_of_data


def list_of_missing_items(list_of_new_items, list_of_current_items):
    if list_of_current_items:
        missing_items = set(list_of_new_items) - set(list_of_current_items)
    else:
        missing_items = list_of_new_items
    return missing_items
