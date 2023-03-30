# Generated by Django 4.1.5 on 2023-03-08 13:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_alter_meeting_date_alter_project_current_deadline_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='riskevaluation',
            name='initial_evaluation',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='riskevaluation',
            name='serialized_project_evaluation_data',
            field=models.BinaryField(null=True),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 15, 13, 24, 58, 252227, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='project',
            name='current_deadline',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 15, 13, 24, 58, 252227, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='project',
            name='initial_deadline',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 15, 13, 24, 58, 252227, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='project',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 8, 13, 24, 58, 252227, tzinfo=datetime.timezone.utc)),
        ),
    ]
