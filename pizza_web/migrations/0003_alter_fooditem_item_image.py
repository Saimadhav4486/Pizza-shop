# Generated by Django 4.2.7 on 2024-01-29 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_web', '0002_fooditem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='item_image',
            field=models.ImageField(upload_to='food_item_images/'),
        ),
    ]
