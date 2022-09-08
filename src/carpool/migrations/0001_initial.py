# Generated by Django 4.0.5 on 2022-09-07 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('RideID', models.IntegerField()),
                ('UserName', models.CharField(max_length=128)),
                ('Approved', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('RideID', models.AutoField(primary_key=True, serialize=False)),
                ('Source_Address', models.CharField(max_length=128)),
                ('Dest_Address', models.CharField(max_length=128)),
                ('NumberPlate', models.CharField(max_length=128)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('Occupancy', models.IntegerField()),
                ('UserName', models.CharField(max_length=128)),
            ],
        ),
    ]
