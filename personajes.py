import requests
import json

url = 'https://rickandmortyapi.com/api/character/'
response = requests.get(url)
data = response.json()

all_characters = data['results']  # Agregar los primeros personajes obtenidos

while 'next' in data['info'] and data['info']['next'] is not None:  # Verificar si 'next' existe y no es None
    response = requests.get(data['info']['next'])
    data = response.json()
    all_characters.extend(data['results'])  # Agregar los personajes de la página actual

with open('rick_and_morty_characters1.json', 'w', encoding='utf-8') as f:
    for character in all_characters:
        f.write(json.dumps(character, ensure_ascii=False, indent=4))
        f.write('\n')