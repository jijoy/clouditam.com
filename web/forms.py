from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

email_errors = {
    'required': 'Email is required',
}


class SignUpForm(forms.ModelForm):
    email = forms.EmailField(error_messages=email_errors)

    class Meta:
        model = get_user_model()
        exclude = []
        error_messages = {
                'username': {
                    'required': _("Username is required."),
                },
                 'password': {
                    'required': _("Password is required."),
                },
        }
        widgets = {
        'password': forms.PasswordInput(),
        }

class SignInForm(forms.Form):
    username_or_email = forms.CharField(max_length=512)
    passwrd = forms.CharField(max_length=32)
