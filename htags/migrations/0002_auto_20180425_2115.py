# Generated by Django 2.0.4 on 2018-04-26 03:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('htags', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='url',
            name='pub_date',
        ),
        migrations.AddField(
            model_name='url',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
