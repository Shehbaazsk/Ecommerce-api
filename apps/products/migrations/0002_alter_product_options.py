# Generated by Django 5.0.2 on 2024-02-28 14:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['id'], 'verbose_name': 'product', 'verbose_name_plural': 'products'},
        ),
    ]
