# Generated by Django 4.1.5 on 2023-04-06 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_remove_post_post_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='hosting_method',
            field=models.CharField(choices=[('C', 'Static'), ('S', 'Server')], default='C', max_length=1),
        ),
    ]
