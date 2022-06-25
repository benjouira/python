from pydoc import describe
from elasticsearch import Elasticsearch, TransportError
from datetime import datetime
import pandas as pd
import pyodbc
import numpy as np


def doc_generator(df):

    def filterKeys(document):
        return ({key: document[key] for key in list(df.columns)})

    # df['société'] = 'mas'
    df.fillna('', inplace=True)

    try:
        es_client = Elasticsearch(['192.168.10.198:9200'], http_auth=('khalil', 'a12345678'))
    except:
        print ('connection error ! ')

    for index, row in df.iterrows():
        try:
            now = datetime.now()
            resp = es_client.index(index='releve_extracted_from_pdf', id='mas'+row['BANQUE']+str(now), body=filterKeys(row))
        except :
            pass
        
# doc_generator(df)

# def x (x):
#     def sul (y):
#         return x+2
#     return sul(x)
# print (x(2))