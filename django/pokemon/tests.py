import unittest.mock

from django.test import TestCase
from django.urls import reverse

from pokemon.models import (
    Pokemon,
    PokemonType,
    PokemonColor,
    PokemonShape,
    PokemonHabitat,
    PokemonEggGroup
)

class PokemonTest(TestCase):
    def setUp(self):
        self.pokemon1 = Pokemon.objects.create(
            name='pokemon_1',
            sprite_url='example.com/sprite/1',
            index=1,
            flavour_texts=['Some text about pokemon 1'],
            color=self._get_or_create_color('blue'),
            shape=self._get_or_create_shape('squiggle'),
            habitat=self._get_or_create_habitat('sea'),
            is_legendary=True,
            is_mythical=False,
        )
        self.pokemon1.types.add(
            self._get_or_create_type('water'),
            self._get_or_create_type('flying')
        )
        self.pokemon1.egg_groups.add(
            self._get_or_create_egg_group('egg_group_1'),
            self._get_or_create_egg_group('egg_group_2')
        )
        self.pokemon2 = Pokemon.objects.create(
            name='pokemon_2',
            sprite_url='example.com/sprite/2',
            index=1,
            flavour_texts=['Some text about pokemon 2'],
            color=self._get_or_create_color('red'),
            shape=self._get_or_create_shape('circle'),
            habitat=self._get_or_create_habitat('cave'),
            is_legendary=False,
            is_mythical=True,
            evolves_from=self.pokemon1
        )
        self.pokemon2.types.add(
            self._get_or_create_type('water'),
            self._get_or_create_type('poison')
        )
        self.pokemon2.egg_groups.add(
            self._get_or_create_egg_group('egg_group_1'),
        )

    def _get_or_create_type(self, name):
        return PokemonType.objects.get_or_create(
            name=name,
            url='example.com/type/' + name
        )[0]

    def _get_or_create_color(self, name):
        return PokemonColor.objects.get_or_create(
            name=name,
            url='example.com/color/' + name
        )[0]

    def _get_or_create_shape(self, name):
        return PokemonShape.objects.get_or_create(
            name=name,
            url='example.com/shape/' + name
        )[0]

    def _get_or_create_habitat(self, name):
        return PokemonHabitat.objects.get_or_create(
            name=name,
            url='example.com/Habitat/' + name
        )[0]

    def _get_or_create_egg_group(self, name):
        return PokemonEggGroup.objects.get_or_create(
            name=name,
            url='example.com/egg_group/' + name
        )[0]

    def test_no_filter(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        pokemon_list = list(response.context['pokemon_list'])
        self.assertIn(self.pokemon1, pokemon_list)
        self.assertIn(self.pokemon2, pokemon_list)

    def test_filter_by_name(self):
        response = self.client.get(reverse('index'), data={'name': 'pokemon_1'})
        self.assertEqual(response.status_code, 200)
        pokemon_list = list(response.context['pokemon_list'])
        self.assertIn(self.pokemon1, pokemon_list)
        self.assertNotIn(self.pokemon2, pokemon_list)

    def test_filter_by_type(self):
        response = self.client.get(reverse('index'), data={'types': [
            self._get_or_create_type('water').pk
        ]})
        self.assertEqual(response.status_code, 200)
        pokemon_list = list(response.context['pokemon_list'])
        self.assertIn(self.pokemon1, pokemon_list)
        self.assertIn(self.pokemon2, pokemon_list)

        response = self.client.get(reverse('index'), data={'types': [
            self._get_or_create_type('water').pk,
            self._get_or_create_type('flying').pk,
        ]})
        self.assertEqual(response.status_code, 200)
        pokemon_list = list(response.context['pokemon_list'])
        self.assertIn(self.pokemon1, pokemon_list)
        self.assertNotIn(self.pokemon2, pokemon_list)

        response = self.client.get(reverse('index'), data={'types': [
            self._get_or_create_type('dark').pk
        ]})
        self.assertEqual(response.status_code, 200)
        pokemon_list = list(response.context['pokemon_list'])
        self.assertNotIn(self.pokemon1, pokemon_list)
        self.assertNotIn(self.pokemon2, pokemon_list)

    def test_filter_by_color(self):
        response = self.client.get(reverse('index'), data={'color': [
            self._get_or_create_color('red').pk
        ]})
        self.assertEqual(response.status_code, 200)
        pokemon_list = list(response.context['pokemon_list'])
        self.assertNotIn(self.pokemon1, pokemon_list)
        self.assertIn(self.pokemon2, pokemon_list)

    def test_filter_by_habitat(self):
        response = self.client.get(reverse('index'), data={'habitat': [
            self._get_or_create_habitat('cave').pk
        ]})
        self.assertEqual(response.status_code, 200)
        pokemon_list = list(response.context['pokemon_list'])
        self.assertNotIn(self.pokemon1, pokemon_list)
        self.assertIn(self.pokemon2, pokemon_list)

    def test_filter_by_egg_groups(self):
        response = self.client.get(reverse('index'), data={'egg_groups': [
            self._get_or_create_egg_group('egg_group_1').pk
        ]})
        self.assertEqual(response.status_code, 200)
        pokemon_list = list(response.context['pokemon_list'])
        self.assertIn(self.pokemon1, pokemon_list)
        self.assertIn(self.pokemon2, pokemon_list)

        response = self.client.get(reverse('index'), data={'egg_groups': [
            self._get_or_create_egg_group('egg_group_1').pk,
            self._get_or_create_egg_group('egg_group_2').pk
        ]})
        self.assertEqual(response.status_code, 200)
        pokemon_list = list(response.context['pokemon_list'])
        self.assertIn(self.pokemon1, pokemon_list)
        self.assertNotIn(self.pokemon2, pokemon_list)

    def test_filter_by_can_evolve(self):
        # Pokemon 1 can evolve, Pokemon 2 cannot
        response = self.client.get(reverse('index'), data={
            'can_evolve': 'true'
        })
        self.assertEqual(response.status_code, 200)
        pokemon_list = list(response.context['pokemon_list'])
        self.assertIn(self.pokemon1, pokemon_list)
        self.assertNotIn(self.pokemon2, pokemon_list)

        response = self.client.get(reverse('index'), data={
            'cant_evolve': 'true'
        })
        self.assertEqual(response.status_code, 200)
        pokemon_list = list(response.context['pokemon_list'])
        self.assertNotIn(self.pokemon1, pokemon_list)
        self.assertIn(self.pokemon2, pokemon_list)

    def test_filter_by_is_legendary(self):
        response = self.client.get(reverse('index'), data={
            'is_legendary': 'true'}
        )
        self.assertEqual(response.status_code, 200)
        pokemon_list = list(response.context['pokemon_list'])
        self.assertIn(self.pokemon1, pokemon_list)
        self.assertNotIn(self.pokemon2, pokemon_list)

    def test_filter_by_is_mythical(self):
        response = self.client.get(reverse('index'), data={
            'is_mythical': 'true'}
        )
        self.assertEqual(response.status_code, 200)
        pokemon_list = list(response.context['pokemon_list'])
        self.assertNotIn(self.pokemon1, pokemon_list)
        self.assertIn(self.pokemon2, pokemon_list)
