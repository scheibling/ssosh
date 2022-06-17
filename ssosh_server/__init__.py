from django import template
register = template.Library()

def geturi():
    return "Hello World"

register.filter('geturi', geturi)