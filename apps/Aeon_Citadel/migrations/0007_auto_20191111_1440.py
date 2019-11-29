# Generated by Django 2.2.5 on 2019-11-11 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Aeon_Citadel', '0006_journey_difficulty'),
    ]

    operations = [
        migrations.RenameField(
            model_name='journey',
            old_name='event',
            new_name='current_event',
        ),
        migrations.AddField(
            model_name='journey',
            name='event_queue',
            field=models.CharField(default='[]', max_length=1024),
        ),
    ]
