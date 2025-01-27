from django.contrib import admin
from .models import Genre, Artist, Album, Song, UserProfile

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'bio_short')
    search_fields = ('name', 'bio', 'user__username')
    readonly_fields = ('user',)

    fieldsets = (
        (None, {'fields': ('user', 'name')}),
        ('Biography', {'fields': ('bio',)}),
        ('Image', {'fields': ('image',)}),
    )

    def bio_short(self, obj):
        return obj.bio[:50]

    bio_short.short_description = 'Short biography'
    bio_short.admin_order_field = 'bio'


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_artists', 'release_date', 'bio_short')
    search_fields = ('title', 'artists__name', 'bio')
    list_filter = ('release_date', 'genres')
    filter_horizontal = ('artists', 'genres')
    readonly_fields = ('release_date',)

    fieldsets = (
        (None, {'fields': ('title',)}),
        ('Artists', {'fields': ('artists',)}),
        ('Genres', {'fields': ('genres',)}),
        ('Biography', {'fields': ('bio',)}),
        ('Image', {'fields': ('image',)}),
        ('Release date', {'fields': ('release_date',)}),
    )

    def get_artists(self, obj):
        return ", ".join([artist.name for artist in obj.artists.all()])
    get_artists.short_description = 'Artists'


    def bio_short(self, obj):
        return obj.bio[:50]
    bio_short.short_description = 'Short biography'


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_artists', 'album', 'audio' ,'release_date')
    search_fields = ('title', 'artists__name', 'album__title')
    list_filter = ('album', 'release_date', 'genres')
    filter_horizontal = ('artists', 'genres')
    readonly_fields = ('release_date',)


    fieldsets = (
        (None, {'fields': ('title', 'album')}),
        ('Artists', {'fields': ('artists',)}),
        ('Genres', {'fields': ('genres',)}),
        ('Audio', {'fields': ('audio',)}),
        ('Release date', {'fields': ('release_date',)}),
    )

    def get_artists(self, obj):
        return ", ".join([artist.name for artist in obj.artists.all()])
    get_artists.short_description = 'Artists'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio_short', 'get_favorite_songs', 'get_favorite_albums')
    search_fields = ('user__username', 'bio')
    list_filter = ('user__is_active',)
    readonly_fields = ('user',)

    fieldsets = (
        (None, {'fields': ('user',)}),
        ('Biography', {'fields': ('bio',)}),
        ('Favorite songs', {'fields': ('favorite_songs',)}),
        ('Favorite albums', {'fields': ('favorite_albums',)}),
    )

    def bio_short(self, obj):
        return obj.bio[:50]

    bio_short.short_description = 'Short biography'
    bio_short.admin_order_field = 'bio'

    def get_favorite_songs(self, obj):
        return ", ".join([song.title for song in obj.favorite_songs.all()])

    get_favorite_songs.short_description = 'Favorite songs'

    def get_favorite_albums(self, obj):
        return ", ".join([album.title for album in obj.favorite_albums.all()])

    get_favorite_albums.short_description = 'Favorite albums'

    def has_add_permission(self, request):
        return False


