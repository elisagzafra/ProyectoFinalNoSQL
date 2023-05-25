# ProyectoFinalNoSQL

# Descargar Librerias
pip instal requests
pip instal json
pip instal py2neo

# MONGO
En la terminal correr:

python3 personajes.py

docker stop mongo
docker rm mongo
docker run -p 27017:27017 \
       -v mongo-data:/data/db \
       --name mongo \
       -d mongo

mongoimport --db=ram1 --collection=char --file=rick_and_morty_characters1.json

docker exec -it mongo mongosh

use ram1

# Encontrar los 10 personajes que aparecen en más episodios y solo ver su nombre y el número de episodios en los que aparece
db.char.aggregate([ { $project: { _id: 0, name: 1, numEpisodes: { $size: "$episode" } } }, { $sort: { numEpisodes: -1 } }, { $limit: 10 }])

# Encontrar los personajes con status muerto que no sean humanos, mostrar nombre, origin.name, species y total de personajes
 db.char.aggregate([ { $match: { "status": "Dead", "species": { $ne: "Human" } } }, { $group: { _id: null, total: { $sum: 1 }, characters: { $push: { name: "$name", origin: "$origin.name", species: "$species" } } } }, { $project: { _id: 0, total: 1, characters: 1 } }])

# Encontrar todos los ‘Rick´s’ que aparecen en loa temporada 1, y mostrar su nombre, status, gender, origin y el total de personajes con esta condición. 
db.char.aggregate([ { $match: { $and: [ { "name": { $regex: "rick", $options: "i" } }, { "episode": { $in: [ "https://rickandmortyapi.com/api/episode/1", "https://rickandmortyapi.com/api/episode/2", "https://rickandmortyapi.com/api/episode/3", "https://rickandmortyapi.com/api/episode/4", "https://rickandmortyapi.com/api/episode/5", "https://rickandmortyapi.com/api/episode/6", "https://rickandmortyapi.com/api/episode/7", "https://rickandmortyapi.com/api/episode/8", "https://rickandmortyapi.com/api/episode/9", "https://rickandmortyapi.com/api/episode/10", "https://rickandmortyapi.com/api/episode/11"] } }] } }, { $facet: { characters: [ { $project: { _id: 0, name: 1, gender:1,status: 1, origin: "$origin.name" } }], total: [ { $count: "count" }] } }, { $unwind: "$total" }, { $project: { characters: 1, total: "$total.count" } }])



# NEO4J
Abrir Neo4j Desktop
Crear nueva base de datos local:
    New
    Create project
    Add
    Local DBMS
Nombrar base de datos (cualquier nombre) y poner contraseña: Rick&Morty (puede ser cualquier otra o ninguna)
Activar base de datos:
    Create
    Start
    Open

En la terminal:
python3 rickandmorty.py

En Neo4j:
match (n) return (n)   # Verifica creación del grafo

# Encontrar los personajes que han aparecido en la mayor cantidad de episodios:
MATCH (c:Character)-[:aparecio_en]->(e:Episode)
RETURN c.name, COUNT(e) AS num_of_episodes
ORDER BY num_of_episodes DESC
LIMIT 10

# Encontrar los episodios con la mayor cantidad de personajes:
MATCH (e:Episode)<-[:aparecio_en]-(c:Character)
RETURN e.id, COUNT(c) AS num_of_characters
ORDER BY num_of_characters DESC
LIMIT 10

# Encontrar las ubicaciones con la mayor cantidad de personajes:
MATCH (l:Location)<-[:ultima_vez_visto_en]-(c:Character)
RETURN l.name, COUNT(c) AS num_of_characters
ORDER BY num_of_characters DESC
LIMIT 10





