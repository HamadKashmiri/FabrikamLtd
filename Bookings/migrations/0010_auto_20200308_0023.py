# Generated by Django 3.0.3 on 2020-03-08 00:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Bookings', '0009_auto_20200306_2033'),
    ]

    operations = [
        migrations.AddField(
            model_name='individualsession',
            name='isbooked',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='session',
            name='teacher',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
