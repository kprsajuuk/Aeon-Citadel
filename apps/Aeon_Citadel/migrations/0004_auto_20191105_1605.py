# Generated by Django 2.2.5 on 2019-11-05 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Aeon_Citadel', '0003_auto_20191101_1901'),
    ]

    operations = [
        migrations.AddField(
            model_name='journey',
            name='avatar_status',
            field=models.CharField(default='{}', max_length=128),
        ),
        migrations.AlterField(
            model_name='journey',
            name='event',
            field=models.CharField(default=None, max_length=512),
        ),
    ]
