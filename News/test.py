"""

import random

chars = ["*","#","%","&","?","@"]
bw  = ["черт", "дурак"]
txt = 'Ты черт нарисовал чертеж?'.replace('  ', ' ').lower().split()
print(txt)

for word in txt:
    if word in bw:
        i = ''.join(random.sample(chars, len(word)))
        txt = [x.replace(word, i) for x in txt]

res = ' '.join(txt)
print(res)"""
text1 = "я твой дом редиска ел"
censor_list = ['редиска', 'ел']


"""def censor(t):
    txt = t.split()
    for i in range(len(txt)):
        if txt[i] in censor_list:
            txt[i] = ''.join("***")
    res = ' '.join(txt)
    return f'{res}'


c_text = censor(text1)

print(c_text)"""


def censor2(t):
    txt = t.split()
    for i in range(len(txt)):
        if txt[i] in censor_list:
            stars_num = '*'*len(txt[i])
            txt[i] = ''.join(stars_num)

    res = ' '.join(txt)
    return f'{res}'


c_text = censor2(text1)

print(c_text)