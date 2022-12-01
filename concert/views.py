from django.shortcuts import render, get_object_or_404
from .models import Category, Artist

def art_list(request, category_id=None):
    category = None
    artists = Artist.objects.filter(available=True)
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        artists = Artist.objects.filter(category=category, available=True)
    return render(request, 'concert/category.html', {'category':category, 'art':artists})
    
def artist_detail(request, category_id, artist_id):
    artist = get_object_or_404(Artist, category_id=category_id, id=artist_id)
    return render(request, 'concert/artist.html', {'artist':artist})