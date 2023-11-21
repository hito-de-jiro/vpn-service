import pdb
import re

from django.http import HttpResponse, JsonResponse

import requests
from django.shortcuts import redirect

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}


def proxy_url(request, user_path=None):
    print(request.path, 111)
    print(user_path, 222)
    if request.path.startswith('/user-site-name'):
        url = f'https:/{user_path}'
        fixed_headers = HEADERS
    else:
        url = f'https://www.ukr.net/{request.path}'
        # pdb.set_trace()
        fixed_headers = request.headers
        fixed_headers['Referer'] = 'https://www.ukr.net/'

    # sess = requests.Session()
    # pdb.set_trace()
    res = requests.get(url, headers=fixed_headers)
    res.raise_for_status()
    # pdb.set_trace()

    # return HttpResponse(repl_link(res.text, user_path))
    return HttpResponse(res.text)


def repl_link(site, site_name):
    host = 'http://127.0.0.1:8000' + site_name
    print(host)
    pattern = re.compile(f'href=\"https?:(//)(www.)?{site_name}', re.VERBOSE)
    res = re.sub(pattern, host, site)

    return res
