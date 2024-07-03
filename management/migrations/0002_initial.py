# Generated by Django 5.0.6 on 2024-07-03 22:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('management', '0001_initial'),
        ('schools', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournamentresults',
            name='school1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='school1', to='schools.schoolprofile'),
        ),
        migrations.AddField(
            model_name='tournamentresults',
            name='school2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='school2', to='schools.schoolprofile'),
        ),
        migrations.AddField(
            model_name='tournamentresults',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.tournament'),
        ),
    ]