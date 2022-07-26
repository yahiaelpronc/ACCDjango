# Generated by Django 4.0.5 on 2022-07-27 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0034_serviserequest_dismissuser_serviserequest_dismissvet_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviserequest',
            name='status',
            field=models.CharField(blank=True, choices=[('accepted', 'accepted'), ('pending', 'pending'), ('declined ', 'declined')], default='pending', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='surgicaloperationsrequest',
            name='status',
            field=models.CharField(blank=True, choices=[('accepted', 'accepted'), ('pending', 'pending'), ('declined ', 'declined')], default='pending', max_length=30, null=True),
        ),
    ]
