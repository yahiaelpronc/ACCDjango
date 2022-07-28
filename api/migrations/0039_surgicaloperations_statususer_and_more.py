# Generated by Django 4.0.5 on 2022-07-27 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0038_alter_surgicaloperationsrequest_statususer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='surgicaloperations',
            name='statusUser',
            field=models.CharField(blank=True, choices=[('accepted', 'accepted'), ('pending', 'pending'), ('declined', 'declined')], default='pending', max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='surgicaloperations',
            name='statusVet',
            field=models.CharField(blank=True, choices=[('accepted', 'accepted'), ('pending', 'pending'), ('declined', 'declined')], default='pending', max_length=30, null=True),
        ),
    ]