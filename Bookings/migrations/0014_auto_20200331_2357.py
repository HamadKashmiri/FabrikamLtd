# Generated by Django 3.0.3 on 2020-03-31 23:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Bookings', '0013_session_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='session',
            old_name='image',
            new_name='logo',
        ),
    ]
