# Generated by Django 2.2.1 on 2019-10-03 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_remove_profile_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='limit',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
