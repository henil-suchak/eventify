# Generated by Django 5.1.6 on 2025-02-15 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0004_alter_registration_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='event',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='user',
        ),
        migrations.RemoveField(
            model_name='registration',
            name='event',
        ),
        migrations.RemoveField(
            model_name='registration',
            name='user',
        ),
        migrations.DeleteModel(
            name='user',
        ),
        migrations.RemoveField(
            model_name='attendee',
            name='dob',
        ),
        migrations.RemoveField(
            model_name='attendee',
            name='user',
        ),
        migrations.RemoveField(
            model_name='event',
            name='organizer',
        ),
        migrations.AddField(
            model_name='attendee',
            name='events',
            field=models.ManyToManyField(related_name='event_attendees', to='event.event'),
        ),
        migrations.AlterField(
            model_name='attendee',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.RemoveField(
            model_name='event',
            name='max_attendees',
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
        migrations.DeleteModel(
            name='Registration',
        ),
        migrations.AddField(
            model_name='event',
            name='max_attendees',
            field=models.ManyToManyField(related_name='event_attendees', to='event.attendee'),
        ),
    ]
