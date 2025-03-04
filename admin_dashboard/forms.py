from django import forms
from .models import NewsArticle,BlogPost,JobListing
#from django_summernote.fields import SummernoteWidget


# class NewsArticleForm(forms.ModelForm):
#     class Meta:
#         model = NewsArticle
#         fields = [
#             'title',
#             'short_description',
#             'full_content',
#             'category',
#             'date_published',
#             'is_active',
#         ]
#         widgets = {
#             'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the title'}),
#             #'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter a short description'}),
#             #'full_content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Enter the full content'}),
#             'short_description': SummernoteWidget(),
#             'full_content': SummernoteWidget(),
#             'category': forms.Select(attrs={'class': 'form-control'}),
#             'date_published': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
#             'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
#         }
#         labels = {
#             'title': 'News Title',
#             'short_description': 'Brief Summary',
#             'full_content': 'Content',
#             'category': 'News Category',
#             'date_published': 'Publication Date',
#             'is_active': 'Visible',
#         }
#         help_texts = {
#             'title': 'Provide a concise and clear headline.',
#             'short_description': 'Summarize the news article in a few sentences.',
#             'full_content': 'Include detailed content, images, and videos if applicable.',
#             'category': 'Select the appropriate category for the news.',
#             'date_published': 'Set the date and time of publication.',
#             'is_active': 'Tick this box to make the article visible on the website.',
#         }

from django import forms
from .models import NewsArticle
# from django_summernote.widgets import SummernoteWidget


class NewsArticleForm(forms.ModelForm):
    class Meta:
        model = NewsArticle
        fields = [
            'title',
            'short_description',
            'full_content',
            'category',
            'featured_image',
            'date_published',
            'is_active',
            'is_event_news',  
            'event_start_date',  
            'event_end_date',  
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the title'}),
            #'short_description': SummernoteWidget(),
            #'full_content': SummernoteWidget(),
            'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter a short description'}),
            'full_content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Enter the full content'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'featured_image': forms.FileInput(attrs={'class': 'form-control'}),
            'date_published': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_event_news': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'event_start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'event_end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            
        }

        labels = {
            'title': 'News Title',
            'short_description': 'Brief Summary',
            'full_content': 'Content',
            'category': 'News Category',
            'featured_image': 'News Icon',  
            'date_published': 'Publication Date',
            'is_active': 'Visible',
            'is_event_news': 'Event News',
            'event_start_date': 'Event Start Date',
            'event_end_date': 'Event End Date',
        }
        help_texts = {
            'title': 'Provide a concise and clear headline.',
            'short_description': 'Summarize the news article in a few sentences.',
            'full_content': 'Include detailed content, images, and videos if applicable.',
            'category': 'Select the appropriate category for the news.',
            'featured_image': 'Upload an image to represent the news article.',  # Help text for the featured_image field
            'date_published': 'Set the date and time of publication.',
            'is_active': 'Tick this box to make the article visible on the website.',
            'is_event_news': 'Check this box if the news is related to an event.',
            'event_start_date': 'Select the start date of the event.',
            'event_end_date': 'Select the end date of the event.',
        }




##############################################################################################

