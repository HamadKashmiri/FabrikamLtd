# Generated by Django 3.0.4 on 2020-03-22 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='suppTicket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=300)),
                ('email', models.EmailField(max_length=150)),
                ('name', models.CharField(max_length=50)),
                ('supptype', models.CharField(max_length=300)),
            ],
        ),
    ]
