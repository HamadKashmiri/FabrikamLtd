# Generated by Django 3.0.3 on 2020-03-02 15:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Bookings', '0004_auto_20200221_1628'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndividualSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bookings.Session')),
            ],
        ),
    ]
