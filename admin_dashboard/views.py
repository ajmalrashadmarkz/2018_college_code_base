from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import logout
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from catalog.models import Product,Category
from .models import NewsArticle,BlogPost,JobListing
from functools import wraps
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect
from django.utils.timezone import now
from django.contrib.auth import get_user_model

User = get_user_model() 

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'adminid' in request.session:
            try:
                user = User.objects.get(id=request.session['adminid'])
                if user.account_type and user.account_type.id == 1:
                    # Update last activity timestamp
                    request.session['last_activity'] = now().timestamp()
                    # Temporarily login this user for the duration of this request
                    auth_login(request, user)
                    return view_func(request, *args, **kwargs)
            except User.DoesNotExist:
                pass
        return redirect('account-login-page')
    return wrapper

from seo_dashboard.views import seo_manager_required

@login_required
@admin_required
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
    return render(request, 'admin_dashboard.html', context)

@admin_required
def dashboard_logout(request):
	logout(request)
	request.session.clear()
	return redirect('account-login-page')

###########################################################################################################
###########################################################################################################

from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import NewsArticle
from .forms import NewsArticleForm
from django.shortcuts import get_object_or_404

#@admin_required
@login_required
def news_article_list(request):
    queryset = NewsArticle.objects.filter(deleted_at__isnull=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        queryset = queryset.filter(
            Q(title__icontains=search_query) | 
            Q(short_description__icontains=search_query) |
            Q(full_content__icontains=search_query)
        )
    
    # Sorting functionality
    sort_by = request.GET.get('sort', 'date_published')
    order = request.GET.get('order', 'desc')
    
    valid_sort_fields = ['title', 'category', 'date_published']
    if sort_by not in valid_sort_fields:
        sort_by = 'date_published'
    
    if order == 'desc':
        queryset = queryset.order_by(f'-{sort_by}')
    else:
        queryset = queryset.order_by(sort_by)

    # Pagination
    page = request.GET.get('page', 1)
    per_page = 100
    paginator = Paginator(queryset, per_page)
    
    try:
        news_articles = paginator.page(page)
    except PageNotAnInteger:
        news_articles = paginator.page(1)
    except EmptyPage:
        news_articles = paginator.page(paginator.num_pages)
    
    context = {
        'news_articles': news_articles,
        'search_query': search_query,
        'sort_by': sort_by,
        'order': order,
        'total_articles': queryset.count(),
        'per_page': per_page
    }
    
    return render(request, 'news_article_list.html', context)

#@admin_required
@login_required
def news_article_details(request, pk):
    news_article = get_object_or_404(NewsArticle, pk=pk)
    return render(request, 'news_article_details.html', {'news_article': news_article })

#@admin_required
@login_required
def news_article_create(request):
    if request.method == 'POST':
        form = NewsArticleForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                news_article = form.save()
                messages.success(request, f'News Article "{news_article.title}" created successfully.')
                return redirect('admin_dashboard-news_article_list')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{form.fields[field].label}: {error}")
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
    else:
        form = NewsArticleForm()
    
    return render(request, 'news_article_form.html', {
        'form': form,
        'edit_mode': False,
    })

#@admin_required
@login_required
def news_article_edit(request, pk):
    news_article = get_object_or_404(NewsArticle, pk=pk)
    
    if request.method == 'POST':
        form = NewsArticleForm(request.POST, request.FILES, instance=news_article)
        try:
            if form.is_valid():
                updated_article = form.save()
                messages.success(request, f'News article "{updated_article.title}" updated successfully')
                return redirect('admin_dashboard-news_article_list')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{form.fields[field].label}: {error}")
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
    else:
        form = NewsArticleForm(instance=news_article)
    
    return render(request, 'news_article_form.html', {
        'form': form,
        'news_article': news_article,
        'edit_mode': True
    })


from django.utils import timezone
from django.http import JsonResponse

#@admin_required
@login_required
def news_article_delete(request, pk):
    news_article = get_object_or_404(NewsArticle, pk=pk)

    if request.method == 'POST':
        try:
            # Soft delete logic
            news_article.deleted_at = timezone.now()
            news_article.is_active = False
            news_article.save()

            response_data = {
                'success': True, 
                'message': f'News article "{news_article.title}" deleted successfully',
                'id': pk
            }

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse(response_data)

            messages.success(request, response_data['message'])
            return redirect('admin_dashboard-news_article_list')

        except Exception as e:
            response_data = {
                'success': False, 
                'error': str(e)
            }

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse(response_data, status=400)

            messages.error(request, str(e))
            return redirect('admin_dashboard-news_article_list')

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)







