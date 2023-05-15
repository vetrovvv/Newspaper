from django import template
from django.template.defaultfilters import stringfilter
register = template.Library()
from news.models import *
censor_list = []



with open ("../NewsPaper/censor_words.txt", "r") as censor_words:
    for line in censor_words:
        b = (line.strip())
        censor_list = b.split(",")
censor_words.close()


@register.filter
@stringfilter
def censor(value):

    value1 = value.lower()
    for word in censor_list:
        if word in value1:
            if word != "":
                value1 = value1.replace(word, "*" * len(word))
    list_of_value = list(value)
    uppercase_index_list = []
    for letter in list_of_value:
        if letter.isupper():
            uppercase_index_list.append(value.index(letter))
    uppercase_index_list_uniq = sorted(list(set(uppercase_index_list)))
    list_of_value1 = list(value1)
    for id, sym in enumerate(list_of_value1):
        if id in uppercase_index_list_uniq:
            list_of_value1[id] = sym.upper()
            value = "".join(list_of_value1)
    return value

@register.filter
def author(value):
    m = Author.objects.get(id = value)
    return m

@register.filter
def category_name(value):
    if '=' in value:
        part1,part2 = value.split('=')
        return Category.objects.get(id=part2)


