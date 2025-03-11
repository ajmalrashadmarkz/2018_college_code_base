from django.shortcuts import render,redirect
from django.utils import timezone
from admin_dashboard.models import BlogPost, JobListing, NewsArticle, Project
# from django.views.decorators.cache import cache_control
# Create your views here.

# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
def error_404(request, *args, **kwargs):
    return render(request, '404_robo.html', status=404)


def truncate_words(text, num_words):
    words = text.split()
    return ' '.join(words[:num_words])



def home_page(request):
    current_time = timezone.now()
    
    # Get latest active blog posts
    blog_posts = BlogPost.objects.filter(
        is_active=True,
        deleted_at__isnull=True,
        date_published__lte=current_time
    ).order_by('-date_published')[:3]
    
    # Process blog posts
    for post in blog_posts:
        post.short_description = truncate_words(post.short_description, 15)
    
    # Get latest active projects
    projects = Project.objects.filter(
        is_active=True,
        deleted_at__isnull=True
    ).order_by('-created_at')[:3]
    
    # Create context with both blog posts and projects
    context = {
        'page_title': 'Home Page',
        'blog_posts': blog_posts,
        'projects': projects
    }
    
    print("#############################HOME PAGE###################")
    return render(request, 'home.html', context)


######################################################################################################
######################################################################################################
######################################################################################################

from django.shortcuts import render, get_object_or_404
from catalog.models import Category, Product
from django.http import HttpResponseRedirect

def category_by_id(request, category_id):
    print("###############################--category_by_id--####################")

    category = get_object_or_404(Category, id=category_id)
    
    return redirect('user_account-category_view', category_slug=category.slug)


def get_banner(category):
    while category:
        if category.banner:
            return category.banner.url
        category = category.parent
    return None


def category_view(request, category_slug):
    print("###############################--category_view--####################")
    
    category = get_object_or_404(Category, slug=category_slug)
    subcategories = Category.objects.filter(parent=category, deleted_at__isnull=True)
    banner_url = get_banner(category)
    
    subcategory_count = subcategories.count()
    absolute_url = request.build_absolute_uri()

    if subcategory_count == 0:
        products = Product.objects.filter(categories=category, deleted_at__isnull=True)
        
        context = {
            'category': category,
            'subcategories': subcategories,
            'subcategory_count': subcategory_count,
            'products': products,
            'banner_url': banner_url,
            'absolute_url': absolute_url,
        }
        return redirect('user_account-product_list_view', category_slug=category.slug)

    
    context = {
        'category': category,
        'subcategories': subcategories,
        'banner_url': banner_url,
        'absolute_url': absolute_url,
    }
    print(context)
    return render(request, 'category_home_list.html', context)




#####################################################################################



def product_list_view(request, category_slug):
    print("###############################--product_list_view_--####################")
    category = get_object_or_404(Category, slug=category_slug)
    
    subcategories = Category.objects.filter(parent=category, deleted_at__isnull=True)
    banner_url = get_banner(category)
    subcategory_count = subcategories.count()
    
    
    products = None
    absolute_url = request.build_absolute_uri()
    
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
            'absolute_url': absolute_url,
            
        }
        return render(request, 'product_home_list.html', context)
        
    
    context = {
        'category': category,
        'subcategories': subcategories,
        'subcategory_count': subcategory_count,
        'products': products, 
        'absolute_url': absolute_url, 
    }
    print(context)
    return render(request, 'category_home_list.html', context)


#####################################################################################



def product_detail_view(request, category_slug, product_slug):
    # Get the category by slug
    category = get_object_or_404(Category, slug=category_slug)
    
    # Get the product by slug and ensure it belongs to the specified category
    product = get_object_or_404(
        Product.objects.select_related().prefetch_related(
            'categories',
            'images',
            'specifications',
            'documents'
        ),
        slug=product_slug,
        categories=category
    )

    # Handle documents
    documents_by_type = {}
    for doc in product.documents.all():
        doc_type = doc.document_type or 'Uncategorized'
        if doc_type not in documents_by_type:
            documents_by_type[doc_type] = []
        documents_by_type[doc_type].append(doc)

    # Prepare context
    context = {
        'product': product,
        'category': category,
        'documents_by_type': documents_by_type,
        'banner_url': "/media/banner_default_image/Hubnetix_default_Banner.JPG",
        'absolute_url': request.build_absolute_uri(),
    }

    return render(request, 'product_home_detail.html', context)


