import os
import json
from app.repositories.MongoRepository import MongoRepository

# cogemos el archivo EjerciciosGym.json y lo leemos
with open('seeders/EjerciciosGym.json', encoding='utf-8') as file:
    data = json.load(file)


# creamos una instancia de MongoRepository
repo = MongoRepository('exercises')

# eliminamos todos los datos de la base de datos
repo.delete_all()




# insertamos los datos en la base de datos
result = repo.insert_many(data)

print(f'{len(result.inserted_ids)} inserted')



# obtenemos todos los músculos distintos
distinct_muscles = repo.collection.distinct('muscle')
distinct_secondary_muscles = repo.collection.distinct('secondary_muscle')

# combinamos y eliminamos duplicados
all_muscles = list(set(distinct_muscles + distinct_secondary_muscles))

# guardamos los músculos en un archivo JSON
with open('seeders/muscles.json', 'w', encoding='utf-8') as file:
    json.dump(all_muscles, file, ensure_ascii=False)

print('Muscles saved to muscles.json')