import datetime

from django.db import models
from django.utils import timezone

'''
class Image(models.Model):
    id = models.CharField(primary_key=True, max_length=64)
    data = models.TextField(blank=True)
    class Meta:
        managed = False
        db_table = 'image'
'''

class Question(models.Model):
    type = models.IntegerField(blank=True, null=True)
    id = models.IntegerField(primary_key=True)  # AutoField?
    no = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True)
    content = models.TextField(blank=True)
    subject = models.IntegerField(db_column='subject',blank=True)
    rightanswer = models.TextField(db_column='rightAnswer', blank=True)  # Field name made lowercase.
    answerexplain = models.TextField(db_column='answerExplain', blank=True)  # Field name made lowercase.
    difficulty = models.IntegerField(blank=True, null=True)
    rightrate = models.FloatField(db_column='rightRate', blank=True, null=True)  # Field name made lowercase.
    hot = models.IntegerField(blank=True, null=True)
    storetime = models.DateField(db_column='storeTime', blank=True, null=True)  # Field name made lowercase.
    A = models.TextField(db_column='A', blank=True)  # Field name made lowercase.
    B = models.TextField(db_column='B', blank=True)  # Field name made lowercase.
    C = models.TextField(db_column='C', blank=True)  # Field name made lowercase.
    D = models.TextField(db_column='D', blank=True)  # Field name made lowercase.
    source = models.TextField(db_column='source', blank=True)  # Field name made lowercase.
    plainText = models.TextField(db_column='plainText', blank=True)  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'QUESTION'