# Generated by Django 2.2.3 on 2019-07-15 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserInterfaceapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='password',
        ),
    ]
