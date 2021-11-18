import zipfile
import random
import csv

from django.shortcuts import render
from django.views.generic import ListView, View, DetailView
from django.http import JsonResponse, Http404, HttpResponse

from pokemon import forms
from pokemon.models import Pokemon
from pokemon.utils import PokeAPI

class IndexView(ListView):
    ''' Main view for displaying a list of Pokemon and their details '''
    model = Pokemon
    template_name = 'index.html'

    def get_queryset(self):
        qs = super().get_queryset()

        # Filter out by inputs with many-to-many relationships first
        for param in ['types','egg_groups']:
            if param in self.request.GET:
                # Filter by each given item
                values = self.request.GET.getlist(param)
                for value in values:
                    qs = qs.filter(**{param: value})

        # Compile the remaining filters into a set of arguments
        filters = {}
        for param in ['color','shape', 'habitat']:
            value = self.request.GET.get(param)
            if value:
                filters[param] = value

        # Allow searching of names
        if 'name' in self.request.GET:
            filters['name__icontains'] = self.request.GET['name']

        if self.request.GET.get('is_legendary') == 'true':
            filters['is_legendary'] = True

        if self.request.GET.get('is_mythical') == 'true':
            filters['is_mythical'] = True

        if self.request.GET.get('can_evolve') == 'true':
            qs = qs.filter(evolves_into__isnull=False)

        if self.request.GET.get('cant_evolve') == 'true':
            qs = qs.filter(evolves_into__isnull=True)

        return qs.filter(**filters).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(form=forms.PokemonFilterForm(self.request.GET))
        return context


class ExportView(ListView):
    model = Pokemon
    http_method_names = ['post']


    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset()
        return qs.filter(pk__in=self.request.POST.getlist('selected_pokemon'))

    def post(self, request, *args, **kwargs):
        selected_pokemon = self.get_queryset()

        # Export selected pokemon to CSV file
        if 'csv' in self.request.POST:
            return self.generate_csv(selected_pokemon)

        # Download sprites and pack into a zip file
        elif 'sprites' in self.request.POST:
            return self.generate_sprites_zip(selected_pokemon)

        # 404 if anything else submitted
        raise Http404

    def generate_csv(self, queryset):
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="pokemon.csv"'},
        )
        writer = csv.writer(response)
        for pokemon in queryset:
            writer.writerow([
                pokemon.index,
                str(pokemon),
                pokemon.random_flavor_text()
            ])
        return response

    def generate_sprites_zip(self, queryset):
        response = HttpResponse(
            content_type="application/x-zip-compressed",
            headers={'Content-Disposition': 'attachment; filename=sprites.zip'}
        )
        zip_file =  zipfile.ZipFile(
            response,
            mode="w",
            compression=zipfile.ZIP_DEFLATED
        )
        for pokemon in queryset:
            data = PokeAPI.get_sprite(pokemon)
            zip_file.writestr(pokemon.get_sprite_filename(), data)

        zip_file.close()

        return response
