# Generated by Django 4.0.5 on 2022-07-27 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0035_alter_serviserequest_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medication',
            name='adminstrationRoute',
            field=models.CharField(blank=True, choices=[('Intramascular', 'Intramascular'), ('Intravenous', 'Intravenous'), ('Oral ', 'Oral'), ('Sublingual ', 'Sublingual'), ('Topical ', 'Topical'), ('Ocular ', 'Ocular'), ('Subcutaneous ', 'Subcutaneous')], max_length=30, null=True),
        ),
    ]
