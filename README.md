# Explicación de los pasos seguidos

### 1. Reutilizar el [código del reto 1](https://github.com/rdo164/D_IoT_Reto1/blob/main/docker-compose.yml) y actualizarlo para poder almacenar el dashboard generado.

```
version: '3'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.13.0
    ports:
      - "9200:9200"
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    volumes:
      - esdata:/usr/share/elasticsearch/data  # Volumen para persistencia de datos

  kibana:
    image: docker.elastic.co/kibana/kibana:8.13.0
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch

  filebeat:
    image: docker.elastic.co/beats/filebeat:8.13.0
    command: filebeat -e -strict.perms=false
    volumes:
      - ./filebeat.yml:/usr/share/filebeat/filebeat.yml:rw
      - ./logs/dummy_logs.json:/usr/share/filebeat/dummy_logs.json:rw
      # Asegúrate de definir correctamente este volumen si deseas recolectar logs de Docker
      - /var/lib/docker/containers:/var/lib/docker/containers:ro

volumes:
  esdata:
    driver: local

```
### 2. He investigado cómo mandar un dato a ElasticSearch mediante el uso de python. [Fuente](https://rishab07.medium.com/indexing-data-into-elasticsearch-using-python-bdc04aacccdd)

```
# fuente: https://rishab07.medium.com/indexing-data-into-elasticsearch-using-python-bdc04aacccdd

try:
 import os
 import sys
 import elasticsearch
 from elasticsearch import Elasticsearch
 import pandas as pd
 from elasticsearch import RequestsHttpConnection
 print("All modules loaded")
except Exception as e:
 print("Some modules are missing")
 
es=Elasticsearch([
 {
 "host":'localhost',
 "port":9200,
 "scheme":'https'

 }
 ])
client = Elasticsearch(hosts=["http://localhost:9200"],
verify_certs = False, basic_auth=["rod", "1212"])


print(client.cluster.health)
print(client.ping())
```
Con este código compruebo si le están llegando los datos a ElasticSearch.

### 3. Fuente de datos
Ahora que ya sé insertar datos voy buscar una fuente de datos. He reutilizado un dataframe antiguo limpio que tenía para el entrenamiento, con este [notebook](./data/explore.ipynb) he visto que tenía uno de 1500 datos y simplemente he reformateado el formato con:

```
# Extraer la columna de "Marca" basada en las columnas disponibles
marca_cols = [col for col in data.columns if "marca: _" in col]
data['Marca'] = data[marca_cols].idxmax(axis=1).str.replace('marca: _', '')

# Extraer la columna de "Marca del Procesador"
procesor_br_cols = [col for col in data.columns if "procesor_br: _" in col]
data['Marca del Procesador'] = data[procesor_br_cols].idxmax(axis=1).str.replace('procesor_br: _', '')

# Extraer la columna de "Modelo del Procesador"
procesador_nombre_cols = [col for col in data.columns if "procesador_nombre: _" in col]
data['Modelo del Procesador'] = data[procesador_nombre_cols].idxmax(axis=1).str.replace('procesador_nombre: _', '')

# Extraer la columna de "Sistema Operativo"
os_cols = [col for col in data.columns if "os: _" in col]
data['Sistema Operativo'] = data[os_cols].idxmax(axis=1).str.replace('os: _', '')

# Eliminar las columnas originales para limpieza
data_clean = data.drop(columns=marca_cols + procesor_br_cols + procesador_nombre_cols + os_cols)

# Mostrar las primeras filas del dataframe modificado para verificar los cambios
data_clean.head()

``` 
### 4. Inserción de datos

Ahora que ya sé la fuente de datos que voy a utilizar voy a recorrerla e insertarla.
```
import pandas as pd
try:
 import os
 import sys
 import elasticsearch
 from elasticsearch import Elasticsearch
 from elasticsearch import RequestsHttpConnection
 print("All modules loaded")
except Exception as e:
 print("Some modules are missing")
 
# Conectarse a Elasticsearch
es=Elasticsearch([
 {
 "host":'localhost',
 "port":9200,
 "scheme":'http' 
 }
])

client = Elasticsearch(hosts=["http://localhost:9200"],
verify_certs = False, basic_auth=["rod", "1212"])

# Verifico la conexión
print(client.cluster.health)
print(client.ping())

# Leo datos del dataframe
df = pd.read_csv('./data/Ordenadores_upd.csv')

# Convierto el dataframe a un diccionario
data_list = df.to_dict(orient='records')
resp = es.indices.delete(
    index="computer",
)
print(resp)

# Itero el diccionario y enviar datos a Elasticsearch
for data in data_list:
    try:
        es.index(index='computer', body=data)
    except Exception as e:
        print(f'Error al indexar documento: {e}')

# Cierro la conexión
es.close()
```

### 5. Visualizar los datos
Con las diapositivas mi práctica con los gráficos, he empleado los que más valor podían aportar al cliente.
## Mejoras 
- Implementación del algoritmo en Kibana.
- Más seguridad enviando los datos encriptados.
- Obtención de datos en tiempo real.

## Problemas 
- Versiones. Al parecer en la versión 8 hay que utilizar seguridad por obligación. 
- Almacenamiento de Kibana.  Siempre tenía que hacer de nuevo los dashboards.

## Alternativas
- Respecto a la visualización se podría hacer con Grafana y PowerBI.