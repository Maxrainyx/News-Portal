
from django import template


register = template.Library()

censor_list = ['редиска', 'заголовок']


@register.filter()
def censor(t):
    txt = t.split()
    for i in range(len(txt)):
        if txt[i] in censor_list:
            stars_num = '*'*len(txt[i])
            txt[i] = ''.join(stars_num)

    res = ' '.join(txt)
    return f'{res}'
