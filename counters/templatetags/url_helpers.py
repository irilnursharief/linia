from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def relative_url(context, field_name, value):
    url_dict = context["request"].GET.copy()
    url_dict[field_name] = value
    return url_dict.urlencode()
