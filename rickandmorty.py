import requests
import json
import re
from py2neo import Graph, Node, Relationship, NodeMatcher

def obtener_recurso (base_url, rango):
    #Lista de valores que queremos obtener de la api
    ids = list(range(1, rango))  # Lista de IDs del 1 al 826

    # Construir la URL con la lista de IDs
    url = base_url + "[" + ",".join(str(id) for id in ids) + "]"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Comprobar si hay errores en la respuesta
        recurso = response.json()
        '''
        with open('rick_and_morty_characters.json', 'w', encoding='utf-8') as file:
            json.dump(recurso, file, ensure_ascii=False, indent=4)
        '''
        print("Personajes guardados en rick_and_morty_characters.json")
        

    except requests.exceptions.RequestException as e:
        print("Error al realizar la solicitud:", e)

    return recurso

def obtener_ultimo_numero(cadena):
    numeros = re.findall(r'\d+', cadena)
    if numeros:
        return int(numeros[-1])
    else:
        return None
    

def clave_existe(clave, valor, diccionario):
    if clave in diccionario:
        diccionario[clave].append(valor)
    else:
        diccionario[clave] = [valor]


#Establecer conexión con neo4j
graph = Graph("bolt://localhost:7687", auth=("neo4j", "Rick&Morty"))


url_personajes = "https://rickandmortyapi.com/api/character/"
url_locaciones = "https://rickandmortyapi.com/api/location/"
url_episodios = "https://rickandmortyapi.com/api/episode/"
personajes = obtener_recurso(url_personajes, 827)
locaciones = obtener_recurso(url_locaciones, 127)
episodios = obtener_recurso(url_episodios, 52)



relacion_episodios = {} # Diccionario para establecer que personajes aparecen en el mismo episodio
relacion_locacion = {} # Diccionario para establecer que personajes tienen la misma locacion

# [... El resto del código se mantiene igual hasta la creación de los nodos ...]

# Usamos "Character" como label y almacenamos el nombre como propiedad
for personaje in personajes:
    nombre = personaje.pop('name') 
    locacion = personaje['origin']['name'] 
    clave_existe(locacion, nombre, relacion_locacion)
    for episodio in personaje['episode']: 
        numero = obtener_ultimo_numero(episodio)
        clave_existe(numero, nombre, relacion_episodios)
    del personaje['origin']
    del personaje['episode']
    del personaje['url']
    del personaje['created']
    del personaje['image']
    del personaje['location']
    etiquetas = personaje
    nodo = Node("Character", name=nombre, **etiquetas)
    graph.merge(nodo, "Character", "name")  # Merge evita la creación de nodos duplicados

for locacion in locaciones:
    nombre = locacion.pop('name')
    del locacion['residents']
    del locacion['url']
    del locacion['created']
    etiquetas = locacion
    nodo = Node("Location", name=nombre, **etiquetas)
    graph.merge(nodo, "Location", "name") 

for episodio in episodios:
    id = episodio['id']
    del episodio['id']
    del episodio['characters']
    del episodio['url']
    del episodio['created']
    etiquetas = episodio
    nodo = Node("Episode", id=id, **etiquetas)
    graph.merge(nodo, "Episode", "id") 

# [... El resto del código se mantiene igual hasta la creación de las relaciones ...]

# Generamos las relaciones usando las propiedades para encontrar los nodos
def generar_relaciones(relaciones, tipo_relacion):
    for relacion, valores in relaciones.items():
        for valor in valores:
            if tipo_relacion == 'aparecio_en':
                episodio_node = graph.nodes.match("Episode", id=relacion).first()
                character_node = graph.nodes.match("Character", name=valor).first()
                if episodio_node is not None and character_node is not None:
                    print(f"Creando relación '{tipo_relacion}' entre {character_node} y {episodio_node}")
                    relation = Relationship(character_node, tipo_relacion, episodio_node)
                    graph.merge(relation)
                else:
                    print(f"No se pudo crear la relación '{tipo_relacion}'. Nodos: {character_node}, {episodio_node}")
            elif tipo_relacion == 'ultima_vez_visto_en':
                location_node = graph.nodes.match("Location", name=relacion).first()
                character_node = graph.nodes.match("Character", name=valor).first()
                if location_node is not None and character_node is not None:
                    print(f"Creando relación '{tipo_relacion}' entre {character_node} y {location_node}")
                    relation = Relationship(character_node, tipo_relacion, location_node)
                    graph.merge(relation)
                else:
                    print(f"No se pudo crear la relación '{tipo_relacion}'. Nodos: {character_node}, {location_node}")


generar_relaciones(relacion_episodios, 'aparecio_en')
generar_relaciones(relacion_locacion, 'ultima_vez_visto_en')