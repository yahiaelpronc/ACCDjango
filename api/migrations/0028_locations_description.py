# Generated by Django 4.0.5 on 2022-07-26 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_surgicaloperations_owner_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='locations',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]