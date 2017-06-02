from __future__ import unicode_literals
from django.db import models
from django.utils import timezone


class similar_users(models.Model):
    user_id = models.IntegerField()
    similar_user_id = models.IntegerField()
    similarity = models.FloatField()
    created_ts = models.DateTimeField()
    model_id = models.ForeignKey('Models', on_delete=models.CASCADE)


class similar_attractions(models.Model):
    attraction_id = models.IntegerField()
    similar_attraction_id = models.IntegerField()
    similarity = models.FloatField()
    created_ts = models.DateTimeField()
    model_id = models.ForeignKey('Models', on_delete=models.CASCADE)


class user_attraction_recommendations(models.Model):
    user_id = model.IntegerField()
    attraction_id = models.IntegerField()
    score = models.FloatField()
    rank = models.IntegerField()
    created_ts = model.DateTimeField()
    model_id = models.ForeignKey('Models', on_delete=models.CASCADE)


class attraction_user_recommendations(models.Model):
    attraction_id = models.IntegerField()
    user_id = model.IntegerField()
    score = models.FloatField()
    rank = models.IntegerField()
    created_ts = model.DateTimeField()
    model_id = models.ForeignKey('ml_model', on_delete=models.CASCADE)


class ml_model(models.Model):
    model_name = models.CharField(max_length=200)
    model_url = models.CharField(max_length=200)
    model_type = models.CharField(max_length=200)
    model_algorithm = models.CharField(max_length=200)
    model_rmse = models.FloatField()
    model_accuracy = models.FloatField()
    model_precision = models.FloatField()
    model_recall = models.FloatField
    models_auc = models.FloatField()
    model_fail_criteria = models.CharField(max_length=100)
    model_fail_threshold = models.FloatField()
    model_training_dataset_id = models.ForeignKey('ml_training_dataset')
    creation_ts = models.DateTimeField()


class ml_training_dataset(models.Model):
    file_name = models.CharField(max_length=200)
    number_of_examples = models.IntegerField()
    number_of_features = models.IntegerField()
    training_dataset_url = models.CharField(max_length=200)
    feature_column_names = models.CharField(max_length=200)
    creation_ts = models.DateTimeField()
