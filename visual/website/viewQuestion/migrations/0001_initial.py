# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.CharField(max_length=64, serialize=False, primary_key=True)),
                ('data', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'image',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('type', models.IntegerField(null=True, blank=True)),
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('no', models.IntegerField(null=True, blank=True)),
                ('content', models.TextField(blank=True)),
                ('rightanswer', models.TextField(db_column=b'rightAnswer', blank=True)),
                ('answerexplain', models.TextField(db_column=b'answerExplain', blank=True)),
                ('difficulty', models.IntegerField(null=True, blank=True)),
                ('rightrate', models.FloatField(null=True, db_column=b'rightRate', blank=True)),
                ('hot', models.IntegerField(null=True, blank=True)),
                ('storetime', models.DateField(null=True, db_column=b'storeTime', blank=True)),
            ],
            options={
                'db_table': 'question',
                'managed': False,
            },
            bases=(models.Model,),
        ),
    ]
