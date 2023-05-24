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

# Consultas MongoDB

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

# Consultas Neo4j





