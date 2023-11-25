import re

import requests
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DeleteView

from .forms import LoginForm, RegisterForm
from .models import UserSiteModel

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}


def proxy_url(request, user_path=None):
    full_path = request.get_full_path()

    # Create url for request
    if full_path.startswith('/user-site-name'):
        site_name = full_path.split('/')[2]
        url_path = full_path.removeprefix('/user-site-name/')
        url = f'https://{url_path}'
    else:
        # Try load link from referer
        if 'referer' in request.headers:
            site_name = request.headers.get('referer').split('user-site-name')[1].split('/')[1]
            url_path = full_path.removeprefix('/')
            url = f'https://{site_name}/{url_path}'
        else:
            raise ValueError(f"Invalid path {full_path}")

    # Handle cors
    if request.headers.get('Sec-Fetch-Mode') == 'cors':
        fixed_headers = dict(request.headers.items())
        fixed_headers = {
            k: v.replace('http://127.0.0.1:8000', f'https://{site_name}') if 'http://127.0.0.1:8000' in v else v
            for k, v in fixed_headers.items()
        }
        fixed_headers = {
            k: v.replace('http://localhost:8000', f'https://{site_name}') if 'http://localhost:8000' in v else v
            for k, v in fixed_headers.items()
        }
    else:
        fixed_headers = HEADERS

    # Do request
    res = requests.get(url, headers=fixed_headers, cookies=request.COOKIES)

    # Retry if error
    if res.status_code != 200:
        print(url[:100], res.status_code, res.text[:200])
        print('Trying again...', end='')
        res = requests.get(url, headers=HEADERS, cookies=request.COOKIES)
        if res.status_code != 200:
            # Ignore errors
            print('Error', url[:100], res.status_code, res.text[:200])
            print()
            print()
        else:
            print('Fixed')

    # Replace urls in response
    response = res.text

    def url_repl(matchobj):
        return f'http://localhost:8000/user-site-name/{matchobj.group(1)}/'

    response = re.sub(rf"https://(\w*\.?{site_name})/", url_repl, response)
    response = re.sub(r"href=\"/(?!/)", f'href="http://localhost:8000/user-site-name/{site_name}/', response)
    response = re.sub(r"src=[\"\']/(?!/)", f'src="http://localhost:8000/user-site-name/{site_name}/', response)

    # Add content type in response
    content_type = res.headers.get('Content-Type')

    # Return response
    return HttpResponse(response, content_type=content_type)


def repl_link(site, site_name):
    host = 'http://127.0.0.1:8000' + site_name
    print(host)
    pattern = re.compile(f'href=\"https?:(//)(www.)?{site_name}', re.VERBOSE)
    res = re.sub(pattern, host, site)

    return res


class UserSiteListView(ListView):
    model = UserSiteModel


#
# class UserSiteCreateView(LoginRequiredMixin, CreateView):
#     model = UserSiteModel
#     template_name = "vpnservice/site_form.html"
#     fields = [
#         'site_name',
#         'site_path',
#     ]
#
#     def get_context_data(self, **kwargs):
#         data = super().get_context_data(**kwargs)
#
#         if self.request.POST:
#             data['site_info'] = AddSiteInfoFormSet(self.request.POST)
#         else:
#             data['site_info'] = AddSiteInfoFormSet()
#
#         return data
#
#     def form_valid(self, parent_form):
#         context = self.get_context_data()
#         site_info_fs: AddSiteInfoFormSet = context['site_info']
#         new_parent = parent_form.save()
#
#         if site_info_fs.is_valid():
#             for instance in site_info_fs:
#                 if instance in site_info_fs.deleted_forms:
#                     continue
#                 site_info = instance.save(commit=False)
#                 site_info.schema = new_parent
#                 site_info.save()
#         else:
#             return self.form_invalid(parent_form)
#
#         return super().form_valid(parent_form)


# def add_user_info(request, pk):
#     pass
#
#
# def update_user_info(request, pk):
#     parent_obj = get_object_or_404(UserInfoModel, pk=pk)
#     if request.method == 'POST':
#         pass
#
#
# def site_info(request, pk):
#     pass
class SiteDeleteView(LoginRequiredMixin, DeleteView):
    model = UserSiteModel
    template_name = 'site_delete.html'

    def get_success_url(self):
        return reverse("home")


def home(request):
    return render(request, 'vpnservice/home.html')


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'registration/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='/')

        return render(request, self.template_name, {'form': form})


class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)
