# Generated by Django 4.2.1 on 2023-05-11 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('slug', models.SlugField(max_length=128)),
                ('description', models.TextField(blank=True)),
                ('shop', models.CharField(max_length=128)),
                ('link', models.URLField(max_length=254)),
                ('image', models.URLField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='GameData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=0.0)),
                ('discount', models.FloatField(default=0.0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.game')),
            ],
        ),
    ]
