# Generated by Django 5.1.6 on 2025-03-04 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0013_alter_event_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendeerequest',
            name='is_attending',
            field=models.BooleanField(default=True),
        ),
    ]
