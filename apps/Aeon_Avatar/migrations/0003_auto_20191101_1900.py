# Generated by Django 2.2.5 on 2019-11-01 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Aeon_Avatar', '0002_auto_20191018_1456'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='avatar',
            name='id',
        ),
        migrations.AddField(
            model_name='avatar',
            name='avatar_id',
            field=models.CharField(default='0', max_length=128, primary_key=True, serialize=False),
        ),
    ]