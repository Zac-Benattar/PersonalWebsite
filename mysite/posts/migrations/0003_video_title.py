# Generated by Django 4.1.5 on 2023-04-02 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_remove_albumpost_name_remove_blogpost_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='title',
            field=models.CharField(default='Untitled Video', max_length=300, unique=True),
        ),
    ]