# Generated by Django 2.1.5 on 2019-03-28 21:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_sourcing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 28, 18, 9, 43, 880352)),
        ),
        migrations.AlterField(
            model_name='eventstore',
            name='tracked_object_id',
            field=models.PositiveIntegerField(),
        ),
    ]
