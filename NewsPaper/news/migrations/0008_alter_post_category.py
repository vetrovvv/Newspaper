# Generated by Django 4.2 on 2023-05-13 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_alter_category_subscribers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ManyToManyField(default='4', through='news.PostCategory', to='news.category'),
        ),
    ]