###########################################################################################################
###########################################################################################################

from .models import BlogPost
from .forms import BlogPostForm

#@admin_required
@login_required
def blog_post_list(request):
    queryset = BlogPost.objects.filter(deleted_at__isnull=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        queryset = queryset.filter(
            Q(title__icontains=search_query) | 
            Q(short_description__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(tags__icontains=search_query)
        )
    
    # Sorting functionality
    sort_by = request.GET.get('sort', 'date_published')
    order = request.GET.get('order', 'desc')
    
    valid_sort_fields = ['title', 'category', 'date_published']
    if sort_by not in valid_sort_fields:
        sort_by = 'date_published'
    
    if order == 'desc':
        queryset = queryset.order_by(f'-{sort_by}')
    else:
        queryset = queryset.order_by(sort_by)

    # Pagination
    page = request.GET.get('page', 1)
    per_page = 100
    paginator = Paginator(queryset, per_page)
    
    try:
        blog_posts = paginator.page(page)
    except PageNotAnInteger:
        blog_posts = paginator.page(1)
    except EmptyPage:
        blog_posts = paginator.page(paginator.num_pages)
    
    context = {
        'blog_posts': blog_posts,
        'search_query': search_query,
        'sort_by': sort_by,
        'order': order,
        'total_posts': queryset.count(),
        'per_page': per_page
    }
    
    return render(request, 'blog_post_list.html', context)


#@admin_required
@login_required
def blog_post_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                blog_post = form.save()
                messages.success(request, f'Blog Post "{blog_post.title}" created successfully.')
                return redirect('admin_dashboard-blog_post_list')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{form.fields[field].label}: {error}")
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
    else:
        form = BlogPostForm()
    
    return render(request, 'blog_post_form.html', {
        'form': form,
        'edit_mode': False,
    })

#@admin_required
@login_required
def blog_post_details(request, pk):
    blog_post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'blog_post_details.html', {'blog_post': blog_post})


from .models import BlogPost
from .forms import BlogPostForm

#@admin_required
@login_required
def blog_post_edit(request, pk):
    blog_post = get_object_or_404(BlogPost, pk=pk)

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=blog_post)
        try:
            if form.is_valid():
                updated_post = form.save()
                messages.success(request, f'Blog post "{updated_post.title}" updated successfully')
                return redirect('admin_dashboard-blog_post_list')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{form.fields[field].label}: {error}")
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
    else:
        form = BlogPostForm(instance=blog_post)

    return render(request, 'blog_post_form.html', {
        'form': form,
        'blog_post': blog_post,
        'edit_mode': True
    })

#@admin_required
@login_required
def blog_post_details(request, pk):
    blog_post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'blog_post_details.html', {'blog_post': blog_post })


#@admin_required
@login_required
def blog_post_delete(request, pk):
    blog_post = get_object_or_404(BlogPost, pk=pk)

    if request.method == 'POST':
        try:
            # Soft delete logic
            blog_post.deleted_at = timezone.now()
            blog_post.is_active = False
            blog_post.save()

            response_data = {
                'success': True, 
                'message': f'Blog post "{blog_post.title}" deleted successfully',
                'id': pk
            }

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse(response_data)

            messages.success(request, response_data['message'])
            return redirect('admin_dashboard-blog_post_list')

        except Exception as e:
            response_data = {
                'success': False, 
                'error': str(e)
            }

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse(response_data, status=400)

            messages.error(request, str(e))
            return redirect('admin_dashboard-blog_post_list')

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)


###########################################################################################################
###########################################################################################################



from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.utils import timezone
from django.contrib import messages
from .models import JobListing
from .forms import JobListingForm

