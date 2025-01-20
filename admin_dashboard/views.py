from django.shortcuts import get_object_or_404, render, redirect
from .models import Survey, Submission
from .forms import AdminSurveyForm
from django.contrib.auth import logout

def dashboard_view(request):
    print("#####################################")
    total_providers = 2
    context = {
        'total_providers': total_providers, 
    }
    return render(request, 'admin_dashboard.html', context)

def dashboard_logout(request):
	logout(request)
	request.session.clear()
	return redirect('account-login-page')

#################################################################################

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.utils import timezone
from .models import Survey
from .forms import AdminSurveyForm

@login_required
def survey_list(request):
    queryset = Survey.objects.filter(deleted_at__isnull=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        queryset = queryset.filter(Q(title__icontains=search_query))
    
    # Sorting functionality
    sort_by = request.GET.get('sort', 'created_at')
    order = request.GET.get('order', 'desc')
    
    valid_sort_fields = ['title', 'created_at']
    if sort_by not in valid_sort_fields:
        sort_by = 'created_at'
    
    if order == 'desc':
        queryset = queryset.order_by(f'-{sort_by}')
    else:
        queryset = queryset.order_by(sort_by)

    # Pagination
    page = request.GET.get('page', 1)
    per_page = 10
    paginator = Paginator(queryset, per_page)
    
    try:
        surveys = paginator.page(page)
    except PageNotAnInteger:
        surveys = paginator.page(1)
    except EmptyPage:
        surveys = paginator.page(paginator.num_pages)
    
    context = {
        'surveys': surveys,
        'search_query': search_query,
        'sort_by': sort_by,
        'order': order,
        'total_surveys': queryset.count(),
        'per_page': per_page
    }
    
    return render(request, 'survey_list.html', context)

@login_required
def survey_details(request, pk):
    survey = get_object_or_404(Survey, pk=pk)
    return render(request, 'survey_details.html', {'survey': survey})

@login_required
def survey_create(request):
    if request.method == 'POST':
        form = AdminSurveyForm(request.POST)
        try:
            if form.is_valid():
                survey = form.save()
                messages.success(request, f'Survey "{survey.title}" created successfully.')
                return redirect('admin_dashboard-survey_list')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{form.fields[field].label}: {error}")
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
    else:
        form = AdminSurveyForm()
    
    return render(request, 'survey_form.html', {
        'form': form,
        'edit_mode': False,
    })

@login_required
def survey_edit(request, pk):
    survey = get_object_or_404(Survey, pk=pk)
    
    if request.method == 'POST':
        form = AdminSurveyForm(request.POST, instance=survey)
        try:
            if form.is_valid():
                updated_survey = form.save()
                messages.success(request, f'Survey "{updated_survey.title}" updated successfully')
                return redirect('admin_dashboard-survey_list')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{form.fields[field].label}: {error}")
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
    else:
        form = AdminSurveyForm(instance=survey)
    
    return render(request, 'survey_form.html', {
        'form': form,
        'survey': survey,
        'edit_mode': True
    })

@login_required
def survey_delete(request, pk):
    survey = get_object_or_404(Survey, pk=pk)

    if request.method == 'POST':
        try:
            # Soft delete logic
            survey.deleted_at = timezone.now()
            survey.save()

            response_data = {
                'success': True, 
                'message': f'Survey "{survey.title}" deleted successfully',
                'id': pk
            }

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse(response_data)

            messages.success(request, response_data['message'])
            return redirect('admin_dashboard-survey_list')

        except Exception as e:
            response_data = {
                'success': False, 
                'error': str(e)
            }

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse(response_data, status=400)

            messages.error(request, str(e))
            return redirect('admin_dashboard-survey_list')

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)




########################################################################################################
from .models import Submission
from .forms import SubmissionForm


@login_required
def submission_list(request):
    queryset = Submission.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        queryset = queryset.filter(
            Q(participant_email__icontains=search_query) |
            Q(participant_name__icontains=search_query) |
            Q(participant_place__icontains=search_query) |
            Q(status__icontains=search_query)
        )
    
    # Sorting functionality
    sort_by = request.GET.get('sort', 'participant_email')
    order = request.GET.get('order', 'desc')
    
    valid_sort_fields = ['participant_email', 'participant_name', 'status', 'participant_age']
    if sort_by not in valid_sort_fields:
        sort_by = 'participant_email'
    
    if order == 'desc':
        queryset = queryset.order_by(f'-{sort_by}')
    else:
        queryset = queryset.order_by(sort_by)

    # Pagination
    page = request.GET.get('page', 1)
    per_page = 10
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
    
    return render(request, 'submission_list.html', context)

@login_required
def submission_details(request, pk):
    submission = get_object_or_404(Submission, pk=pk)
    return render(request, 'submission_details.html', {'submission': submission})

@login_required
def submission_create(request):
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        try:
            if form.is_valid():
                submission = form.save()
                messages.success(request, f'Submission for {submission.participant_email} created successfully.')
                return redirect('admin_dashboard-submission_list')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{form.fields[field].label}: {error}")
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
    else:
        form = SubmissionForm()
    
    return render(request, 'submission_form.html', {
        'form': form,
        'edit_mode': False,
    })

@login_required
def submission_edit(request, pk):
    submission = get_object_or_404(Submission, pk=pk)
    
    if request.method == 'POST':
        form = SubmissionForm(request.POST, instance=submission)
        try:
            if form.is_valid():
                updated_submission = form.save()
                messages.success(request, f'Submission for {updated_submission.participant_email} updated successfully')
                return redirect('admin_dashboard-submission_list')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{form.fields[field].label}: {error}")
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
    else:
        form = SubmissionForm(instance=submission)
    
    return render(request, 'submission_form.html', {
        'form': form,
        'submission': submission,
        'edit_mode': True
    })

@login_required
def submission_delete(request, pk):
    submission = get_object_or_404(Submission, pk=pk)

    if request.method == 'POST':
        try:
            # Soft delete logic
            # submission.deleted_at = timezone.now()
            submission.delete()
            # submission.save()

            response_data = {
                'success': True,
                'message': f'Submission for {submission.participant_email} deleted successfully',
                'id': pk
            }

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse(response_data)

            messages.success(request, response_data['message'])
            return redirect('admin_dashboard-submission_list')

        except Exception as e:
            response_data = {
                'success': False,
                'error': str(e)
            }

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse(response_data, status=400)

            messages.error(request, str(e))
            return redirect('admin_dashboard-submission_list')

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)