# Generated by Django 4.1.5 on 2023-01-17 16:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0015_remove_userquests_quests_completed_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userquests',
            name='quest_completed',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='Home.quests', verbose_name='Выполненное задание'),
        ),
    ]
