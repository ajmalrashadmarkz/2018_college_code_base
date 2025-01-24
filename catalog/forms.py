from django import forms
from .models import Category
from django.core.exceptions import ValidationError


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'name', 'style', 'short_description', 'detailed_description', 
            'icon', 'banner', 'side_image', 'parent', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category name'}),
            'style': forms.Select(attrs={'class': 'form-control'}),
            'short_description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter short description'}),
            'detailed_description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter detailed description'}),
            'icon': forms.FileInput(attrs={'class': 'form-control'}), 
            'banner': forms.FileInput(attrs={'class': 'form-control'}), 
            'side_image': forms.FileInput(attrs={'class': 'form-control'}),  
            'parent': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
        labels = {
            'name': 'Category Name',
            'style': 'Display Style',
            'short_description': 'Short Description',
            'detailed_description': 'Detailed Description',
            'icon': 'Icon',
            'banner': 'Banner',
            'side_image': 'Side Image',
            'parent': 'Parent Category',
            'is_active': 'Active'
        }
        help_texts = {
            'name': 'Display name for the category',
            'style': 'Visual display style for the category',
            'short_description': 'Brief summary for search results or listings',
            'detailed_description': 'Comprehensive description for SEO and context',
            'icon': 'Icon representing the category',
            'banner': 'Large banner image at the top of the category page',
            'side_image': 'Side image for promoting sub-categories',
            'parent': 'Parent category for multi-level hierarchy',
            'is_active': 'Indicates if the category is currently active'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].required = True
        self.fields['icon'].required = True
        self.fields['short_description'].required = True

        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            elif not isinstance(field.widget, forms.SelectMultiple):
                field.widget.attrs.update({'class': 'form-control'})
            if self.errors.get(field_name):
                field.widget.attrs.update({'class': 'form-control is-invalid'})

        self.fields['parent'].queryset = Category.objects.filter(deleted_at__isnull=True)

    

#######################################################################################################
# 2024-12-18

from django import forms
from .models import Product, Category, ProductImage, ProductDocument
from django import forms
from django.core.exceptions import ValidationError
from .models import Product, Category, ProductImage, ProductDocument, ProductSpecification
import json

class ProductForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.filter(deleted_at__isnull=True),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control select2',
            'multiple': 'multiple'
        }),
        required=True,
        help_text='Select one or more categories for this product'
    )

    additional_images = forms.FileField(
        required=False,
        label='Additional Images',
        help_text='Select multiple images for the product gallery'
    )

    additional_documents = forms.FileField(
        required=False,
        label='Additional Documents',
        help_text='Select multiple documents for the product'
    )

    specifications = forms.JSONField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Product
        fields = [
            'name',
            'short_description',
            'detailed_description',
            'main_image',
            'quantity_in_stock',
            'categories',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter product name'}),
            'short_description': forms.TextInput(attrs={'placeholder': 'Enter short description'}),
            'detailed_description': forms.Textarea(attrs={'placeholder': 'Enter detailed description'}),
            'main_image': forms.FileInput(attrs={'class': 'form-control'}),
            'quantity_in_stock': forms.NumberInput(attrs={'placeholder': 'Enter stock quantity'}),
        }
        labels = {
            'name': 'Product Name',
            'short_description': 'Short Description',
            'detailed_description': 'Detailed Description',
            'main_image': 'Main Image',
            'quantity_in_stock': 'Quantity in Stock',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['short_description'].required = True
        self.fields['detailed_description'].required = True
        self.fields['main_image'].required = True

        # Add Bootstrap classes
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            elif not isinstance(field.widget, forms.SelectMultiple):
                field.widget.attrs.update({'class': 'form-control'})
            if self.errors.get(field_name):
                field.widget.attrs.update({'class': 'form-control is-invalid'})

        # Configure additional fields for multi-upload
        self.fields['additional_images'].widget.attrs.update({
            'class': 'form-control',
            'multiple': True,
            'accept': 'image/*'
        })
        self.fields['additional_documents'].widget.attrs.update({
            'class': 'form-control',
            'multiple': True,
            'accept': '.pdf,.doc,.docx,.txt,.xls,.xlsx,.csv,.ppt,.pptx'
        })

    def clean_specifications(self):
        specs = self.cleaned_data.get('specifications')
        if specs:
            if not isinstance(specs, dict):
                try:
                    specs = json.loads(specs)
                except json.JSONDecodeError:
                    raise ValidationError("Invalid specification format")

            for key, value in specs.items():
                if not isinstance(key, str) or not isinstance(value, str):
                    raise ValidationError("Specifications must be text")
                if not key.strip() or not value.strip():
                    raise ValidationError("Specification keys and values cannot be empty")

        return specs or {}

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

            specs_data = self.cleaned_data.get('specifications', {})
            if isinstance(specs_data, str):
                try:
                    specs_data = json.loads(specs_data)
                except json.JSONDecodeError:
                    specs_data = {}

            for heading, value in specs_data.items():
                if heading and value:
                    ProductSpecification.objects.create(
                        product=instance,
                        specification_title=heading.strip(),
                        specification=value.strip()
                    )

            instance.categories.clear()
            instance.categories.add(*self.cleaned_data['categories'])

            images = self.files.getlist('additional_images')
            for image in images:
                ProductImage.objects.create(product=instance, product_image=image)

            documents = self.files.getlist('additional_documents')
            for document in documents:
                ProductDocument.objects.create(
                    product=instance,
                    title=document.name.split('.')[0],
                    document=document
                )

        return instance
    

#########################################################################################################################
#################################################################################################################################

from django import forms
from .models import Product, ProductSpecification, Category
import json
from django.core.exceptions import ValidationError

class EditProductForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.filter(deleted_at__isnull=True),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control select2',
            'multiple': 'multiple'
        }),
        required=True
    )
    specifications = forms.JSONField(
        required=False,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = Product
        fields = [
            'name', 'short_description', 'detailed_description',
            'main_image', 'quantity_in_stock', 'categories'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'short_description': forms.TextInput(attrs={'class': 'form-control'}),
            'detailed_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'main_image': forms.FileInput(attrs={'class': 'form-control'}),
            'quantity_in_stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        
        if instance:
            # Get all specifications for this product
            specs = instance.specifications.all()
            if specs.exists():
                specs_dict = {
                    spec.specification_title: spec.specification
                    for spec in specs
                }
                self.initial['specifications'] = json.dumps(specs_dict)

    def clean_specifications(self):
        specs = self.cleaned_data.get('specifications')
        if not specs:
            return {}
            
        try:
            if isinstance(specs, str):
                specs = json.loads(specs)
            if not isinstance(specs, dict):
                raise ValidationError("Specifications must be a valid JSON object")
            return specs
        except json.JSONDecodeError:
            raise ValidationError("Invalid specification format")

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if commit:
            instance.save()
            self.save_m2m()  # Save many-to-many fields (categories)
            
            # Handle specifications
            specs_data = self.cleaned_data.get('specifications', {})
            if isinstance(specs_data, str):
                specs_data = json.loads(specs_data)
            
            # Delete specifications that are no longer present
            instance.specifications.exclude(
                specification_title__in=specs_data.keys()
            ).delete()
            
            # Update or create specifications
            for title, value in specs_data.items():
                ProductSpecification.objects.update_or_create(
                    product=instance,
                    specification_title=title,
                    defaults={'specification': value}
                )
        
        return instance











