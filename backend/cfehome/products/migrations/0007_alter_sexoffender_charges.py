# Generated by Django 4.2 on 2023-01-30 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_sexoffender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sexoffender',
            name='charges',
            field=models.CharField(max_length=200),
        ),
    ]
