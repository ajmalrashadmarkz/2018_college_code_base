# Generated by Django 5.1.4 on 2025-01-20 06:59

import admin_dashboard.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_dashboard', '0003_joblisting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsarticle',
            name='full_content',
            field=admin_dashboard.fields.CustomSummernoteTextField(blank=True, help_text='The body of the news article, which can include text, images, and videos.', null=True),
        ),
        migrations.AlterField(
            model_name='newsarticle',
            name='short_description',
            field=admin_dashboard.fields.CustomSummernoteTextField(blank=True, help_text='A brief summary of the news article.', null=True),
        ),
    ]
