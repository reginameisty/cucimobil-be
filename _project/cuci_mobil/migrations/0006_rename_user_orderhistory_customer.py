# Generated by Django 4.2.3 on 2023-07-18 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cuci_mobil', '0005_orderhistory'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderhistory',
            old_name='user',
            new_name='customer',
        ),
    ]
