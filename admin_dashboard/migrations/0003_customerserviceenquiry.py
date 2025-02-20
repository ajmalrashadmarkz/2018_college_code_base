# Generated by Django 5.1.4 on 2025-02-20 07:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_dashboard', '0002_quoterequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerServiceEnquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('company', models.CharField(blank=True, max_length=200)),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('postal_code', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=20)),
                ('category', models.CharField(choices=[('general', 'General Inquiry'), ('technical', 'Technical Support'), ('billing', 'Billing Support'), ('product', 'Product Support')], max_length=50)),
                ('subject', models.CharField(max_length=200)),
                ('question', models.TextField()),
                ('attachment', models.FileField(blank=True, upload_to='customer_service_attachments/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'])])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('resolved', 'Resolved'), ('closed', 'Closed')], default='pending', max_length=20)),
            ],
            options={
                'verbose_name': 'Customer Service Enquiry',
                'verbose_name_plural': 'Customer Service Enquiries',
                'ordering': ['-created_at'],
            },
        ),
    ]
