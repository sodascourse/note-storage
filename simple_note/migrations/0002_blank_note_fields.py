# Generated by Django 1.11.1 on 2017-05-30 07:57
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simple_note', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='content',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='note',
            name='title',
            field=models.TextField(blank=True),
        ),
    ]
