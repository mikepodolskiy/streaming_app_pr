# Generated by Django 4.2.5 on 2024-02-03 12:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filmwork',
            name='certificate',
        ),
    ]
