# Generated by Django 2.0.2 on 2018-02-18 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webtoon', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='rating',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='episode',
            name='title',
            field=models.CharField(max_length=150),
        ),
    ]