######################################################################################################
######################################################################################################
######################################################################################################




def about_page(request):
    projects = Project.objects.filter(
        is_active=True,
        deleted_at__isnull=True
    ).order_by('-created_at')  
    
    context = {
        'banner_url': "home_assets/media/abt-banner.jpg",
        'projects': projects
    }
    
    return render(request, 'about-us.html', context)


def contact_page(request):
    banner_url = "home_assets/media/contact_bg.jpg"  
    return render(request, 'contact_us.html', {'banner_url': banner_url})


def partners_page(request):
    banner_url = "home_assets/media/partner_bg.png"  
    return render(request, 'partners.html', {'banner_url': banner_url})

def support_page(request):
    banner_url = "home_assets/media/surrport.jpg"  
    return render(request, 'support.html', {'banner_url': banner_url})

def policy_page(request):
    banner_url = "home_assets/media/policy.png"  
    return render(request, 'policy.html', {'banner_url': banner_url})

def terms_page(request):
    banner_url = "home_assets/media/terms.png"  
    return render(request, 'terms.html', {'banner_url': banner_url})

def guide_page(request):
    banner_url = "home_assets/media/e-book-bg.png"  
    dummy_image = "home_assets/media/e-book-card.png"
    return render(request, 'e-book-detail.html', {'banner_url': banner_url, 'dummy_image': dummy_image})




######################################################################################################
######################################################################################################
######################################################################################################

def resources_page(request):
    banner_url = "home_assets/media/resources_bg.jpg"

    current_time = timezone.now()
    blog_posts = BlogPost.objects.filter(
        is_active=True,
        deleted_at__isnull=True,
        date_published__lte=current_time
    ).order_by('-date_published')

    for post in blog_posts:
        post.short_description = truncate_words(post.short_description, 20)
        
    return render(request, 'resources.html', {'banner_url': banner_url, 'blog_posts': blog_posts})


##########################################################

def careers_page(request):

    banner_url = "home_assets/media/career-bg.png"
    
    job_listings = JobListing.objects.filter(
        active=True,
        deleted_at__isnull=True
    ).order_by('-date_posted')
    
    context = {
        'banner_url': banner_url,
        'job_listings': job_listings
    }
    
    return render(request, 'career.html', context)


#######################################################



from django.utils import timezone
from django.utils.html import mark_safe
from itertools import chain

from django.utils.html import strip_tags
from django.utils.text import Truncator

def news_page(request):
    current_time = timezone.now()
    
    news_articles = list(NewsArticle.objects.filter(
        is_active=True,
        deleted_at__isnull=True,
        date_published__lte=current_time,
        is_event_news=False
    ).order_by('-date_published'))

    event_articles = list(NewsArticle.objects.filter(
        is_active=True,
        deleted_at__isnull=True,
        is_event_news=True,
        date_published__lte=current_time
    ).order_by('-date_published'))

    combined_articles = sorted(
        news_articles + event_articles, 
        key=lambda article: article.date_published, 
        reverse=True
    )

    
    for article in combined_articles:
        raw_text = strip_tags(article.short_description)  
        article.short_description = mark_safe(Truncator(raw_text).chars(300, truncate="..."))  # Trim to 100 chars

    return render(request, 'news.html', {
        'banner_url': "home_assets/media/news-bg.jpg",
        'news_articles': news_articles,
        'event_articles': event_articles,
        'total_articles': len(news_articles)
    })


#############################################################################################
from admin_dashboard.models import JobApplication
from admin_dashboard.forms import JobApplicationForm

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse


def submit_application(request):
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': 'Your application has been submitted successfully!'
                })
            messages.success(request, 'Your application has been submitted successfully!')
            return redirect('careers')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'errors': form.errors
                }, status=400)
            messages.error(request, 'Please correct the errors below.')
    else:
        form = JobApplicationForm()
    
    return render(request, 'careers.html', {'form': form})

###################################################################

from admin_dashboard.forms import ContactForm


