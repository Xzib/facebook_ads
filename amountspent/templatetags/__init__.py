from django import template

register = template.Library()


@register.filter
def float_twospace(value):
    return "{:.2f}".format(value)
