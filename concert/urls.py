from django.urls import path
from . import views

app_name = 'concert'

urlpatterns = [
    path('', views.art_list, name = 'all_artists'),
    path('<uuid:category_id>/', views.art_list, name = 'artists_by_category'),
    path('<uuid:category_id>/<uuid:artist_id>/>', views.artist_detail, name = 'artist_detail'),
    path('venue/', views.concert_view, name = 'venue'),
]
