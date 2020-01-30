# Generated by Django 2.1.5 on 2020-01-31 01:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_auto_20190904_1939'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='was_updated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='commentreply',
            name='was_updated',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='comment',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 31, 1, 4, 23, 237319)),
        ),
        migrations.AlterField(
            model_name='commentreply',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 31, 1, 4, 23, 237817)),
        ),
    ]
