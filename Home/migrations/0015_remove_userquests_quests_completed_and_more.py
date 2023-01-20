# Generated by Django 4.1.5 on 2023-01-17 16:09

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0014_userquests_delete_userpoints'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userquests',
            name='quests_completed',
        ),
        migrations.AddField(
            model_name='userquests',
            name='completed_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Выполнено'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userquests',
            name='quest_completed',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='Home.quests', verbose_name='Выполненное задание'),
        ),
    ]
