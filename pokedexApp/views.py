from django.shortcuts import render
import urllib.request
import json
from http import HTTPStatus
from urllib.error import HTTPError


# Funciones para los path

# create a function to get the list of pokemon of a color
def list_color(request,color):
    url_pokeapi = urllib.request.Request(f'https://pokeapi.co/api/v2/pokemon-color/'+str(color))
    url_pokeapi.add_header('User-Agent', "pikachu")
    source = urllib.request.urlopen(url_pokeapi).read()
    list_of_data = json.loads(source)
    count_pokemon = len(list_of_data['pokemon_species'])
    list_pokemon = []
    for i in range(count_pokemon):
        list_pokemon.append(list_of_data['pokemon_species'][i]['name'])
    return list_pokemon

def list_pokemon(request,type):
    url_pokeapi = urllib.request.Request(f'https://pokeapi.co/api/v2/type/'+str(type))
    url_pokeapi.add_header('User-Agent', "pikachu")
    source = urllib.request.urlopen(url_pokeapi).read()
    list_of_data = json.loads(source)
    count_pokemon = len(list_of_data['pokemon'])
    list_pokemon = []
    for i in range(count_pokemon):
        list_pokemon.append(list_of_data['pokemon'][i]['pokemon']['name'])
    return list_pokemon


# create a function to get the list of pokemon of a generation
def list_generation(request,generation):
    url_pokeapi = urllib.request.Request(f'https://pokeapi.co/api/v2/generation/'+str(generation))
    url_pokeapi.add_header('User-Agent', "pikachu")
    source = urllib.request.urlopen(url_pokeapi).read()
    list_of_data = json.loads(source)
    count_pokemon = len(list_of_data['pokemon_species'])
    list_pokemon = []
    for i in range(count_pokemon):
        list_pokemon.append(list_of_data['pokemon_species'][i]['name'])
    return list_pokemon


# intersect list_generation and list_pokemon
def intersect(request,generation,type):
    list_gen = list_generation(request,generation)
    list_poke = list_pokemon(request,type)
    list_intersect = [x for x in list_gen if x in list_poke]
    return list_intersect
# Check if the Pokemons on a list can evolve and make a list with those that can evolve
def check_evolution(request,list_pokemon):
    list_evolution = []
    for i in range(len(list_pokemon)):
        url_pokeapi = urllib.request.Request(f'https://pokeapi.co/api/v2/pokemon-species/{list_pokemon[i]}')
        url_pokeapi.add_header('User-Agent', "pikachu")
        source = urllib.request.urlopen(url_pokeapi).read()
        list_of_data = json.loads(source)
        if list_of_data['evolves_from_species'] != None:
            list_evolution.append(list_pokemon[i])
    return list_evolution



 
def pokeindex(request):
    try:
        if request.method == 'POST':
            pokemon = request.POST['pokemon'].lower()
            pokemon = pokemon.replace(' ', '%20')
            url_pokeapi = urllib.request.Request(f'https://pokeapi.co/api/v2/type/{pokemon}')
            url_pokeapi.add_header('User-Agent', "poison")
            source = urllib.request.urlopen(url_pokeapi).read()
            
            # Convirtiendo el JSON a un diccionario
            # 'list_of_data' guardará todos los datos que estamos solicitando
            list_of_data = json.loads(source)
               
            data = {
                "name": str(list_of_data['name']),
                "lista_epica": list_pokemon(request,str(list_of_data['name'])),

                
    
            }

        else:
            data = {}
        return render(request, "main/pokeindex.html", data)
    except HTTPError as e:
        if e.code == 404:
            return render(request, "main/404.html")


def index(request):
    try:
        if request.method == 'POST':
            pokemon = request.POST['pokemon'].lower()
            pokemon = pokemon.replace(' ', '%20')
            url_pokeapi = urllib.request.Request(f'https://pokeapi.co/api/v2/pokemon/{pokemon}')
            url_pokeapi.add_header('User-Agent', "pikachu")
            source = urllib.request.urlopen(url_pokeapi).read()
            a= str({pokemon})
            if a =="vaporeon":
                return render(request, "main/404.html", data)

            

            # Convirtiendo el JSON a un diccionario
            # 'list_of_data' guardará todos los datos que estamos solicitando
            list_of_data = json.loads(source)
                
            # La variable 'data' guardará todo lo que vamos a renderizar en HTML
            # Las llaves y valores las provee la API de Pokemon

            # Altura de decímetros a metros
            height_obtained = (float(list_of_data['height']) * 0.1)
            height_rounded = round(height_obtained, 2)

            # Peso de hectogramos a kilogramos
            weight_obtained = (float(list_of_data['weight']) * 0.1)
            weight_rounded = round(weight_obtained, 2)
            # count abilities and create a list with them and create string with them
            count_abilities = len(list_of_data['abilities'])
            list_abilities = []
            for i in range(count_abilities):
                list_abilities.append(list_of_data['abilities'][i]['ability']['name'])
            abilities = ', '.join(list_abilities)
            # count types and create a list with them and create string with them
            count_types = len(list_of_data['types'])
            list_types = []
            for i in range(count_types):
                list_types.append(list_of_data['types'][i]['type']['name'])
            types = ', '.join(list_types)      
           
            data = {
                "number": str(list_of_data['id']),
                "name": str(list_of_data['name']).capitalize(),
                "height": str(height_rounded)+ " m",
                "weight": str(weight_rounded)+ " kg",
                "sprite": str(list_of_data['sprites']['front_default']),
                "sprite2": str(list_of_data['sprites']['front_shiny']), 
                "type": types,
                "generation": str(list_of_data['game_indices'][0]['version']['name']).capitalize(),

            }

        else:
            data = {}
        return render(request, "main/index.html", data)
    except HTTPError as e:
        if e.code == 404:
            return render(request, "main/404.html")

