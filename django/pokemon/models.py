import random
from django.db import models

class Pokemon(models.Model):
    name = models.CharField(max_length=255)
    index = models.PositiveIntegerField()
    sprite_url = models.URLField(max_length=255)
    flavour_texts = models.JSONField()

    # Foreign key relationships to other groups
    types = models.ManyToManyField(
        'pokemon.PokemonType',
    )
    color = models.ForeignKey(
        'pokemon.PokemonColor',
        null=True,
        on_delete=models.SET_NULL
    )
    shape = models.ForeignKey(
        'pokemon.PokemonShape',
        null=True,
        on_delete=models.SET_NULL
    )
    habitat = models.ForeignKey(
        'pokemon.PokemonHabitat',
        null=True,
        on_delete=models.SET_NULL
    )
    egg_groups = models.ManyToManyField(
        'pokemon.PokemonEggGroup',
    )
    evolves_from = models.ForeignKey(
        'pokemon.Pokemon',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='evolves_into'
    )
    # Boolean attribites don't require FK
    is_legendary = models.BooleanField()
    is_mythical = models.BooleanField()

    def __str__(self):
        if self.name.endswith('-f'):
            name = self.name.replace('-f', ' (Female)')
        elif self.name.endswith('-m'):
            name = self.name.replace('-m', ' (Male)')
        else:
            name = self.name
        return name.title()

    @property
    def can_evolve(self):
        return self.evolves_into.all().count() > 0

    def get_sprite_filename(self):
        ext = self.sprite_url.split('/')[-1].split('.')[-1]
        return f'{self.name}.{ext}'

    def random_flavor_text(self):
        return random.choice(self.flavour_texts)

    def get_type_names(self):
        return ", ".join((type.name.title() for type in self.types.all()))

class PokemonType(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=255)

    def __str__(self):
        return self.name.title()


class PokemonColor(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=255)

    def __str__(self):
        return self.name.title()


class PokemonShape(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=255)

    def __str__(self):
        return self.name.title()


class PokemonHabitat(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=255)

    def __str__(self):
        return self.name.title()


class PokemonEggGroup(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=255)

    def __str__(self):
        return self.name.title()
