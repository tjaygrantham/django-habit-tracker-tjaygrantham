from django import forms
from .models import Habit, Record
from django.utils.text import slugify


class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = [
            'action',
            'lesser',
            'goal',
            'unit',
            'period',
        ]
        labels = {
            'action': 'I want to ',
            'lesser': '',
            'goal': '',
            'unit': '',
            'period': 'every ',
        }


    # Init some stuff
    def __init__(self, *args, **kwargs):
        # Set label suffix
        kwargs['label_suffix'] = ' '
        super(HabitForm, self).__init__(*args, **kwargs)
        # Add placeholders for each field
        placeholders = {
            'action': 'walk',
            'goal': 1,
            'unit': 'mile',
            'period': 'day',
        }
        for k,v in self.fields.items():
            if k != 'lesser':
                v.widget.attrs['placeholder'] = placeholders[k]


class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = [
            'quantity',
            'added'
        ]
        labels = {
            'quantity': 'I',
            'added': 'on'
        }


    def __init__(self, *args, **kwargs):
        kwargs['label_suffix'] = ' '
        super(RecordForm, self).__init__(*args, **kwargs)
        self.fields['quantity'].widget.attrs['placeholder'] = '1'