from django import template
from ..utils import convert_currency

register = template.Library()

@register.filter
def convert_currency_filter(amount, currency):
    """Django template filter to convert currency dynamically."""
    return convert_currency(amount, currency)
