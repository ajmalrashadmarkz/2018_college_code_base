from django.shortcuts import render
from functools import wraps
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect
from django.utils.timezone import now
from django.contrib.auth import get_user_model

User = get_user_model() 

# Create your views here.
def seo_manager_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'seomanagerid' in request.session:
            try:
                user = User.objects.get(id=request.session['seomanagerid'])
                if user.account_type and user.account_type.id == 2:
                    # Update last activity timestamp
                    request.session['last_activity'] = now().timestamp()
                    # Temporarily login this user for the duration of this request
                    auth_login(request, user)
                    return view_func(request, *args, **kwargs)
            except User.DoesNotExist:
                pass
        return redirect('account-login-page')
    return wrapper


###########################################################################

from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import logout
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from catalog.models import Product,Category
from admin_dashboard.models import NewsArticle,BlogPost,JobListing




@login_required
@seo_manager_required
def dashboard_view(request):
    total_categories = Category.objects.filter(deleted_at__isnull=True).count()
    total_products = Product.objects.filter(deleted_at__isnull=True).count()
    total_news = NewsArticle.objects.filter(deleted_at__isnull=True).count()
    total_blogs = BlogPost.objects.filter(deleted_at__isnull=True).count()
    total_jobs = JobListing.objects.filter(deleted_at__isnull=True).count()

    context = {
        'total_categories': total_categories,
        'total_products': total_products,
        'total_news': total_news,
        'total_blogs': total_blogs,
        'total_jobs': total_jobs,
    }
    return render(request, 'seo_dashboard.html', context)

@seo_manager_required
def dashboard_logout(request):
	logout(request)
	request.session.clear()
	return redirect('account-login-page')


#####################################################################################
#####################################################################################
#####################################################################################
#####################################################################################



from django.shortcuts import render, redirect, get_object_or_404
from .forms import CategoryForm
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import CategoryForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def category_list(request):
    queryset = Category.objects.filter(deleted_at__isnull=True)
    
    search_query = request.GET.get('search', '')
    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query) | 
            Q(slug__icontains=search_query)
        )
    
    sort_by = request.GET.get('sort', 'name')
    order = request.GET.get('order', 'asc')
    
    valid_sort_fields = ['name', 'created_at', 'style']
    if sort_by not in valid_sort_fields:
        sort_by = 'name'
    
    if order == 'desc':
        queryset = queryset.order_by(f'-{sort_by}')
    else:
        queryset = queryset.order_by(sort_by)

    page = request.GET.get('page', 1)
    per_page = 100
    paginator = Paginator(queryset, per_page)
    
    try:
        category_list = paginator.page(page)
    except PageNotAnInteger:
        category_list = paginator.page(1)
    except EmptyPage:
        category_list = paginator.page(paginator.num_pages)
    
    context = {
        'category_list': category_list,
        'search_query': search_query,
        'sort_by': sort_by,
        'order': order,
        'total_categories': queryset.count(),
        'per_page': per_page
    }
    
    return render(request, 'seo_category_list.html', context)



@login_required
def category_details(request, pk):
    category = get_object_or_404(Category, pk=pk)
    return render(request, 'seo_category_details.html', {'category': category})



@login_required
def category_edit(request, pk):

    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':

        form = CategoryForm(request.POST, request.FILES, instance=category)
        try:
            if form.is_valid():

                updated_category = form.save()
                messages.success(request, f'Category "{updated_category.name}" updated successfully')
                return redirect('seo_dashboard-category_list')
            else:

                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{form.fields[field].label}: {error}")
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
    else:

        form = CategoryForm(instance=category)

    return render(request, 'seo_category_form.html', {
        'form': form, 
        'category': category,  
        'edit_mode': True  
    })


#################################################################################################
#################################################################################################
#################################################################################################

from django.shortcuts import render, redirect
from django.contrib import messages
from catalog.models import ProductImage,ProductDocument,ProductSpecification
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import FileResponse



#####################################################################################################


