# Generated by Django 4.2.3 on 2023-09-06 08:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cuci_mobil', '0040_remove_customer_customer_groups_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='deskripsi',
        ),
    ]
