from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, inlineformset_factory, URLInput

from .models import UserInfoModel, UserSiteModel, SiteInfoModel


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100,
                                 required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name',
                                                               'class': 'form-control',
                                                               }))
    last_name = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name',
                                                              'class': 'form-control',
                                                              }))
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                           'class': 'form-control',
                                                           }))
    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                 'class': 'form-control',
                                                                 'data-toggle': 'password',
                                                                 'id': 'password',
                                                                 'name': 'password',
                                                                 }))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']


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