@login_required
def product_list(request):
    queryset = Product.objects.filter(deleted_at__isnull=True)
    
    search_query = request.GET.get('search', '')
    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query) | 
            Q(slug__icontains=search_query) |
            Q(short_description__icontains=search_query)
        )
    

    category_filter = request.GET.get('category', '')
    if category_filter:
        queryset = queryset.filter(categories__id=category_filter)
    

    stock_filter = request.GET.get('stock', '')
    if stock_filter == 'in_stock':
        queryset = queryset.filter(quantity_in_stock__gt=0)
    elif stock_filter == 'out_of_stock':
        queryset = queryset.filter(quantity_in_stock=0)
    
    sort_by = request.GET.get('sort', 'name')
    order = request.GET.get('order', 'asc')

    valid_sort_fields = ['name', 'created_at', 'quantity_in_stock']
    if sort_by not in valid_sort_fields:
        sort_by = 'name'
    

    if order == 'desc':
        queryset = queryset.order_by(f'-{sort_by}')
    else:
        queryset = queryset.order_by(sort_by)
    
    page = request.GET.get('page', 1)
    per_page = 100  
    paginator = Paginator(queryset, per_page)
    
    try:
        product_list = paginator.page(page)
    except PageNotAnInteger:
        product_list = paginator.page(1)
    except EmptyPage:
        product_list = paginator.page(paginator.num_pages)
    
    categories = Category.objects.filter(deleted_at__isnull=True)
    
    context = {
        'product_list': product_list,
        'categories': categories,
        'search_query': search_query,
        'category_filter': category_filter,
        'stock_filter': stock_filter,
        'sort_by': sort_by,
        'order': order,
        'total_products': queryset.count(),
        'per_page': per_page
    }

    print(context)
    
    return render(request, 'seo_product_list.html', context)



####################################################

@login_required
def product_details(request, pk):
    product = get_object_or_404(Product.objects.prefetch_related('images'), pk=pk)
    return render(request, 'seo_product_details.html', {'product': product})







#####################################################################################################
########################################################################################################

from django.views.decorators.http import require_POST

@login_required
@require_POST
def delete_product_image(request, pk):
    try:
        product = get_object_or_404(Product, pk=pk, deleted_at__isnull=True)
        
        # Delete the physical file
        if product.main_image:
            product.main_image.delete(save=False)
        
        # Clear the field
        product.main_image = None
        product.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Image deleted successfully'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)




########################################################################################################################
########################################################################################################################
########################################################################################################################
# 2025-01-02


from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .forms import ProductForm, ProductImageFormSet

def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        # Initialize forms with POST data and files
        product_form = ProductForm(request.POST, request.FILES, instance=product)
        image_formset = ProductImageFormSet(request.POST, request.FILES, instance=product)
        
        # Print debug info
        if not image_formset.is_valid():
            print("Formset errors:", image_formset.errors)
            print("Management form data:", image_formset.management_form.data)
            
        if product_form.is_valid() and image_formset.is_valid():
            try:
                # Save the product first
                product = product_form.save()
                
                # Save only non-empty forms
                instances = image_formset.save(commit=False)
                for instance in instances:
                    # Only save if there's an image or if it's an existing record
                    if instance.pk or (hasattr(instance, 'product_image') and instance.product_image):
                        instance.product = product
                        instance.save()
                
                # Handle deletions
                for obj in image_formset.deleted_objects:
                    obj.delete()
                
                messages.success(request, 'Product updated successfully.')
                return redirect('seo_dashboard-products_list')
                
            except Exception as e:
                print(f"Error saving product: {str(e)}")
                messages.error(request, f'Error saving product: {str(e)}')
        else:
            # If validation fails, display error message
            messages.error(request, 'Please correct the errors below.')
            print("Product form errors:", product_form.errors)
            print("Image formset errors:", image_formset.errors)
    else:
        # GET request handling
        product_form = ProductForm(instance=product)
        image_formset = ProductImageFormSet(instance=product)
    
    context = {
        'product_form': product_form,
        'image_formset': image_formset,
        'product': product,
        'title': f'Edit Product: {product.name}'
    }
    
    return render(request, 'seo_product_edit_form.html', context)