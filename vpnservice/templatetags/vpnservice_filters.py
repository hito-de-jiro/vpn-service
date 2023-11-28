from django import template

import re

register = template.Library()


@register.filter(name='url_repl')
def url_repl(value):
    value = re.sub(r"https?://((www.)?\.?)", '', value)

    return value


register.filter('url_repl', url_repl)
