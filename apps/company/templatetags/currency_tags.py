from decimal import Decimal, InvalidOperation
from django import template

register = template.Library()

@register.filter
def currency_format(value, symbol='RD$'):
    """Formatea un valor con separadores de miles y dos decimales."""
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return f"{symbol} 0.00"

    if amount < 0:
        return f"-{symbol} {abs(amount):,.2f}"
    return f"{symbol} {amount:,.2f}"
