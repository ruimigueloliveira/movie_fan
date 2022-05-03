from django import forms

class myRentalForms(forms.Form):
    # username = forms.CharField()
    rental_time = forms.CharField()

class mySignUpForms(forms.Form):
    username = forms.CharField()
    email = forms.CharField()
    password = forms.CharField()


