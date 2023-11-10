# Generated by Django 4.2.3 on 2023-08-29 03:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cuci_mobil', '0023_alter_customer_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='service',
            old_name='nama',
            new_name='kategori',
        ),
        migrations.AlterField(
            model_name='order',
            name='kategori_kendaraan',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='cuci_mobil.service'),
        ),
    ]
