# Generated by Django 4.0.5 on 2022-07-25 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_alter_myuser_b_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='b_date',
            field=models.DateField(default='2022-09-01', max_length=20),
            preserve_default=False,
        ),
    ]
