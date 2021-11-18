from django.core.management.base import BaseCommand, CommandError
import pokemon.tasks

class Command(BaseCommand):
    help = "Populate the database with information from pokeapi.co"

    def handle(self, *args, **options):
        self.stdout.write('Connecting to pokeapi.com to populate the database...')
        pokemon.tasks.populate()
        self.stdout.write('Populate task run succesfully.')
