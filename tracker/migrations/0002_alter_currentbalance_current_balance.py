# Generated by Django 5.1.3 on 2024-12-04 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currentbalance',
            name='current_balance',
            field=models.FloatField(default=0),
        ),
    ]
