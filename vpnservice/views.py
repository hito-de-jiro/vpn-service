import re
from sys import getsizeof

import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from .forms import LoginForm, RegisterForm, UpdateUserForm, UserSiteForm
from .models import UserSiteModel

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}
HOST = 'http://127.0.0.1:8000'


def proxy_url(request, pk=14):
    number_visits = 0
    full_path = request.get_full_path()
    site_name = full_path.split('/')[1]
    site_name, url = create_request(full_path, request, site_name)
    fixed_headers = handle_cors(request, site_name)
    # Do request
    res = requests.get(url, headers=fixed_headers, cookies=request.COOKIES)
    # Add data sent to db
    user_site = UserSiteModel(id=pk)
    old_data_sent = UserSiteModel.objects.get(id=pk).data_sent
    if user_site.data_sent is None:
        user_site.data_sent = count_data_traffic(request)
    else:
        user_site.data_sent = count_data_traffic(request) + old_data_sent
    # Retry if error
    res = retry_error(request, res, url)
    # Replace urls in response
    response = res.text

    def url_repl(match_obj):
        return f'{HOST}{match_obj.group(1)}/'

    response = correct_response(response, site_name, url_repl)
    # Add content type in response
    content_type = res.headers.get('Content-Type')
    # Add data load to db
    old_data_loaded = UserSiteModel.objects.get(id=pk).data_loaded
    if old_data_loaded is None:
        user_site.data_loaded = count_data_traffic(response)
    else:
        user_site.data_loaded = count_data_traffic(response) + old_data_loaded
    old_number_visits = UserSiteModel.objects.get(id=pk).number_visits

    user_site.number_visits = old_number_visits + 1

    user_site.save(update_fields=['data_sent', 'data_loaded', 'number_visits'])

    # Return response
    return HttpResponse(response, content_type=content_type)


def correct_response(response, site_name, url_repl):
    # correct URLs in response
    response = re.sub(rf"https://(\w*\.?{site_name})/", url_repl, response)
    response = re.sub(r"href=\"/(?!/)", f'href="{HOST}/{site_name}/', response)
    response = re.sub(r"src=[\"\']/(?!/)", f'src="{HOST}/{site_name}/', response)
    return response


def create_request(full_path, request, site_name):
    # Create url for request
    if full_path.startswith('/'):
        url_path = full_path.removeprefix(f'/{site_name}/')
        url = f'https://{url_path}'
    else:
        # Try load link from referer
        if 'referer' in request.headers:
            site_name = request.headers.get('referer').split(f'{site_name}')[1].split('/')[1]
            url_path = full_path.removeprefix('/')
            url = f'https://{site_name}/{url_path}'
        else:
            raise ValueError(f"Invalid path {full_path}")
    return site_name, url


def retry_error(request, res, url):
    # Retry if error
    if res.status_code != 200:
        print(url[:100], res.status_code, res.text[:200])
        print('Trying again...', end='')
        res = requests.get(url, headers=HEADERS, cookies=request.COOKIES)
        if res.status_code != 200:
            # Ignore errors
            print('Error', url[:100], res.status_code, res.text[:200])
        else:
            print('Fixed')
    return res


def handle_cors(request, site_name):
    # Handle cors
    if request.headers.get('Sec-Fetch-Mode') == 'cors':
        fixed_headers = dict(request.headers.items())

        fixed_headers = {
            k: v.replace(HOST, f'https://{site_name}') if HOST in v else v
            for k, v in fixed_headers.items()
        }

    else:
        fixed_headers = HEADERS
    return fixed_headers


def count_data_traffic(data) -> float:
    count_data = getsizeof(data)

    return count_data  # the value in KB is returned
    # return float("%.2f" % (count_data / 1024))   # the value in KB is returned


def count_num_follow_to_page():
    # TODO document why this method is empty
    pass


@login_required
def user_site_list(request, template_name='vpnservice/site_list.html'):
    site_info = UserSiteModel.objects.all()
    data = {'object_list': site_info}
    return render(request, template_name, data)


@login_required
def site_info_list(request, template_name='vpnservice/site_info.html'):
    site_info = UserSiteModel.objects.all()
    data = {'object_list': site_info}

    return render(request, template_name, data)


@login_required
def create_user_site(request):
    context = {}
    form = UserSiteForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('user-home')

    context['form'] = form

    return render(request, 'vpnservice/site_form.html', context)


@login_required
def site_delete(request, pk, template_name='vpnservice/site_delete.html'):
    book = get_object_or_404(UserSiteModel, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('user-home')
    return render(request, template_name, {'object': book})


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


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)

    return render(request, 'registration/profile.html', {'user_form': user_form})
