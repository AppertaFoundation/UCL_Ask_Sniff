""" custom template tags/filters to be used in template """
from django import template
register = template.Library()

@register.filter(name='sub')
def sub(value, arg):
    """ function used in template to subtract 2 values """
    return value - arg
