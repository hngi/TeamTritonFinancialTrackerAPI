# Generated by Django 2.2.1 on 2019-10-03 22:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20191003_2228'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='age',
        ),
    ]
