# Generated by Django 4.0.5 on 2022-08-01 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0051_remove_serviserequest_status_locations_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notifications',
            name='message',
            field=models.CharField(default='', max_length=300),
        ),
    ]
