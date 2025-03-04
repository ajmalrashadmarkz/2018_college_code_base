# Generated by Django 5.1.4 on 2025-02-24 09:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_dashboard', '0002_remove_quoterequest_product'),
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quoterequest',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.product'),
        ),
    ]
