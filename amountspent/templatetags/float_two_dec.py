from django import template
register = template.Library()
@register.filter
def float_two_dec(value):

    return "{:.2f}".format(float(value))