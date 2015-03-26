from django import forms

class validationForm(forms.Form):
    amt_id = forms.CharField()
    question1 = forms.CharField()
    question2 = forms.CharField()
    question3 = forms.CharField()
    question4 = forms.CharField()
    question5 = forms.CharField()
    question6 = forms.CharField()
    question7 = forms.CharField()
