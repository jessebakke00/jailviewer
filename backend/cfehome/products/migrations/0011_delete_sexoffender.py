# Generated by Django 4.2 on 2023-06-24 04:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_inmate_is_in_custody'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SexOffender',
        ),
    ]
