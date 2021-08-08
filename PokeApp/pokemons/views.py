from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.core.paginator import Paginator

from .models import *
from .forms import *

import requests


def registration(request: HttpRequest) -> HttpResponse:
    # Create new user
    if request.method == 'POST':
        CreateForm = UserCreationForm(request.POST)
        if CreateForm.is_valid():
            CreateForm.save()
        return redirect('pokemons:pokemon_list')
    else:
        CreateForm = UserCreationForm()
        context: dict = {'CreateForm': CreateForm}
        return render(request, 'pokemons/register.html', context)


@login_required
def pokemon_list(request: HttpRequest) -> HttpResponse:
    # Get list of all pokemons
    pokemon_count = requests.get(
        'https://pokeapi.co/api/v2/pokemon/').json()['count']

    parameters: dict = {'limit': pokemon_count}
    response = requests.get(
        'https://pokeapi.co/api/v2/pokemon/', params=parameters).json()

    # Show 10 pokemons per page.
    ResponseTuple: tuple = tuple(response.items())
    paginator = Paginator(ResponseTuple[3][1], 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Add pokemon types to objects in current page
    for pokemon_on_page in paginator.get_page(page_number).object_list:
        resp = requests.get(pokemon_on_page['url']).json()
        pokemon_on_page['id'] = resp['id']
        for slot in resp['types']:
            if 'type' not in pokemon_on_page.keys():
                pokemon_on_page['type'] = slot['type']['name']
            else:
                pokemon_on_page['type'] = (
                    pokemon_on_page['type'], slot['type']['name'])

    context: dict = {'page_obj': page_obj, 'ResponseTuple': pokemon_on_page}
    return render(request, 'pokemons/pokemon_list.html', context)


@login_required
def detail_view(request: HttpRequest, pokemon_name: str) -> HttpResponse:
    # Get evolution chain data based on pokemon name
    getDetailsData = requests.get(
        f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}').json()
    getEvolutionChainLink = requests.get(getDetailsData['species']['url']).json()[
        'evolution_chain']['url']
    getEvolutionChainData = requests.get(getEvolutionChainLink).json()

    # Check if pokemon is already in favourites list and add flag to dictionary
    if FavouritePokemon.objects.filter(pokemon_name=pokemon_name, owner=request.user).exists():
        getDetailsData["exists_in_db"] = True

    context: dict = {'getDetailsData': getDetailsData,
                     'getEvolutionChainData': getEvolutionChainData['chain']}
    return render(request, 'pokemons/detail_view.html', context)


@login_required
def save_pokemon(request: HttpRequest, name: str) -> HttpResponse:
    # Save pokemon from current detail view to FavouritePokemon model
    pokemon = FavouritePokemon(owner=request.user, pokemon_name=name)
    pokemon.save()
    return redirect('pokemons:detail_view', pokemon_name=name)


@login_required
def delete_pokemon(request: HttpRequest, name: str) -> HttpResponse:
    # Remove pokemon from current detail view from FavouritePokemon model
    pokemon = FavouritePokemon.objects.filter(
        owner=request.user, pokemon_name=name).delete()
    return redirect('pokemons:detail_view', pokemon_name=name)


@login_required
def show_favourites(request: HttpRequest) -> HttpResponse:
    # Get list of all favourite pokemons for user in request
    fav_pokemons = FavouritePokemon.objects.filter(
        owner=request.user).order_by('pokemon_name')
    context: dict = {'fav_pokemons': fav_pokemons}
    return render(request, 'pokemons/favourites.html', context)
