# Generated by Django 4.0.5 on 2022-07-26 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0029_locations_service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animal',
            name='gender',
            field=models.CharField(choices=[('male', 'male'), ('female', 'female')], max_length=30),
        ),
        migrations.AlterField(
            model_name='surgicaloperations',
            name='owner',
            field=models.CharField(max_length=30),
        ),
    ]