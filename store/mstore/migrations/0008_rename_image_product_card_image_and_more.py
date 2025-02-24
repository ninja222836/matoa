# Generated by Django 4.2.4 on 2023-08-20 08:43

from django.db import migrations, models
import mstore.fields
import mstore.models


class Migration(migrations.Migration):

    dependencies = [
        ('mstore', '0007_product_image_webp'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='image',
            new_name='card_image',
        ),
        migrations.RemoveField(
            model_name='product',
            name='image_webp',
        ),
        migrations.AddField(
            model_name='product',
            name='card_image_webp',
            field=mstore.fields.WEBPField(default=12, upload_to=mstore.models.image_folder, verbose_name='Card Image'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='description_for_slider',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='main_image',
            field=models.ImageField(default=12, upload_to='photos/product_images/%Y/%m/%d/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='main_image_webp',
            field=mstore.fields.WEBPField(default=1, upload_to=mstore.models.image_folder, verbose_name='Main Image webp'),
            preserve_default=False,
        ),
    ]
