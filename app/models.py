from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Count, Sum, Avg
from django.urls import reverse
from django.db.models.functions import Coalesce
import datetime


class FilmRatingManager(models.Manager):
    def save_rating(self, film_id, film_rating, user_id):
        old_data = None
        old = self.filter(film_id = film_id, user_id = user_id)
        if old.count() > 0:
            old_data = old[0].film_rating

        obj, new = self.update_or_create(film_id=film_id, user_id=user_id, defaults={'film_rating': film_rating})
        flag = not new
        return flag, old_data, self.get_rating(film_id)

    def exist_rating(self, film_id):
        res = self.filter(film_id=film_id).aggregate(count=Count('*'))['count']
        return True if res > 0 else False

    def delete_ratings_by_film_id(self, film_id):
        res = self.filter(film_id=film_id).delete()
        return res

    def get_rating(self, film_id):
        if self.exist_rating(film_id) == False:
            return -1
        res = self.filter(film_id=film_id).aggregate(avg=Avg('film_rating'))['avg']
        return res

    def get_users_by_film(self, id):
        res = self.filter(film_id=id).values_list('user_id', flat=True)
        res = list(res)
        return res if len(res) > 0 else -1

    def get_films_by_user(self, id):
        res = self.filter(user_id=id).values_list('film_id', flat=True)
        res = list(res)
        return res if len(res) > 0 else -1


class FilmRating(models.Model):
    film_id = models.IntegerField()
    film_rating = models.IntegerField(default = 0)
    user_id = models.IntegerField()

    objects = FilmRatingManager()

class AccessApplication(models.Model):
    appName = models.CharField(max_length=200)
    appSecret = models.CharField(max_length=200, default=None)
    appToken = models.CharField(max_length=200)
    life = models.IntegerField()
    created = models.DateTimeField()
