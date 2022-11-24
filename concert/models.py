from django.db import models
import uuid
from django.urls import reverse

class Category(models.Model):
    id = models.UUIDField(
    primary_key=True,
    default=uuid.uuid4,
    editable=False)
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(blank = True)
    image = models.ImageField(upload_to = 'category', blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('concert:artists_by_category', args=[self.id])

    def __str__(self):
        return self.name

class Artist(models.Model):
    id = models.UUIDField(
    primary_key=True,
    default=uuid.uuid4,
    editable=False)
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(blank = True)
    concert_date = models.DateTimeField(blank=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to = 'artist', blank=True)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'artist'
        verbose_name_plural = 'artists'

    def get_absolute_url(self):
        return reverse('concert:artist_detail', args=[self.category.id, self.id])

    def __str__(self):
        return self.name
