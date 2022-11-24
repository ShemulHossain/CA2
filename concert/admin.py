from django.contrib import admin
from .models import Category, Artist

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Category, CategoryAdmin)

class ArtistAdmin(admin.ModelAdmin):
    list_display = ['name', 'ticket_price', 'concert_date','description', 'category', 'stock',
    'available']
    list_editable = ['ticket_price', 'stock', 'available']
    list_per_page = 20

admin.site.register(Artist, ArtistAdmin)
