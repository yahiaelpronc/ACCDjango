# Generated by Django 4.0.5 on 2022-08-07 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0057_merge_20220807_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medication',
            name='date',
            field=models.CharField(blank=True, default='2022-08-07', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='messages',
            name='date',
            field=models.CharField(default='2022-08-07', max_length=30),
        ),
    ]
