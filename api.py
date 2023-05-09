import requests
import json

url = 'https://rickandmortyapi.com/api/character/'
response = requests.get(url)
data = response.json()

all_characters = []

while data['info']['next']:
    response = requests.get(data['info']['next'])
    data = response.json()
    for result in data['results']:
        all_characters.append(result)

with open('rick_and_morty_characters.json', 'w', encoding='utf-8') as f:
    for character in all_characters:
        f.write(json.dumps(character, ensure_ascii=False, indent=4))
        f.write('\n')
