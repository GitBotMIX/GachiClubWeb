# Generated by Django 4.1.5 on 2023-01-27 15:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0019_alter_userprofile_options_quests_user_completion_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quests',
            name='user_completion',
        ),
    ]
