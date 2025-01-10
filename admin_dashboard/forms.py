from django import forms
from .models import NewsArticle,BlogPost,JobListing

class NewsArticleForm(forms.ModelForm):
    class Meta:
        model = NewsArticle
        fields = [
            'title',
            'short_description',
            'full_content',
            'category',
            'date_published',
            'is_active',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the title'}),
            'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter a short description'}),
            'full_content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Enter the full content'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'date_published': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'title': 'News Title',
            'short_description': 'Brief Summary',
            'full_content': 'Content',
            'category': 'News Category',
            'date_published': 'Publication Date',
            'is_active': 'Visible',
        }
        help_texts = {
            'title': 'Provide a concise and clear headline.',
            'short_description': 'Summarize the news article in a few sentences.',
            'full_content': 'Include detailed content, images, and videos if applicable.',
            'category': 'Select the appropriate category for the news.',
            'date_published': 'Set the date and time of publication.',
            'is_active': 'Tick this box to make the article visible on the website.',
        }


##############################################################################################

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = [
            'title',
            'short_description',
            'content',
            'category',
            'tags',
            'featured_image',
            #'author',
            'date_published',
            'is_active',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the blog title'}),
            'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter a short teaser'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Enter the full content'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter tags separated by commas'}),
            'featured_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            #'author': forms.Select(attrs={'class': 'form-control'}),
            'date_published': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'title': 'Post Title',
            'short_description': 'Teaser',
            'content': 'Blog Content',
            'category': 'Post Category',
            'tags': 'Tags',
            'featured_image': 'Featured Image',
            #'author': 'Author',
            'date_published': 'Publication Date',
            'is_active': 'Active',
        }
        help_texts = {
            'title': 'Provide a concise and catchy title for your blog post.',
            'short_description': 'Give readers a brief idea about the blog post.',
            'content': 'Write the full content of your blog post here.',
            'category': 'Select a category that best describes your post.',
            'tags': 'Separate tags with commas to help with search and organization.',
            'featured_image': 'Upload an image to represent your post.',
            #'author': 'Choose the author of this blog post.',
            'date_published': 'Specify when this post will be published.',
            'is_active': 'Check this to make the post visible on the site.',
        }


##################################################################################################


class JobListingForm(forms.ModelForm):
    class Meta:
        model = JobListing
        fields = [
            'job_title', 'department', 'job_location', 'job_description',
            'qualifications', 'application_link', 'application_instructions', 'active'
        ]
        widgets = {
        'title': forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter the blog title',
            'maxlength': 100
        }),
        'short_description': forms.Textarea(attrs={
            'class': 'form-control', 
            'rows': 3, 
            'placeholder': 'Enter a short teaser',
            'maxlength': 300
        }),
        'content': forms.Textarea(attrs={
            'class': 'form-control', 
            'rows': 10, 
            'placeholder': 'Enter the full content'
        }),
        'category': forms.Select(attrs={
            'class': 'form-control', 
            'data-placeholder': 'Choose a category'
        }),
        'tags': forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter tags separated by commas'
        }),
        'featured_image': forms.ClearableFileInput(attrs={
            'class': 'form-control', 
            'accept': 'image/*'
        }),
        'date_published': forms.DateTimeInput(attrs={
            'class': 'form-control', 
            'type': 'datetime-local',
            'placeholder': 'Select a date and time'
        }),
        'is_active': forms.CheckboxInput(attrs={
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
        cleaned_data = super().clean()
        job_title = cleaned_data.get('job_title')
        department = cleaned_data.get('department')
        job_location = cleaned_data.get('job_location')
        job_description = cleaned_data.get('job_description')
        qualifications = cleaned_data.get('qualifications')

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


        application_link = cleaned_data.get('application_link')
        application_instructions = cleaned_data.get('application_instructions')

        if not application_link and not application_instructions:
            self.add_error('application_link', 'Either application link or application instructions must be provided.')
            self.add_error('application_instructions', 'Either application link or application instructions must be provided.')