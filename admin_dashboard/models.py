from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# from .fields import CustomSummernoteTextField


class NewsArticle(models.Model):
    TITLE_MAX_LENGTH = 200
    CATEGORY_CHOICES = [
        ('product_launch', 'Product Launch'),
        ('industry_update', 'Industry Update'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=TITLE_MAX_LENGTH, verbose_name='Title', help_text='The headline or title of the news article.')
    short_description = models.TextField(blank=True, null=True, verbose_name='Short Description', help_text='A brief summary of the news article.')
    full_content = models.TextField(blank=True, null=True, verbose_name='Full Content', help_text='The body of the news article, which can include text, images, and videos.')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name='Category', help_text='Category or type of news.')
    is_event_news = models.BooleanField(default=False, verbose_name='Is Event News', help_text='If True, this news is related to an event.')
    event_start_date = models.DateTimeField(blank=True, null=True, verbose_name='Event Start Date', help_text='The start date of the event (required if this is an event news).')
    event_end_date = models.DateTimeField(blank=True, null=True, verbose_name='Event End Date', help_text='The end date of the event (required if this is an event news).')
    #short_description = CustomSummernoteTextField(blank=True, null=True, help_text='A brief summary of the news article.')
    #full_content = CustomSummernoteTextField(blank=True, null=True, help_text='The body of the news article, which can include text, images, and videos.')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name='Category', help_text='Category or type of news.')
    featured_image = models.ImageField(blank=True, null=True, upload_to='news_icons/',verbose_name='News Icon',help_text='The icon image representing the news article, shown as a thumbnail or preview image.')
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
        ('business_achievements', 'Business Achievements'),
        ('tech_news', 'Tech News'),
        ('how_to_guides', 'How-To Guides'),
        ('other', 'Other'),
    ]

    
    title = models.CharField(max_length=TITLE_MAX_LENGTH, verbose_name='Title', help_text='The headline of the blog post.')
    author = models.CharField(blank=True, null=True, max_length=255, verbose_name='Author', help_text='The name of the blog post author.')
    short_description = models.TextField(blank=True, null=True, verbose_name='Short Description', help_text='A teaser or brief description of the blog post.')
    content = models.TextField(blank=True, null=True, verbose_name='Content', help_text='The full content of the blog post, including text, images, videos, and other media.')
    #short_description = CustomSummernoteTextField(blank=True, null=True, verbose_name='Short Description', help_text='A teaser or brief description of the blog post.')
    #content = CustomSummernoteTextField(blank=True, null=True, verbose_name='Content', help_text='The full content of the blog post, including text, images, videos, and other media.')
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
    #job_description = CustomSummernoteTextField(help_text="Job role, responsibilities, and requirements", blank=True, null=True)
    #qualifications = CustomSummernoteTextField(help_text="Skills, experience, and education required", blank=True, null=True)
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
    
#################################################################################

from django.core.validators import FileExtensionValidator

class JobApplication(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    state = models.CharField(max_length=50)
    position = models.CharField(max_length=100)
    resume = models.FileField(
        upload_to='resumes/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])]
    )
    
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.full_name} - {self.position}"


class ContactSubmission(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Contact from {self.full_name} - {self.created_at.strftime('%Y-%m-%d')}"


class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Subscription: {self.email}"


############################################################################################
# models.py

class Project(models.Model): 
    TITLE_MAX_LENGTH = 200
    
    STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
    ]
    
    CATEGORY_CHOICES = [
        ('network_infrastructure', 'Network Infrastructure'),
        ('cybersecurity', 'Cybersecurity'),
        ('cloud_solutions', 'Cloud Solutions'),
        ('other', 'Other'),
    ]
    
    
    title = models.CharField(max_length=TITLE_MAX_LENGTH, verbose_name='Project Title', help_text='The title of the project.'); 
    short_description =models.TextField(blank=True, null=True, verbose_name='Short Description', help_text='A brief summary of the project.'); 
    content = models.TextField(blank=True, null=True, verbose_name='Content', help_text='Detailed information about the project, its objectives, scope, and significance.');

    #short_description = CustomSummernoteTextField(blank=True, null=True, verbose_name='Short Description', help_text='A brief summary of the project.'); 
    #content = CustomSummernoteTextField(blank=True, null=True, verbose_name='Content', help_text='Detailed information about the project, its objectives, scope, and significance.'); 
    category = models.CharField(blank=True, null=True, max_length=50, choices=CATEGORY_CHOICES, verbose_name='Project Category', help_text='The category the project falls under.'); 
    status = models.CharField(blank=True, null=True, max_length=20, choices=STATUS_CHOICES, default='ongoing', verbose_name='Project Status', help_text='The current state of the project.'); 
    featured_image = models.ImageField(upload_to='project_images/', blank=True, null=True, verbose_name='Featured Image', help_text='An image that represents the project.'); 

    is_active = models.BooleanField(default=True, verbose_name='Active', help_text='Indicates if the project is visible on the website.'); 
    
    created_at = models.DateTimeField(auto_now_add=True); 
    updated_at = models.DateTimeField(auto_now=True); 
    deleted_at = models.DateTimeField(null=True, blank=True); 
    

    def __str__(self): 
        return self.title; 
    class Meta: 
        verbose_name = 'Project'; 
        verbose_name_plural = 'Projects'; 
        ordering = ['-created_at']


##################################################################################################

class QuoteRequest(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return f"Quote Request from {self.full_name} - {self.created_at.strftime('%Y-%m-%d')}"

    class Meta:
        ordering = ['-created_at']


##################################################################################################

class CustomerServiceEnquiry(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'General Inquiry'),
        ('technical', 'Technical Support'),
        ('billing', 'Billing Support'),
        ('product', 'Product Support'),
    ]

    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    company = models.CharField(max_length=200, blank=True)
    
    # Contact Information
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    
    # Enquiry Details
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    subject = models.CharField(max_length=200)
    question = models.TextField()
    attachment = models.FileField(
        upload_to='customer_service_attachments/',
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'])]
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True); 
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('in_progress', 'In Progress'),
            ('resolved', 'Resolved'),
            ('closed', 'Closed'),
        ],
        default='pending'
    )

    class Meta:
        verbose_name = 'Customer Service Enquiry'
        verbose_name_plural = 'Customer Service Enquiries'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.subject}"



##################################################################################################


class QuestionSubmission(models.Model):
    # Personal Information
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    
    # Question Details
    product_name = models.CharField(max_length=200)  
    question = models.TextField()
    attachment = models.FileField(
        upload_to='question_attachments/',
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'])]
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True); 

    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('in_progress', 'In Progress'),
            ('answered', 'Answered'),
            ('closed', 'Closed'),
        ],
        default='pending'
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Question Submission'
        verbose_name_plural = 'Question Submissions'

    def __str__(self):
        return f"Question about {self.product_name} from {self.name} - {self.created_at.strftime('%Y-%m-%d')}"


##################################################################################################

from django.utils import timezone
from django.db import models

class PartnerApplication(models.Model):
    # Personal Information
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20)
    
    # Company Information
    company = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=100)
    
    # Application Details
    message = models.TextField()
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)  # Soft delete
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('new', 'New'),
            ('reviewing', 'Under Review'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='new'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Partner Application'
        verbose_name_plural = 'Partner Applications'

    def __str__(self):
        return f"Partner Application - {self.company} ({self.name})"







    
