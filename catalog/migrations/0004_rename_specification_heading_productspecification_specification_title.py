# Generated by Django 5.1.4 on 2024-12-23 09:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_productdocument_deleted_at_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productspecification',
            old_name='specification_heading',
            new_name='specification_title',
        ),
    ]
