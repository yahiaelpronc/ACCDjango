# Generated by Django 4.0.5 on 2022-07-26 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_alter_medication_date_alter_messages_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='surgicaloperations',
            name='owner',
            field=models.CharField(default='mostafamasrya', max_length=30),
        ),
        migrations.AlterField(
            model_name='surgicaloperations',
            name='animalName',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='surgicaloperationsrequest',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
