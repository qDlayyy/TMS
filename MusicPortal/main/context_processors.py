from .models import Artist

def artist_image(request):
    if request.user.is_authenticated:
        try:
            current_artist = Artist.objects.get(user=request.user)
            return {'artist_image': current_artist.image}
        except Artist.DoesNotExist:
            return {'artist_image': None}
    return {'artist_image': None} 