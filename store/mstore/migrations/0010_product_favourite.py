# Generated by Django 4.2.4 on 2023-09-24 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mstore', '0009_productscheme'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='favourite',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
