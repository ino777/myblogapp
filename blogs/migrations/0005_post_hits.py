# Generated by Django 2.1.5 on 2020-02-05 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0004_auto_20200131_0106'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='hits',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
