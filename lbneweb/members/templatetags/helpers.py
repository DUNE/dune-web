from django import template
register = template.Library()

# http://push.cx/2007/django-template-tag-for-dictionary-access
# {{ somedict|dictref:o.id }}
@register.filter
def dictref(h, key):
    return h[key]
