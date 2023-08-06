import json

from django import template
from django.conf import settings

register = template.Library()

@register.filter(name='get')
def get(d, k):
    return d.get(k, None)

@register.filter(name='entity')
def entity(d, k):
    v = d.get(k, None) if d else None
    return v[0].get('value') if v and len(v) else None

@register.filter(name='duration')
def duration(seconds):
    if not seconds:
      return ''
    return '{} ms'.format(int(seconds * 1000))

@register.filter(name='json')
def json_dumps(data):
    return json.dumps(data)


@register.inclusion_tag('botshot/nav.html', takes_context=True)
def show_menu_items(context):
    return {
        "items": ADMIN_VIEWS + settings.BOT_CONFIG.get("ADMIN_VIEWS", []),
        "current_view": context['request'].resolver_match.view_name
    }


ADMIN_VIEWS = [
    {"name": "Dashboard", "view": "dashboard"},
    {"name": "Flows", "view": "flows"},
    {"name": "Messages", "view": "log"},
    {"name": "Tests", "view": "test"},
    {"name": "Recording", "view": "botshot-test-recording"},
]
