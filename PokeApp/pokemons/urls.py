from django.urls import path
from . import views

app_name = 'pokemons'
urlpatterns = [
    path('accounts/registration', views.registration, name='registration'),

    path('', views.pokemon_list, name='pokemon_list'),
    path('detail-view/<str:pokemon_name>/',
         views.detail_view, name='detail_view'),
    path('detail-view/<str:name>/save',
         views.save_pokemon, name='save_pokemon'),
    path('detail-view/<str:name>/delete',
         views.delete_pokemon, name='delete_pokemon'),
    path('favourites/',
         views.show_favourites, name='show_favourites'),
]
