# Generated by Django 4.0.5 on 2022-07-22 09:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_animal_locations_messages_myuser_vet_delete_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 22, 11, 12, 37, 126734)),
        ),
    ]
