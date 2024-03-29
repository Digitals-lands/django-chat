# Generated by Django 5.0.3 on 2024-03-22 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0004_users_is_online_alter_users_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='is_online',
        ),
        migrations.AlterField(
            model_name='messages',
            name='file',
            field=models.FileField(default=None, null=True, upload_to='media/document'),
        ),
        migrations.AlterField(
            model_name='users',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='users',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
    ]
