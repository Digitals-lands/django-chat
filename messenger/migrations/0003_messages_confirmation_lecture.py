# Generated by Django 5.0.1 on 2024-03-18 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0002_alter_users_first_name_alter_users_last_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='confirmation_lecture',
            field=models.BooleanField(default=False),
        ),
    ]