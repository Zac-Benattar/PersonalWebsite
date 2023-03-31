# Generated by Django 4.1.5 on 2023-03-31 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_alter_blogpost_image_paths'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='tags',
            field=models.ManyToManyField(blank=True, to='posts.tag'),
        ),
        migrations.AddField(
            model_name='video',
            name='tags',
            field=models.ManyToManyField(blank=True, to='posts.tag'),
        ),
    ]