def submit_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Thank you for contacting us! We will get back to you soon.'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'errors': form.errors
            }, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

###########################################################################################

from admin_dashboard.forms import NewsletterForm

def subscribe_newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Thank you for subscribing to our newsletter!'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'errors': form.errors
            }, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


################################################################################################

# def project_detail(request, pk):
#     project = get_object_or_404(Project, pk=pk, is_active=True, deleted_at__isnull=True)
    
#     context = {
#         'banner_url': "home_assets/media/abt-banner.jpg",
#         'project': project
#     }
    
#     return render(request, 'project_detail.html', context)

def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug, is_active=True, deleted_at__isnull=True)
    
    absolute_url = request.build_absolute_uri()

    context = {
        'banner_url': "home_assets/media/abt-banner.jpg",
        'project': project,
        'absolute_url': absolute_url
    }
    
    return render(request, 'project_detail.html', context)

################################################################################################



def blog_detail(request, slug):
    post = get_object_or_404(
        BlogPost,
        slug=slug,
        is_active=True,
        deleted_at__isnull=True,
        date_published__lte=timezone.now()
    )

    absolute_url = request.build_absolute_uri()

    context = {
        'post': post,
        'banner_url': "home_assets/media/resources_bg.jpg",
        'absolute_url': absolute_url
    }
    
    return render(request, 'blog_detail.html', context)


################################################################################################


def news_detail(request, slug):
    article = get_object_or_404(NewsArticle, slug=slug, is_active=True, deleted_at__isnull=True)
    
    absolute_url = request.build_absolute_uri()
    
    return render(request, 'news_detail.html', {
        'article': article,
        'absolute_url': absolute_url
    })


################################################################################################


from admin_dashboard.forms import QuoteRequestForm

def request_quote(request):
    if request.method == 'POST':
        form = QuoteRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Your request has been submitted successfully!'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'errors': form.errors
            }, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

############################################################################################

from admin_dashboard.forms import CustomerServiceForm

def submit_customer_enquiry(request):
    if request.method == 'POST':
        form = CustomerServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Your enquiry has been submitted successfully!'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'errors': form.errors
            }, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


############################################################################################

from admin_dashboard.forms import QuestionSubmissionForm


def submit_question(request):
    if request.method == 'POST':
        form = QuestionSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Your question has been submitted successfully!'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'errors': form.errors
            }, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


############################################################################################

from admin_dashboard.forms import PartnerApplicationForm

def partner_application(request):
    if request.method == 'POST':
        form = PartnerApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': 'Your application has been submitted successfully!'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)




#############################################################################################
#############################################################################################


from django.shortcuts import redirect, get_object_or_404
from seo_dashboard.models import OldUrlRedirect
from django.http import Http404  

def php_to_new_url_redirect(request, php_filename):
    print("#########################################")
    slug = php_filename.replace('.php', '')
    try:
        old_url_entry = get_object_or_404(OldUrlRedirect, old_slug=slug)
    except Http404:
        return redirect('home-page', permanent=True)
    
    if old_url_entry.url_type == 'category':
        return redirect('user_account-category_view', 
                        category_slug=old_url_entry.new_slug, 
                        permanent=True)
    elif old_url_entry.url_type == 'product':
        try:
            product = Product.objects.get(slug=old_url_entry.new_slug)
            category = product.categories.first()
            if category:
                return redirect('user_account-product_detail_view', 
                                category_slug=category.slug,
                                product_slug=old_url_entry.new_slug, 
                                permanent=True)
            else:
                return redirect('user_account-product_detail_view', 
                                category_slug='-', 
                                product_slug=old_url_entry.new_slug, 
                                permanent=True)
        except Product.DoesNotExist:
            return redirect('home-page', permanent=True)
    
    elif old_url_entry.url_type == 'news':
        return redirect('home-news_detail',
                        slug=old_url_entry.new_slug,
                        permanent=True)
    elif old_url_entry.url_type == 'blog':
        return redirect('home-blog_detail',
                        slug=old_url_entry.new_slug,
                        permanent=True)
    elif old_url_entry.url_type == 'projects':
        return redirect('home-project_detail',
                        slug=old_url_entry.new_slug,
                        permanent=True)
    else:
        return redirect('home-page')