# class BlogPostForm(forms.ModelForm):
#     class Meta:
#         model = BlogPost
#         fields = [
#             'title',
#             'short_description',
#             'content',
#             'category',
#             'tags',
#             'featured_image',
#             #'author',
#             'date_published',
#             'is_active',
#         ]
#         widgets = {
#             'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the blog title'}),
#             # 'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter a short teaser'}),
#             # 'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Enter the full content'}),
#             'short_description': SummernoteWidget(),
#             'content': SummernoteWidget(),
#             'category': forms.Select(attrs={'class': 'form-control'}),
#             'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter tags separated by commas'}),
#             'featured_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
#             #'author': forms.Select(attrs={'class': 'form-control'}),
#             'date_published': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
#             'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
#         }
#         labels = {
#             'title': 'Post Title',
#             'short_description': 'Teaser',
#             'content': 'Blog Content',
#             'category': 'Post Category',
#             'tags': 'Tags',
#             'featured_image': 'Featured Image',
#             #'author': 'Author',
#             'date_published': 'Publication Date',
#             'is_active': 'Active',
#         }
#         help_texts = {
#             'title': 'Provide a concise and catchy title for your blog post.',
#             'short_description': 'Give readers a brief idea about the blog post.',
#             'content': 'Write the full content of your blog post here.',
#             'category': 'Select a category that best describes your post.',
#             'tags': 'Separate tags with commas to help with search and organization.',
#             'featured_image': 'Upload an image to represent your post.',
#             #'author': 'Choose the author of this blog post.',
#             'date_published': 'Specify when this post will be published.',
#             'is_active': 'Check this to make the post visible on the site.',
#         }

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = [
            'title',
            'author',  # Now it's a CharField
            'short_description',
            'content',
            'category',
            'tags',
            'featured_image',
            'date_published',
            'is_active',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the blog title'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter author name'}),  # TextInput for CharField
            #'short_description': SummernoteWidget(),
            #'content': SummernoteWidget(),
            'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter a short teaser'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Enter the full content'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter tags separated by commas'}),
            'featured_image': forms.ClearableFileInput(attrs={'class': 'form-control',  'required': True}),
            'date_published': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'title': 'Post Title',
            'author': 'Author',  # Label for 'author'
            'short_description': 'Teaser',
            'content': 'Blog Content',
            'category': 'Post Category',
            'tags': 'Tags',
            'featured_image': 'Featured Image',
            'date_published': 'Publication Date',
            'is_active': 'Active',
        }
        help_texts = {
            'title': 'Provide a concise and catchy title for your blog post.',
            'author': 'Enter the name of the author of this blog post.',
            'short_description': 'Give readers a brief idea about the blog post.',
            'content': 'Write the full content of your blog post here.',
            'category': 'Select a category that best describes your post.',
            'tags': 'Separate tags with commas to help with search and organization.',
            'featured_image': 'Upload an image to represent your post.',
            'date_published': 'Specify when this post will be published.',
            'is_active': 'Check this to make the post visible on the site.',
        }
##################################################################################################

from django import forms
from .models import JobListing

class JobListingForm(forms.ModelForm):
    class Meta:
        model = JobListing
        fields = [
            'job_title', 'department', 'job_location', 'job_description',
            'qualifications', 'application_link', 'application_instructions', 'active'
        ]
        widgets = {
            'job_title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter the job title',
                'maxlength': 255
            }),
            'department': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter the department',
                'maxlength': 255
            }),
            'job_location': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter the job location (e.g., Remote, New York Office)',
                'maxlength': 255
            }),
            #'job_description':SummernoteWidget(), 
            #'qualifications': SummernoteWidget(),
            'job_description':forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Enter the full job_description'}),
            'qualifications':forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Enter the qualifications'}),
            'application_link': forms.URLInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter the application link (if any)',
                'maxlength': 500
            }),
            'application_instructions': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 5, 
                'placeholder': 'Provide instructions on how to apply if no link is provided'
            }),
            'active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'job_title': 'Job Title',
            'department': 'Department',
            'job_location': 'Job Location',
            'job_description': 'Job Description',
            'qualifications': 'Qualifications',
            'application_link': 'Application Link',
            'application_instructions': 'Application Instructions',
            'active': 'Active',
        }

    def clean(self):
        """Custom validation logic for the JobListing form."""
        cleaned_data = super().clean()
        job_title = cleaned_data.get('job_title')
        department = cleaned_data.get('department')
        job_location = cleaned_data.get('job_location')
        job_description = cleaned_data.get('job_description')
        qualifications = cleaned_data.get('qualifications')

        # Validate required fields
        if not job_title:
            self.add_error('job_title', 'Job title is required.')
        if not department:
            self.add_error('department', 'Department is required.')
        if not job_location:
            self.add_error('job_location', 'Job location is required.')
        if not job_description:
            self.add_error('job_description', 'Job description is required.')
        if not qualifications:
            self.add_error('qualifications', 'Qualifications are required.')

        # Ensure either application_link or application_instructions is provided
        application_link = cleaned_data.get('application_link')
        application_instructions = cleaned_data.get('application_instructions')

        if not application_link and not application_instructions:
            error_message = 'Either application link or application instructions must be provided.'
            self.add_error('application_link', error_message)
            self.add_error('application_instructions', error_message)



##################################################################################################

from .models import JobApplication, ContactSubmission

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['full_name', 'email', 'phone', 'state', 'position', 'resume']
        
    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            if resume.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError("File size must be under 5MB")
        return resume
    
