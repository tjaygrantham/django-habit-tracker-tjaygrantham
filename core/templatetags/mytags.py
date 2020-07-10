from django import template
from lemminflect import getInflection, getLemma
from datetime import datetime

register = template.Library()

@register.filter
def lemm(input, upos):
    lemma = getLemma(input, upos=upos)
    if len(lemma) > 0:
        return lemma[0]
    return input


@register.filter
def inflect(input, tag):
    inflection = getInflection(input, tag=tag)
    if len(inflection) > 0:
        return inflection[0]
    return input


@register.filter
def suffix(input):
    plural = inflect(input, tag="NNS")
    return plural.replace('s', '')

@register.filter
def sort_descending(input, field):
    return input.order_by(f'-{field}')

@register.filter
def highest(records):
    highest_record = None
    for record in records:
        if not highest_record or record.quantity > highest_record.quantity:
            highest_record = record
    return highest_record

@register.filter
def average(records):
    count = len(records)
    total = 0
    for record in records:
        total+=record.quantity
    return total/count

@register.filter
def toint(input):
    if input.is_integer():
        return int(input)
    return input

@register.filter
def weekly(records):
    now = datetime.today()
    week = [record for record in records if record.added.month == now.month and record.added.year == now.year and record.added.weekday() <= now.weekday()]
    return week