from django import template

register = template.Library()

MIN_FONT_SIZE = 0.9

@register.filter(name="fontsize")
def asFontSizeEm(num, max):
    if max > 1:
        percent = float(num - 1) / (max - 1)
        fontSize = MIN_FONT_SIZE + 0.6 * percent
        return toFontSize(fontSize)

    return toFontSize(MIN_FONT_SIZE)

def toFontSize(size):
    return str(size) + "em"