#@admin_required
@login_required
def job_listing_list(request):
    queryset = JobListing.objects.filter(deleted_at__isnull=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        queryset = queryset.filter(
            Q(job_title__icontains=search_query) |
            Q(department__icontains=search_query) |
            Q(job_location__icontains=search_query) |
            Q(job_description__icontains=search_query)
        )
    
    # Sorting functionality
    sort_by = request.GET.get('sort', 'date_posted')
    order = request.GET.get('order', 'desc')
    
    valid_sort_fields = ['job_title', 'department', 'job_location', 'date_posted']
    if sort_by not in valid_sort_fields:
        sort_by = 'date_posted'
    
    if order == 'desc':
        queryset = queryset.order_by(f'-{sort_by}')
    else:
        queryset = queryset.order_by(sort_by)

    # Pagination
    page = request.GET.get('page', 1)
    per_page = 100
    paginator = Paginator(queryset, per_page)
    
    try:
        job_listings = paginator.page(page)
    except PageNotAnInteger:
        job_listings = paginator.page(1)
    except EmptyPage:
        job_listings = paginator.page(paginator.num_pages)
    
    context = {
        'job_listings': job_listings,
        'search_query': search_query,
        'sort_by': sort_by,
        'order': order,
        'total_listings': queryset.count(),
        'per_page': per_page,
    }
    
    return render(request, 'job_listing_list.html', context)

#@admin_required
@login_required
def job_listing_details(request, pk):
    job_listing = get_object_or_404(JobListing, pk=pk)
    return render(request, 'job_listing_details.html', {'job_listing': job_listing})


#@admin_required
@login_required
def job_listing_create(request):
    if request.method == 'POST':
        form = JobListingForm(request.POST)
        if form.is_valid():
            job_listing = form.save()
            messages.success(request, f'Job listing "{job_listing.job_title}" created successfully.')
            return redirect('admin_dashboard-job_listing_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field].label}: {error}")
    else:
        form = JobListingForm()
    
    return render(request, 'job_listing_form.html', {'form': form, 'edit_mode': False})

#@admin_required
@login_required
def job_listing_edit(request, pk):
    job_listing = get_object_or_404(JobListing, pk=pk)
    
    if request.method == 'POST':
        form = JobListingForm(request.POST, instance=job_listing)
        if form.is_valid():
            updated_listing = form.save()
            messages.success(request, f'Job listing "{updated_listing.job_title}" updated successfully.')
            return redirect('admin_dashboard-job_listing_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field].label}: {error}")
    else:
        form = JobListingForm(instance=job_listing)
    
    return render(request, 'job_listing_form.html', {'form': form, 'job_listing': job_listing, 'edit_mode': True})


#@admin_required
@login_required
def job_listing_delete(request, pk):
    job_listing = get_object_or_404(JobListing, pk=pk)
    
    if request.method == 'POST':
        try:
            job_listing.deleted_at = timezone.now()
            job_listing.active = False
            job_listing.save()
            response_data = {
                'success': True,
                'message': f'Job listing "{job_listing.job_title}" deleted successfully.',
                'id': pk
            }
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse(response_data)
            
            messages.success(request, response_data['message'])
            return redirect('admin_dashboard-job_listing_list')
        except Exception as e:
            response_data = {'success': False, 'error': str(e)}
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse(response_data, status=400)
            
            messages.error(request, str(e))
            return redirect('admin_dashboard-job_listing_list')
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)


#############################################################################################
#############################################################################################


from .models import Project
from .forms import ProjectForm

#@admin_required
@login_required
def project_list(request):
    queryset = Project.objects.filter(deleted_at__isnull=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        queryset = queryset.filter(
            Q(title__icontains=search_query) | 
            Q(short_description__icontains=search_query) |
            Q(content__icontains=search_query)
        )
    
    # Sorting functionality
    sort_by = request.GET.get('sort', 'created_at')
    order = request.GET.get('order', 'desc')
    
    valid_sort_fields = ['title', 'category', 'status', 'created_at']
    if sort_by not in valid_sort_fields:
        sort_by = 'created_at'
    
    queryset = queryset.order_by(f'-{sort_by}' if order == 'desc' else sort_by)
    
    # Pagination
    page = request.GET.get('page', 1)
    per_page = 100
    paginator = Paginator(queryset, per_page)
    
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)
    
    context = {
        'projects': projects,
        'search_query': search_query,
        'sort_by': sort_by,
        'order': order,
        'total_projects': queryset.count(),
        'per_page': per_page
    }
    
    return render(request, 'project_list.html', context)

#@admin_required
@login_required
def project_details(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'project_details.html', {'project': project})

#@admin_required
@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                project = form.save()
                messages.success(request, f'Project "{project.title}" created successfully.')
                return redirect('admin_dashboard-project_list')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{form.fields[field].label}: {error}")
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
    else:
        form = ProjectForm()
    
    return render(request, 'project_form.html', {
        'form': form,
        'edit_mode': False,
    })



#@admin_required
@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        try:
            if form.is_valid():
                updated_project = form.save()
                messages.success(request, f'Project "{updated_project.title}" updated successfully.')
                return redirect('admin_dashboard-project_list')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{form.fields[field].label}: {error}")
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
    else:
        form = ProjectForm(instance=project)
    
    return render(request, 'project_form.html', {
        'form': form,
        'project': project,
        'edit_mode': True,
    })

#@admin_required
@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        try:
            # Soft delete logic
            project.deleted_at = timezone.now()
            project.is_active = False
            project.save()
            
            response_data = {
                'success': True, 
                'message': f'Project "{project.title}" deleted successfully.',
                'id': pk
            }
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse(response_data)
            
            messages.success(request, response_data['message'])
            return redirect('admin_dashboard-project_list')
        except Exception as e:
            response_data = {
                'success': False, 
                'error': str(e)
            }
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse(response_data, status=400)
            
            messages.error(request, str(e))
            return redirect('admin_dashboard-project_list')
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)


######################################################################################


from .models import JobApplication, ContactSubmission, NewsletterSubscription

# Job Application Views
#@admin_required
@login_required
def job_application_list(request):
    queryset = JobApplication.objects.filter(deleted_at__isnull=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        queryset = queryset.filter(
            Q(full_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(position__icontains=search_query)
        )
    
    # Sorting functionality
    sort_by = request.GET.get('sort', 'created_at')
    order = request.GET.get('order', 'desc')
    
    valid_sort_fields = ['full_name', 'email', 'position', 'created_at', 'updated_at']
    if sort_by not in valid_sort_fields:
        sort_by = 'created_at'
    
    queryset = queryset.order_by(f'-{sort_by}' if order == 'desc' else sort_by)
    
    # Pagination
    page = request.GET.get('page', 1)
    per_page = 100
    paginator = Paginator(queryset, per_page)
    
    try:
        applications = paginator.page(page)
    except PageNotAnInteger:
        applications = paginator.page(1)
    except EmptyPage:
        applications = paginator.page(paginator.num_pages)
    
    context = {
        'applications': applications,
        'search_query': search_query,
        'sort_by': sort_by,
        'order': order,
        'total_applications': queryset.count(),
        'per_page': per_page
    }
    
    return render(request, 'job_application_list.html', context)

#@admin_required
@login_required
def job_application_details(request, pk):
    application = get_object_or_404(JobApplication, pk=pk, deleted_at__isnull=True)
    return render(request, 'job_application_details.html', {'application': application})

#@admin_required
@login_required
def job_application_delete(request, pk):
    application = get_object_or_404(JobApplication, pk=pk, deleted_at__isnull=True)
    
    if request.method == 'POST':
        try:
            # Soft delete
            application.deleted_at = timezone.now()
            application.save()
            
            response_data = {
                'success': True,
                'message': f'Application from "{application.full_name}" deleted successfully.',
                'id': pk
            }
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse(response_data)
            
            messages.success(request, response_data['message'])
            return redirect('admin_dashboard-job_application_list')
        except Exception as e:
            response_data = {
                'success': False,
                'error': str(e)
            }
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse(response_data, status=400)
            
            messages.error(request, str(e))
            return redirect('admin_dashboard-job_application_list')
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)


###################################################################################################


# Contact Submission Views
#@admin_required
@login_required
def contact_submission_list(request):
    queryset = ContactSubmission.objects.filter(deleted_at__isnull=True)
    
    search_query = request.GET.get('search', '')
    if search_query:
        queryset = queryset.filter(
            Q(full_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(message__icontains=search_query)
        )
    
    sort_by = request.GET.get('sort', 'created_at')
    order = request.GET.get('order', 'desc')
    
    valid_sort_fields = ['full_name', 'email', 'created_at', 'updated_at']
    if sort_by not in valid_sort_fields:
        sort_by = 'created_at'
    
    queryset = queryset.order_by(f'-{sort_by}' if order == 'desc' else sort_by)
    
    page = request.GET.get('page', 1)
    per_page = 100
    paginator = Paginator(queryset, per_page)
    
    try:
        submissions = paginator.page(page)
    except PageNotAnInteger:
        submissions = paginator.page(1)
    except EmptyPage:
        submissions = paginator.page(paginator.num_pages)
    
    context = {
        'submissions': submissions,
        'search_query': search_query,
        'sort_by': sort_by,
        'order': order,
        'total_submissions': queryset.count(),
        'per_page': per_page
    }
    
    return render(request, 'contact_submission_list.html', context)

#@admin_required
@login_required
def contact_submission_details(request, pk):
    submission = get_object_or_404(ContactSubmission, pk=pk, deleted_at__isnull=True)
    return render(request, 'contact_submission_details.html', {'submission': submission})

#@admin_required
@login_required
def contact_submission_delete(request, pk):
    submission = get_object_or_404(ContactSubmission, pk=pk, deleted_at__isnull=True)
    
    if request.method == 'POST':
        try:
            # Soft delete
            submission.deleted_at = timezone.now()
            submission.save()
            
            response_data = {
                'success': True,
                'message': f'Contact submission from "{submission.full_name}" deleted successfully.',
                'id': pk
            }
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse(response_data)
            
            messages.success(request, response_data['message'])
            return redirect('admin_dashboard-contact_submission_list')
        except Exception as e:
            response_data = {
                'success': False,
                'error': str(e)
            }
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse(response_data, status=400)
            
            messages.error(request, str(e))
            return redirect('admin_dashboard-contact_submission_list')
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

###################################################################################################

# Newsletter Subscription Views
#@admin_required
@login_required
def newsletter_subscription_list(request):
    queryset = NewsletterSubscription.objects.filter(deleted_at__isnull=True)
    
    search_query = request.GET.get('search', '')
    if search_query:
        queryset = queryset.filter(email__icontains=search_query)
    
    sort_by = request.GET.get('sort', 'created_at')
    order = request.GET.get('order', 'desc')
    
    valid_sort_fields = ['email', 'subscribed_at', 'created_at', 'updated_at', 'is_active']
    if sort_by not in valid_sort_fields:
        sort_by = 'created_at'
    
    queryset = queryset.order_by(f'-{sort_by}' if order == 'desc' else sort_by)
    
    page = request.GET.get('page', 1)
    per_page = 100
    paginator = Paginator(queryset, per_page)
    
    try:
        subscriptions = paginator.page(page)
    except PageNotAnInteger:
        subscriptions = paginator.page(1)
    except EmptyPage:
        subscriptions = paginator.page(paginator.num_pages)
    
    context = {
        'subscriptions': subscriptions,
        'search_query': search_query,
        'sort_by': sort_by,
        'order': order,
        'total_subscriptions': queryset.count(),
        'per_page': per_page
    }
    
    return render(request, 'newsletter_subscription_list.html', context)

#@admin_required
@login_required
def newsletter_subscription_delete(request, pk):
    subscription = get_object_or_404(NewsletterSubscription, pk=pk, deleted_at__isnull=True)
    
    if request.method == 'POST':
        try:
            # Soft delete
            subscription.deleted_at = timezone.now()
            subscription.is_active = False  # Additional state change for NewsletterSubscription
            subscription.save()
            
            response_data = {
                'success': True,
                'message': f'Newsletter subscription "{subscription.email}" deleted successfully.',
                'id': pk
            }
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse(response_data)
            
            messages.success(request, response_data['message'])
            return redirect('admin_dashboard-newsletter_subscription_list')
        except Exception as e:
            response_data = {
                'success': False,
                'error': str(e)
            }
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse(response_data, status=400)
            
            messages.error(request, str(e))
            return redirect('admin_dashboard-newsletter_subscription_list')
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

#@admin_required
@login_required
def newsletter_subscription_toggle_status(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        subscription_id = request.POST.get('subscription_id')
        
        try:
            subscription = get_object_or_404(NewsletterSubscription, pk=subscription_id, deleted_at__isnull=True)
            
            # Toggle the status
            subscription.is_active = not subscription.is_active
            subscription.save()
            
            response_data = {
                'success': True,
                'message': f'Subscription for "{subscription.email}" has been {"enabled" if subscription.is_active else "disabled"}.',
                'is_active': subscription.is_active
            }
            
            return JsonResponse(response_data)
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)