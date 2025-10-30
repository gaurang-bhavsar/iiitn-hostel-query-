from django import template

register = template.Library()

@register.filter
def split(value, key):
    """
    Returns the string split by key
    """
    return value.split(key)

@register.filter
def selectattr(value, args):
    """
    Filter items by attribute value
    Usage: {{ items|selectattr:"status","equalto","P" }}
    """
    if not value:
        return []
        
    attr, comparison, target = args.split(',')
    
    if comparison == "equalto":
        return [item for item in value if getattr(item, attr.strip(), None) == target.strip()]
    
    return []
