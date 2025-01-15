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
