from django.core.cache import cache
from django.conf import settings
import requests


class PokeAPI:
    BASE_URL = 'https://pokeapi.co/api/v2/'
    ALL = f'pokemon/?limit={settings.NUMBER_OF_POKEMON}'
    DETAIL = 'pokemon/'
    SPECIES = 'pokemon-species/'

    @classmethod
    def get(cls, url, *args, **kwargs):
        '''
        Utility function to make requests to the API and return empty dicts
        for non-200 responses. Valid responses are stored in a cache for
        15 mins so we don't have to make multiple repeat requests if the
        data being accessed isn't likely to change
        '''
        data = cache.get(url)
        if data:
            return data

        resp = requests.get(url)
        if resp.status_code == 200:
            if kwargs.get('raw'):
                data = resp.content
            else:
                data = resp.json()
            cache.set(url, data, 60 * 15)
            return data

        return {}

    @classmethod
    def get_pokemon_details(cls, id_or_name):
        '''
        Retrieves a pokemon's index, name, type combination, front sprite, and
        some flavour text using the base pokemon endpoint
        '''
        return PokeAPI.get(cls.BASE_URL + cls.DETAIL + str(id_or_name))

    @classmethod
    def get_pokemon_species(cls, pokemon_name):
        return PokeAPI.get(cls.BASE_URL + cls.SPECIES + '/' + pokemon_name)

    @classmethod
    def get_all_pokemon(cls):
        return PokeAPI.get(cls.BASE_URL + cls.ALL).get('results')

    @classmethod
    def get_pokemon_for_attribute(cls, endpoint, id):
        pokemon = PokeAPI.get(cls.BASE_URL + endpoint + '/' + id).get('pokemon')
        return [item['pokemon']['name'] for item in pokemon]

    @classmethod
    def get_attribute_values(cls, endpoint):
        return PokeAPI.get(cls.BASE_URL + endpoint).get('results')

    @classmethod
    def get_sprite(cls, pokemon):
        return PokeAPI.get(pokemon.sprite_url, raw=True)
