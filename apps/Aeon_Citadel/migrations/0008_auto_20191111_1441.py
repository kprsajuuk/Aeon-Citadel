# Generated by Django 2.2.5 on 2019-11-11 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Aeon_Citadel', '0007_auto_20191111_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journey',
            name='difficulty',
            field=models.IntegerField(default=1),
        ),
    ]