from django.db import models
from django.conf import settings
# Create your models here.


class FavouritePokemon(models.Model):
    '''
    A model that stores favourite pokemons of users
    '''
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    pokemon_name = models.CharField(max_length=30)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pokemon_name
