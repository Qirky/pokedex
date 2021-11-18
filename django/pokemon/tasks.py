from django.conf import settings
from celery.utils.log import get_task_logger
from project.celery import app
from celery import Task

from pokemon.utils import PokeAPI
from pokemon.forms import PokemonCreateForm
from pokemon.models import (
    Pokemon,
    PokemonType,
    PokemonColor,
    PokemonShape,
    PokemonHabitat,
    PokemonEggGroup
)

logger = get_task_logger(__name__)

@app.task
def populate():
    logger.info("Populating DB from PokeAPI")

    # Dict of endpoint/model class
    attribute_models = {
        'type': PokemonType,
        'pokemon-color': PokemonColor,
        'pokemon-shape': PokemonShape,
        'pokemon-habitat': PokemonHabitat,
        'egg-group': PokemonEggGroup,
    }

    # Go through each attribute type and fetch the options and store in DB
    attributes = {}
    for endpoint, model_cls in attribute_models.items():
        attributes[endpoint] = {}
        results = PokeAPI.get_attribute_values(endpoint)
        for result in results:
            instance, created = model_cls.objects.get_or_create(
                name=result['name'],
                url=result['url']
            )
            # Keep attribute IDs in memory to populate pokemon data
            attributes[endpoint][instance.name] = instance

    # Go through and get all the pokemon
    processed = []
    for pokemon in PokeAPI.get_all_pokemon():
        create_pokemon_record(pokemon['name'], attributes, processed)

    logger.info("Finished 'populate' task")

def get_flavour_texts(entries, lang='en'):
    return [entry['flavor_text'] for entry in entries if entry['language']['name'] == lang]


def create_pokemon_record(name, attr, processed):
    if name not in processed:
        details = PokeAPI.get_pokemon_details(name)
        species = PokeAPI.get_pokemon_species(name)

        # If this pokemon evolves from another, check if it exists in the DB
        # If not, create that one first so we can create a relationship
        # We can't always assume 'evolves_from' index has already been processed

        evolves_from = species['evolves_from_species']
        if evolves_from:
            try:
                evolves_from = Pokemon.objects.get(name=evolves_from['name'])
            except Pokemon.DoesNotExist:
                evolves_from = create_pokemon_record(
                    evolves_from['name'], attr, processed
                )

        # We aren't interested in processing pokemon outside of the original 151
        index = details['id']
        if index > settings.NUMBER_OF_POKEMON:
            return

        instance = PokemonCreateForm(
            dict(
                name=details['name'],
                index=index,
                sprite_url=details['sprites']['front_default'],
                flavour_texts=get_flavour_texts(species['flavor_text_entries'], lang='en'),
                types=[attr['type'].get(t['type']['name']) for t in details['types']],
                color=attr['pokemon-color'].get(species['color']['name']),
                shape=attr['pokemon-shape'].get(species['shape']['name']),
                habitat=attr['pokemon-habitat'].get(species['habitat']['name']),
                egg_groups=[attr['egg-group'].get(egg['name']) for egg in species['egg_groups']],
                is_legendary=species['is_legendary'],
                is_mythical=species['is_mythical'],
                evolves_from=evolves_from,
            ),
            instance=Pokemon.objects.filter(index=index).first()
        )
        instance.save()
        processed.append(name)
        return instance
