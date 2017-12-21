# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Spider(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.TextField()
    price = models.TextField()
    mall = models.TextField()
    classification = models.TextField()
    posted_at = models.DateTimeField()
    fav_count = models.IntegerField()
    comments_count = models.IntegerField()
    zhi_count = models.IntegerField()
    vote_percent = models.IntegerField()
    url = models.TextField(unique=True)
    img = models.TextField()
    outdated = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'spider'
