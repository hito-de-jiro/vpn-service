from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, inlineformset_factory, URLInput

from .models import UserInfoModel, UserSiteModel, SiteInfoModel


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserInfoForm(ModelForm):
    class Meta:
        model = UserInfoModel
        fields = '__all__'
        widgets = {
            'user_name': TextInput(attrs={
                'class': 'user_name',
                'required': 'true',
            }),
            'user_mail': TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'required': 'true',
            }),
        }


class UserSiteForm(ModelForm):
    class Meta:
        model = UserSiteModel
        fields = '__all__'
        widgets = {
            'site_name': TextInput(attrs={
                'class': 'site_name',
                'required': 'true',
            }),
            'site_path': URLInput(attrs={
                'class': 'site_path',
                'required': 'true',
            }),
        }


AddSiteInfoFormSet = inlineformset_factory(
    UserInfoModel, UserSiteModel, form=UserInfoForm,
    extra=1, can_delete=True, can_delete_extra=True
)
