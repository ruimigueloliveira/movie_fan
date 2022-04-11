from django import forms

class myForms(forms.Form):
    username = forms.CharField()
    rental_time = forms.CharField()