# Generated by Django 4.0.5 on 2022-07-30 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0048_remove_serviserequest_status_locations_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='isOwner',
            field=models.BooleanField(default=False),
        ),
    ]