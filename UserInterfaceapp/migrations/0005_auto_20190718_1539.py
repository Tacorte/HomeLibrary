# Generated by Django 2.2.3 on 2019-07-18 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserInterfaceapp', '0004_auto_20190718_1116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='middle_name',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='author',
            name='surname',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='book_in_library',
            name='size',
            field=models.IntegerField(blank=True),
        ),
    ]