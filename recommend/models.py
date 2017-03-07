from __future__ import unicode_literals
from django.db import models


class User(models.Model):
    app_id = models.IntegerField(default=000)
    user_id = models.IntegerField()
    email = models.CharField(max_length=200)
    first = models.CharField(max_length=100)
    last = models.CharField(max_length=100)


class Attraction(models.Model):
    app_id = models.IntegerField(default=000)
    attraction_id = models.IntegerField()
    attraction_name = models.CharField(max_length=2000)


class SimilarUsers(models.Model):
    user_id = models.IntegerField()
    similar_user_id = models.IntegerField()
    similarity = models.FloatField()
    ts = models.DateTimeField()


class SimilarAttractions(models.Model):
    attraction_id = models.IntegerField()
    similar_attraction_id = models.IntegerField()
    similarity = models.FloatField()
    ts = models.DateTimeField()

#
# class UserAttractionHistory(models.Model):
#     user_id = models.IntegerField()
#     attraction_id = models.IntegerField()
#
#
# class AttractionUserHistory(models.Model):
#     attraction_id = models.IntegerField()
#     user_id = models.IntegerField()
