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
