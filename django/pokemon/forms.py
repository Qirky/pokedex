from django import forms
from django.conf import settings
from pokemon.models import Pokemon, PokemonType


class PokemonFilterForm(forms.ModelForm):
    can_evolve = forms.BooleanField()
    cant_evolve = forms.BooleanField(label="Can't evolve")

    check_fields = [
        'is_legendary',
        'is_mythical',
        'can_evolve',
        'cant_evolve'
    ]

    class Meta:
        model = Pokemon
        fields = [
            'name',
            'types',
            'color',
            'shape',
            'habitat',
            'egg_groups',
            'is_legendary',
            'is_mythical',
            'can_evolve',
            'cant_evolve'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Removes trailing colon from fieldname
        self.label_suffix = ''

        for field in self.fields:
            self.fields[field].required=False
            if field in self.check_fields:
                # Convenience to include 'true' in URL when checkbox ticked
                self.fields[field].widget.attrs['value'] = 'true'
                self.fields[field].widget.attrs['class'] = 'form-check-input'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control'

        # Used to make sure they can't be set at the same time
        self.fields['can_evolve'].widget.attrs['class'] += ' mutually-exclusive'
        self.fields['cant_evolve'].widget.attrs['class'] += ' mutually-exclusive'



class PokemonCreateForm(forms.ModelForm):
    class Meta:
        model = Pokemon
        fields = '__all__'

    def clean_index(self):
        index = self.cleaned_data['index']
        if index > settings.NUMBER_OF_POKEMON:
            raise forms.ValidationError('Invalid index')
        return index
