from django.contrib import admin

from . models import UrlShortener


@admin.register(UrlShortener)
class UrlShortenerAdmin(admin.ModelAdmin):
    list_display = ('shorten_url', 'original_url', 'created')
    search_fields = ('original_url',)
    list_filter = ('created', )
