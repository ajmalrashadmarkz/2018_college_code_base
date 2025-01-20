from django import forms
from .models import Submission, Choice

# class SurveyForm(forms.Form):
#     email = forms.EmailField()
#     question_1 = forms.ChoiceField(widget=forms.RadioSelect, choices=())

#     def __init__(self, survey, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.survey = survey
#         del self.fields["question_1"]
#         for question in survey.question_set.all():
#           choices = [(choice.id, choice.text) for choice in question.choice_set.all()]
#           self.fields[f"question_{question.id}"] = forms.ChoiceField(widget=forms.RadioSelect, choices=choices)
#           self.fields[f"question_{question.id}"].label = question.text

class SurveyForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'})
    )
    age = forms.IntegerField(
        required=True,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your age'})
    )
    place = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your place'})
    )

    def __init__(self, survey, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.survey = survey
        for question in survey.question_set.all():
            choices = [(choice.id, choice.text) for choice in question.choice_set.all()]
            self.fields[f"question_{question.id}"] = forms.ChoiceField(
                widget=forms.RadioSelect,
                choices=choices
            )
            self.fields[f"question_{question.id}"].label = question.text


from django import forms
from .models import Survey

class AdminSurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter survey title'
            }),
        }
        labels = {
            'title': 'Survey Title',
        }
        help_texts = {
            'title': 'Provide a descriptive title for your survey.',
        }


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = [
            'survey',
            'participant_email',
            'participant_name',
            'participant_phone',
            'participant_age',
            'participant_place',
            'answer',
            'status'
        ]
        widgets = {
            'survey': forms.Select(attrs={'class': 'form-control'}),
            'participant_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'participant_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}),
            'participant_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'participant_age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter age'}),
            'participant_place': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter place'}),
            'answer': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'status': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter status'})
        }
        labels = {
            'survey': 'Survey',
            'participant_email': 'Email',
            'participant_name': 'Name',
            'participant_phone': 'Phone',
            'participant_age': 'Age',
            'participant_place': 'Place',
            'answer': 'Answers',
            'status': 'Status'
        }
        help_texts = {
            'survey': 'Select the related survey',
            'participant_email': 'Enter participant email address',
            'participant_name': 'Enter participant full name',
            'participant_phone': 'Enter participant phone number (optional)',
            'participant_age': 'Enter participant age (optional)',
            'participant_place': 'Enter participant location (optional)',
            'answer': 'Select the answers given by the participant',
            'status': 'Current status of the submission'
        }
