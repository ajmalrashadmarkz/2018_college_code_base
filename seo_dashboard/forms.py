from django import forms
from catalog.models import Category
from django.core.exceptions import ValidationError
#from django_summernote.fields import SummernoteWidget


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'name', 'slug', 'short_description', 'detailed_description',
            'meta_tags', 'meta_description', 'canonical_url',
            'icon', 'icon_alt', 'banner', 'banner_alt', 'side_image', 'side_image_alt'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category name'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter slug'}),
            'short_description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter short description'}),
            'detailed_description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter detailed description'}),
            'meta_tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter meta tags'}),
            'meta_description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter meta description'}),
            'canonical_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter canonical URL'}),
            'icon': forms.FileInput(attrs={'class': 'form-control'}),
            'icon_alt': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter icon alt text'}),
            'banner': forms.FileInput(attrs={'class': 'form-control'}),
            'banner_alt': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter banner alt text'}),
            'side_image': forms.FileInput(attrs={'class': 'form-control'}),
            'side_image_alt': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter side image alt text'}),
        }
        labels = {
            'name': 'Category Name',
            'slug': 'Slug',
            'short_description': 'Short Description',
            'detailed_description': 'Detailed Description',
            'meta_tags': 'Meta Tags',
            'meta_description': 'Meta Description',
            'canonical_url': 'Canonical URL',
            'icon': 'Icon',
            'icon_alt': 'Icon Alt Text',
            'banner': 'Banner',
            'banner_alt': 'Banner Alt Text',
            'side_image': 'Side Image',
            'side_image_alt': 'Side Image Alt Text',
        }
        help_texts = {
            'name': 'Display name for the category',
            'slug': 'URL-friendly version of the category name',
            'short_description': 'Brief summary for search results or listings',
            'detailed_description': 'Comprehensive description for SEO and context',
            'meta_tags': 'SEO-friendly tags for better visibility',
            'meta_description': 'Short description for search engine snippets',
            'canonical_url': 'Canonical URL to avoid duplicate content',
            'icon': 'Icon representing the category',
            'icon_alt': 'Alt text for the icon image',
            'banner': 'Large banner image at the top of the category page',
            'banner_alt': 'Alt text for the banner image',
            'side_image': 'Side image for promoting sub-categories',
            'side_image_alt': 'Alt text for the side image',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Required fields for SEO team
        self.fields['name'].required = True
        self.fields['slug'].required = True
        self.fields['short_description'].required = True
        self.fields['meta_description'].required = True

        # Add Bootstrap error styling if validation fails
        for field_name, field in self.fields.items():
            if self.errors.get(field_name):
                field.widget.attrs.update({'class': 'form-control is-invalid'})


#######################################################################################################
# 2024-12-18
from django import forms
from django.forms import inlineformset_factory, BaseInlineFormSet
from catalog.models import Product, ProductImage

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'slug', 'short_description', 'detailed_description',
            'main_image', 'main_image_alt', 'meta_tags', 'meta_description', 'canonical_url'
        ]

class ProductImageForm(forms.ModelForm):
    # Add this to make the field not required for new instances
    product_image = forms.ImageField(required=False)
    
    class Meta:
        model = ProductImage
        fields = ['product_image', 'alt_text']

# Custom formset that handles empty forms better
class BaseProductImageFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        # No validation needed for empty forms
        for form in self.forms:
            if not form.has_changed() and not form.instance.pk:
                for field in form.errors:
                    form.errors[field] = []

# Use our custom formset as the base
ProductImageFormSet = inlineformset_factory(
    Product, 
    ProductImage, 
    form=ProductImageForm, 
    formset=BaseProductImageFormSet,  # Use our custom formset
    extra=0,
    can_delete=False
)













