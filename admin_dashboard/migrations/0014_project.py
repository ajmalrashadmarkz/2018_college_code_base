# Generated by Django 5.1.4 on 2025-02-05 08:43

import admin_dashboard.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_dashboard', '0013_newslettersubscription'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='The title of the project.', max_length=200, verbose_name='Project Title')),
                ('short_description', admin_dashboard.fields.CustomSummernoteTextField(blank=True, help_text='A brief summary of the project.', null=True, verbose_name='Short Description')),
                ('content', admin_dashboard.fields.CustomSummernoteTextField(blank=True, help_text='Detailed information about the project, its objectives, scope, and significance.', null=True, verbose_name='Content')),
                ('category', models.CharField(choices=[('network_infrastructure', 'Network Infrastructure'), ('cybersecurity', 'Cybersecurity'), ('cloud_solutions', 'Cloud Solutions'), ('other', 'Other')], help_text='The category the project falls under.', max_length=50, verbose_name='Project Category')),
                ('status', models.CharField(choices=[('ongoing', 'Ongoing'), ('completed', 'Completed'), ('on_hold', 'On Hold')], default='ongoing', help_text='The current state of the project.', max_length=20, verbose_name='Project Status')),
                ('featured_image', models.ImageField(blank=True, help_text='An image that represents the project.', null=True, upload_to='project_images/', verbose_name='Featured Image')),
                ('is_active', models.BooleanField(default=True, help_text='Indicates if the project is visible on the website.', verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
                'ordering': ['-created_at'],
            },
        ),
    ]
