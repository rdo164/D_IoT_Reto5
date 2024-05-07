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