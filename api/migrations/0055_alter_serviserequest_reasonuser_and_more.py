# Generated by Django 4.0.5 on 2022-08-06 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0054_alter_surgicaloperations_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviserequest',
            name='reasonUser',
            field=models.CharField(blank=True, default='', max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='serviserequest',
            name='reasonVet',
            field=models.CharField(blank=True, default='', max_length=300, null=True),
        ),
    ]
