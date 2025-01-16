##############################################################################
#   2024-12-13 login 

from django.shortcuts import render, redirect

def login_page(request):
    return render(request,'login.html')

    ##############################################


"""
Secure Login View with Features:
- Multi-factor login attempt tracking
- Account lockout after 5 failed attempts
- 15-minute lockout duration
- Session timeout (15 minutes)
- Restricted to specific account types
- Prevents brute-force attacks
"""
from datetime import timedelta
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.utils.timezone import now
from django.conf import settings
from django.contrib.auth import get_user_model
import json
from django.utils import timezone  

User = get_user_model()

def account_login(request):
    SESSION_TIMEOUT = getattr(settings, 'SESSION_TIMEOUT', 900)  # Default 15 minutes
    MAX_LOGIN_ATTEMPTS = 5  # Maximum allowed login attempts
    LOCKOUT_DURATION = 15 * 60  # 15 minutes in seconds

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)

            # Handle previous day's login attempts
            if user.failed_attempts:
                failed_attempts = json.loads(user.failed_attempts)
                today = now().date()
                failed_attempts = [
                    attempt for attempt in failed_attempts
                    if timezone.datetime.strptime(attempt, '%Y-%m-%d').date() == today
                ]
                user.failed_attempts = json.dumps(failed_attempts)
                user.login_attempts = len(failed_attempts)
                user.save()

            # Check for lockout
            if user.is_locked_out and user.locked_out_until and user.locked_out_until > now():
                remaining_time = int((user.locked_out_until - now()).total_seconds())
                messages.error(request, f"Account is locked. Try again in {remaining_time // 60} minutes.")
                return render(request, 'login.html')

        except User.DoesNotExist:
            user = None

        # Authenticate the user
        authenticated_user = authenticate(request, email=email, password=password)

        if authenticated_user:
            authenticated_user.login_attempts = 0
            authenticated_user.is_locked_out = False
            authenticated_user.locked_out_until = None
            authenticated_user.failed_attempts = json.dumps([])

            if authenticated_user.account_type and authenticated_user.account_type.id == 1:
                authenticated_user.last_login_attempt = now()
                authenticated_user.save()

                auth_login(request, authenticated_user)
                request.session.set_expiry(SESSION_TIMEOUT)
                request.session['last_activity'] = now().timestamp()

                return redirect('admin_dashboard-dashboard')
            else:
                messages.error(request, "Access denied. Invalid account type.")
        else:
            try:
                user = User.objects.get(email=email)
                user.login_attempts += 1

                failed_attempts = json.loads(user.failed_attempts) if user.failed_attempts else []
                failed_attempts.append(str(now().date()))
                user.failed_attempts = json.dumps(failed_attempts)

                if user.login_attempts >= MAX_LOGIN_ATTEMPTS:
                    user.is_locked_out = True
                    user.locked_out_until = now() + timedelta(seconds=LOCKOUT_DURATION)
                    messages.error(request, f"Too many failed attempts. Account locked for {LOCKOUT_DURATION // 60} minutes.")
                else:
                    messages.error(request, "Invalid email or password.")

                user.save()
            except User.DoesNotExist:
                messages.error(request, "Invalid email or password.")

        return render(request, 'login.html')

    if request.user.is_authenticated:
        last_activity = request.session.get('last_activity')
        if last_activity and now().timestamp() - last_activity > SESSION_TIMEOUT:
            logout(request)
            messages.warning(request, "Session expired due to inactivity. Please log in again.")

    return render(request, 'login.html')



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









