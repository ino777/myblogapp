# Generated by Django 2.1.5 on 2020-01-30 21:17

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='icon_image',
            field=imagekit.models.fields.ProcessedImageField(default='default-user-icon.png', upload_to='uploads/icon/%Y/%m/%d/'),
        ),
    ]