###############################################################################

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ['full_name', 'email', 'phone', 'message']

##################################################################################
# forms.py

from .models import NewsletterSubscription

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscription
        fields = ['email']
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if NewsletterSubscription.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already subscribed to our newsletter.")
        return email
    

##################################################################################



from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title',
            'short_description',
            'content',
            'category',
            'status',
            'featured_image',
            'is_active',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the project title'}),
            #'short_description': SummernoteWidget(),
            #'content': SummernoteWidget(),
            'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Provide a brief summary of the project'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Provide detailed information about the project'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'featured_image': forms.FileInput(attrs={'class': 'form-control',  'required': True}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'title': 'Project Title',
            'short_description': 'Short Description',
            'content': 'Project Content',
            'category': 'Project Category',
            'status': 'Project Status',
            'featured_image': 'Featured Image',
            'is_active': 'Active',
        }
        help_texts = {
            'title': 'The title of the project.',
            'short_description': 'A brief summary of the project.',
            'content': 'Detailed information about the project, its objectives, scope, and significance.',
            'category': 'The category the project falls under.',
            'status': 'The current state of the project.',
            'featured_image': 'An image that represents the project.',
            'is_active': 'Indicates if the project is visible on the website.',
        }


##################################################################################

from .models import QuoteRequest

# class QuoteRequestForm(forms.ModelForm):
#     class Meta:
#         model = QuoteRequest
#         fields = ['full_name', 'email', 'phone', 'message']

    # def clean_phone(self):
    #     phone = self.cleaned_data.get('phone')
    #     if not phone.isdigit():
    #         raise forms.ValidationError("Phone number should contain only digits.")
    #     if len(phone) < 7 or len(phone) > 15:
    #         raise forms.ValidationError("Enter a valid phone number.")
    #     return phone

class QuoteRequestForm(forms.ModelForm):
    product_name = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), required=False)
    
    class Meta:
        model = QuoteRequest
        fields = ['full_name', 'email', 'phone', 'message', 'product']
        widgets = {
            'product': forms.HiddenInput()
        }
    

##################################################################################

from .models import CustomerServiceEnquiry

class CustomerServiceForm(forms.ModelForm):
    class Meta:
        model = CustomerServiceEnquiry
        exclude = ['status', 'created_at', 'updated_at', 'deleted_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        required_fields = ['first_name','last_name','email', 'address', 'phone', 'city', 'postal_code', 'subject', 'question']
        for field in required_fields:
            self.fields[field].required = True

    # def clean_phone(self):
    #     phone = self.cleaned_data.get('phone')
    #     if not phone.isdigit():
    #         raise forms.ValidationError("Phone number should contain only digits.")
    #     if len(phone) < 7 or len(phone) > 15:
    #         raise forms.ValidationError("Enter a valid phone number.")
    #     return phone


##################################################################################

from .models import QuestionSubmission

class QuestionSubmissionForm(forms.ModelForm):
    class Meta:
        model = QuestionSubmission
        exclude = ['status', 'created_at', 'updated_at', 'deleted_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        required_fields = ['name', 'email', 'phone', 'country', 'product_name', 'question']
        for field in required_fields:
            self.fields[field].required = True

    # def clean_phone(self):
    #     phone = self.cleaned_data.get('phone')
    #     if not phone.isdigit():
    #         raise forms.ValidationError("Phone number should contain only digits.")
    #     if len(phone) < 7 or len(phone) > 15:
    #         raise forms.ValidationError("Enter a valid phone number.")
    #     return phone
    

##################################################################################

from django import forms
from .models import PartnerApplication

class PartnerApplicationForm(forms.ModelForm):
    class Meta:
        model = PartnerApplication
        fields = ['name', 'position', 'phone', 'company', 'email', 'country', 'message']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if PartnerApplication.objects.filter(email=email, deleted_at__isnull=True).exists():
            raise forms.ValidationError("This email has already submitted a partner application.")
        return email

    # def clean_phone(self):
    #     phone = self.cleaned_data.get('phone')
    #     if not phone.isdigit():
    #         raise forms.ValidationError("Phone number should contain only digits.")
    #     if len(phone) < 7 or len(phone) > 15:
    #         raise forms.ValidationError("Enter a valid phone number.")
    #     return phone



    




