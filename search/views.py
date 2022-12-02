from concert.models import Artist
from django.views.generic import ListView
from django.db.models import Q

class SearchResultsListView(ListView):
    model = Artist
    context_object_name = 'artist_list'
    template_name = 'search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Artist.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))

    def get_context_data(self, **kwargs):
        context = super(SearchResultsListView, self).get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context