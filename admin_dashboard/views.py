from django.shortcuts import get_object_or_404, render, redirect
from .models import Survey, Submission
from .forms import SurveyForm
from django.contrib.auth import logout


# def index(request):
#     surveys = Survey.objects.all()
#     print(surveys)
#     return render(request, "index.html", {"surveys": surveys})


# views.py
def index(request):
    video_id = "GKAgpuJkBdk"  # Make sure this is being passed correctly
    surveys = Survey.objects.all()
    context = {
        "surveys": surveys,
        "video_id": video_id,
    }
    print("Video ID:", video_id)  # Add this debug line
    return render(request, "index.html", context)

def thank_you(request):
    return render(request, 'thank_you.html')



# def show_survey(request, id=None):
#     print("#############show_survey########################")
#     survey = get_object_or_404(Survey, pk=id)
    
#     if request.method == 'POST':
#         form = SurveyForm(survey, request.POST)
#         if form.is_valid():
#             submission = Submission.objects.create(
#                 survey=survey,
#                 participant_email=form.cleaned_data['email']
#             )
            
#             for field_name, choice_id in form.cleaned_data.items():
#                 if field_name.startswith('question_'):
#                     submission.answer.add(choice_id)
            
#             return redirect('thank_you') 
#     else:
#         form = SurveyForm(survey)
    
#     context = {
#         "survey": survey,
#         "form": form,
#     }
#     return render(request, "survey.html", context)

def show_survey(request, id=None):
    print("#############show_survey########################")
    survey = get_object_or_404(Survey, pk=id)
    
    if request.method == 'POST':
        form = SurveyForm(survey, request.POST)
        if form.is_valid():
            submission = Submission.objects.create(
                survey=survey,
                participant_email=form.cleaned_data['email'],
                participant_name=form.cleaned_data['name'],
                participant_phone=form.cleaned_data['phone'],
                participant_age=form.cleaned_data['age'],
                participant_place=form.cleaned_data['place']
            )
            
            for field_name, choice_id in form.cleaned_data.items():
                if field_name.startswith('question_'):
                    submission.answer.add(choice_id)
            
            return redirect('thank_you')
    else:
        form = SurveyForm(survey)
    
    context = {
        "survey": survey,
        "form": form,
    }
    return render(request, "survey.html", context)




#################################################################################

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