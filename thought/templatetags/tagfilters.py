from django import template

register = template.Library()

@register.filter(name="fontsize")
def asFontSizeEm(num, max):
    percent = float(num - 1) / (max - 1)
    fontSize = 0.9 + 0.6 * percent
    return str(fontSize) + "em"