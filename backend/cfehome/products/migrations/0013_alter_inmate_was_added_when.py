# Generated by Django 4.2 on 2023-06-26 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_inmate_was_added_when'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inmate',
            name='was_added_when',
            field=models.TimeField(auto_now_add=True, null=True),
        ),
    ]
