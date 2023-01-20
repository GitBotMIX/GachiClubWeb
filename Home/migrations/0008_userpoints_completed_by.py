# Generated by Django 4.1.5 on 2023-01-15 10:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Home', '0007_alter_userpoints_points_alter_userpoints_quest_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpoints',
            name='completed_by',
            field=models.ManyToManyField(related_name='completed_tasks', to=settings.AUTH_USER_MODEL),
        ),
    ]
