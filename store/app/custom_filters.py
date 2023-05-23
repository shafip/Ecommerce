from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    css_class = ' '.join(value.field.widget.attrs.get('class', '').split() + [arg])
    return value.as_widget(attrs={'class': css_class})
@register.filter(name='add_clas')
def add_clas(value, arg):
    css_classes = value.field.widget.attrs.get('class', '').split()
    css_classes.append(arg)
    return value.as_widget(attrs={'class': ' '.join(css_classes)})