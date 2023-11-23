# Generated by Django 4.2.3 on 2023-09-06 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuci_mobil', '0032_customer_is_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customer',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]
