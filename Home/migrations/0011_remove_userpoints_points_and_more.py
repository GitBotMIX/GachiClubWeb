# Generated by Django 4.1.5 on 2023-01-15 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0010_remove_userpoints_completed_by_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userpoints',
            name='points',
        ),
        migrations.AlterField(
            model_name='userpoints',
            name='quests_completed',
            field=models.ManyToManyField(blank=True, null=True, related_name='completed_tasks', to='Home.quests', verbose_name='Выполненные задания'),
        ),
    ]
