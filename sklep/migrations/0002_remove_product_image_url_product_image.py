# Generated by Django 5.0.1 on 2024-01-24 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sklep', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image_url',
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default='', upload_to='product_images/'),
            preserve_default=False,
        ),
    ]
