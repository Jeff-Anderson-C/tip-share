from django import forms

class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=45)
    last_name = forms.CharField(max_length=45)
    email = forms.EmailField()
    password = forms.CharField(max_length=45, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=45, widget=forms.PasswordInput)

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=45, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=45, widget=forms.PasswordInput)