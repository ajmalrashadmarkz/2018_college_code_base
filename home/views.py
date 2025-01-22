from django.shortcuts import render,redirect
# Create your views here.

# def home_page(request):
#     return render(request,'home.html')

def home_page(request):
    context = {'page_title': 'Home Page'}
    return render(request, 'home.html', context)


######################################################################################################
######################################################################################################
######################################################################################################

from django.shortcuts import render, get_object_or_404
from catalog.models import Category, Product
from django.http import HttpResponseRedirect

# def category_view(request, category_id):
#     category = get_object_or_404(Category, id=category_id)
    
#     # Fetch subcategories where the parent is the current category
#     subcategories = Category.objects.filter(parent=category, deleted_at__isnull=True)
#     parent_category = category.parent if category.parent else None
    

#     context = {
#         'category': category,
#         'subcategories': subcategories,  
#         'parent_category': parent_category
#     }
#     print(context)
#     return render(request, 'category_home_list.html', context)


def get_banner(category):
    while category:
        if category.banner:
            return category.banner.url
        category = category.parent
    return None


def category_view(request, category_id):
    print("###############################--category_view--####################")
    category = get_object_or_404(Category, id=category_id)
    
    subcategories = Category.objects.filter(parent=category, deleted_at__isnull=True)
    banner_url = get_banner(category)
    
    subcategory_count = subcategories.count()

    if subcategory_count == 0 and category_id > 5:
        products = Product.objects.filter(categories=category, deleted_at__isnull=True)
        
        context = {
            'category': category,
            'subcategories': subcategories,
            'subcategory_count': subcategory_count,
            'products': products,
            'banner_url': banner_url,
        }
        return redirect('user_account-product_list_view', category_id=category.id)

    context = {
        'category': category,
        'subcategories': subcategories,
        'banner_url': banner_url,
    }
    print(context)
    return render(request, 'category_home_list.html', context)



#####################################################################################



def product_list_view(request, category_id):
    print("###############################--product_list_view_--####################")
    category = get_object_or_404(Category, id=category_id)
    
    subcategories = Category.objects.filter(parent=category, deleted_at__isnull=True)
    banner_url = get_banner(category)
    subcategory_count = subcategories.count()
    
    
    products = None
    
    
    if subcategory_count == 0:
        products = Product.objects.filter(categories=category, deleted_at__isnull=True)
        products_count = products.count()
        
        context = {
            'category': category,
            'subcategories': subcategories,
            'subcategory_count': subcategory_count,
            'products': products,  
            'products_count':products_count,
            'banner_url': banner_url,
        }
        return render(request, 'product_home_list.html', context)
        
    
    context = {
        'category': category,
        'subcategories': subcategories,
        'subcategory_count': subcategory_count,
        'products': products,  
    }
    print(context)
    return render(request, 'category_home_list.html', context)


#####################################################################################

# def product_detail_view(request, product_id):
#     print("###############################--product_detail_view--####################")
#     print(product_id)
#     product = get_object_or_404(Product.objects.select_related(
#         ).prefetch_related(
#             'categories',
#             'images',
#             'specifications',
#             'documents'
#         ), pk=product_id)

#     documents_by_type = {}
#     for doc in product.documents.all():
#         if doc.document_type not in documents_by_type:
#             documents_by_type[doc.document_type] = []
#         documents_by_type[doc.document_type].append(doc)

#     banner_url = "/media/banner_default_image/Hubnetix_default_Banner.JPG"
    
#     context = {
#         'product': product,
#         'documents_by_type': documents_by_type,
#         'banner_url': banner_url,
#     }

#     return render(request, 'product_home_detail.html', context)
    # return render(request, 'product_details.html', context)



def product_detail_view(request, product_id):
    print("###############################--product_detail_view--####################")
    print(product_id)
    product = get_object_or_404(Product.objects.select_related().prefetch_related(
        'categories',
        'images',
        'specifications',
        'documents'
    ), pk=product_id)

    documents_by_type = {}
    for doc in product.documents.all():
        if doc.document_type not in documents_by_type:
            documents_by_type[doc.document_type] = []
        documents_by_type[doc.document_type].append(doc)

    banner_url = "/media/banner_default_image/Hubnetix_default_Banner.JPG"

    context = {
        'product': product,
        'documents_by_type': documents_by_type,
        'banner_url': banner_url,
        'images': product.images.all(),  
    }

    print(context)

    return render(request, 'product_home_detail.html', context)


######################################################################################################
######################################################################################################
######################################################################################################


def about_page(request):
    banner_url = "home_assets/media/abt-banner.jpg"  # Path relative to the static folder
    return render(request, 'about-us.html', {'banner_url': banner_url})


def resources_page(request):
    banner_url = "home_assets/media/resources_bg.jpg"  
    return render(request, 'resources.html', {'banner_url': banner_url})

def news_page(request):
    banner_url = "home_assets/media/news-bg.jpg"  
    return render(request, 'news.html', {'banner_url': banner_url})

def contact_page(request):
    banner_url = "home_assets/media/contact_bg.jpg"  
    return render(request, 'contact_us.html', {'banner_url': banner_url})

def careers_page(request):
    banner_url = "home_assets/media/career-bg.png" 
    return render(request, 'career.html', {'banner_url': banner_url})



