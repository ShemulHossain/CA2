from django.views.generic import ListView
from django.shortcuts import render
from concert.models import Artist
from django.db.models import Q
from concert.models import Artist, Category

def filterView(request):
    qs = Artist.objects.all()
    categories = Category.objects.all()
    artist_name_query = request.GET.get('artist_name')
    id_exact_query = request.GET.get('id_exact')
    ticket_price_min = request.GET.get('ticket_price_min')
    ticket_price_max = request.GET.get('ticket_price_max')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    category = request.GET.get('category')
    available = request.GET.get('available')
    notAvailable = request.GET.get('notAvailable')
    if artist_name_query != '' and artist_name_query is not None:
        qs = qs.filter(name__icontains=artist_name_query)
    elif id_exact_query != '' and id_exact_query is not None:
        qs = qs.filter(id=id_exact_query)
    
    if ticket_price_min != '' and ticket_price_min is not None:
        qs = qs.filter(ticket_price__gte=ticket_price_min)
    if ticket_price_max != '' and ticket_price_max is not None:
        qs = qs.filter(ticket_price__lt=ticket_price_max)
    if date_min != '' and date_min is not None:
        qs = qs.filter(concert_date__gte=date_min)
    if date_max != '' and date_max is not None:
        qs = qs.filter(concert_date__lt=date_max)

    if category != '' and category is not None and category != 'Choose...':
        qs = qs.filter(category__name=category)

    if available == 'on':
        qs = qs.filter(available=True)
    elif notAvailable == 'on':
        qs = qs.filter(stock=False)

    context = {
        'queryset':qs,
        'categories':categories
    }

    
    return render(request, "search.html", context)
