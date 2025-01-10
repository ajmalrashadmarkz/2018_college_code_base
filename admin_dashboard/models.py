from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class NewsArticle(models.Model):
    TITLE_MAX_LENGTH = 200
    CATEGORY_CHOICES = [
        ('product_launch', 'Product Launch'),
        ('industry_update', 'Industry Update'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=TITLE_MAX_LENGTH, verbose_name='Title', help_text='The headline or title of the news article.')
    short_description = models.TextField(verbose_name='Short Description', help_text='A brief summary of the news article.')
    full_content = models.TextField(verbose_name='Full Content', help_text='The body of the news article, which can include text, images, and videos.')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name='Category', help_text='Category or type of news.')
    date_published = models.DateTimeField(verbose_name='Date Published', help_text='The publication date of the news article.')
    is_active = models.BooleanField(default=True, verbose_name='Active', help_text='A boolean field to specify if the news is active (visible on the website).')

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'News Article'
        verbose_name_plural = 'News Articles'
        ordering = ['-date_published']




class BlogPost(models.Model):
    TITLE_MAX_LENGTH = 200
    CATEGORY_CHOICES = [
        ('tech_news', 'Tech News'),
        ('how_to_guides', 'How-To Guides'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=TITLE_MAX_LENGTH, verbose_name='Title', help_text='The headline of the blog post.')
    short_description = models.TextField(verbose_name='Short Description', help_text='A teaser or brief description of the blog post.')
    content = models.TextField(verbose_name='Content', help_text='The full content of the blog post, including text, images, videos, and other media.')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name='Category', help_text='The blog category to help organize posts.')
    tags = models.CharField(max_length=200, verbose_name='Tags', help_text='Keywords or phrases associated with the blog post.')
    featured_image = models.ImageField(upload_to='blog_images/', verbose_name='Featured Image', help_text='The image that will appear at the top of the blog post or as a thumbnail.')
    #author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author', help_text='The name of the blog post author.')
    date_published = models.DateTimeField(verbose_name='Date Published', help_text='The publication date of the blog post.')
    is_active = models.BooleanField(default=True, verbose_name='Active', help_text='A boolean field to indicate if the blog post is currently live.')

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
        ordering = ['-date_published']




class JobListing(models.Model):
    job_title = models.CharField(max_length=255, help_text="Job title")
    department = models.CharField(max_length=255, help_text="Department")
    job_location = models.CharField(max_length=255, help_text="Office location or remote")
    job_description = models.TextField(help_text="Job role, responsibilities, and requirements", blank=True, null=True)
    qualifications = models.TextField(help_text="Skills, experience, and education required", blank=True, null=True)
    application_link = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Link to apply for the job"
    )
    application_instructions = models.TextField(
        blank=True,
        null=True,
        help_text="How to submit an application if no link is provided"
    )
    active = models.BooleanField(default=True, help_text="Is the job listing active?")
    date_posted = models.DateField(auto_now_add=True, help_text="Date posted")

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.job_title





    
