from django import forms
from .models import NewsArticle,BlogPost,JobListing
# from django_summernote.fields import SummernoteWidget


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
            'featured_image',  # Include the featured_image field
            'date_published',
            'is_active',
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
        }
        labels = {
            'title': 'News Title',
            'short_description': 'Brief Summary',
            'full_content': 'Content',
            'category': 'News Category',
            'featured_image': 'News Icon',  # Label for the featured_image field
            'date_published': 'Publication Date',
            'is_active': 'Visible',
        }
        help_texts = {
            'title': 'Provide a concise and clear headline.',
            'short_description': 'Summarize the news article in a few sentences.',
            'full_content': 'Include detailed content, images, and videos if applicable.',
            'category': 'Select the appropriate category for the news.',
            'featured_image': 'Upload an image to represent the news article.',  # Help text for the featured_image field
            'date_published': 'Set the date and time of publication.',
            'is_active': 'Tick this box to make the article visible on the website.',
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
            'featured_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
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


class JobListingForm(forms.ModelForm):
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
