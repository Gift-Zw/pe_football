# Generated by Django 5.0.6 on 2024-07-04 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolprofile',
            name='date_registered',
            field=models.DateTimeField(default=None),
        ),
    ]
