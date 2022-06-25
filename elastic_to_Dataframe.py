from elasticsearch import Elasticsearch
import pandas as pd 

es = Elasticsearch(hosts=['http://192.168.10.198:9200'], http_auth=('khalil', 'a12345678'))
print(es.ping())


# function to get first and last day of month given
def get_first_and_last_day_of_month (date):
    start_day_of_month = pd.Period(date,freq='M').start_time.date()
    last_day_of_month = pd.Period(date,freq='M').end_time.date()
    return start_day_of_month, last_day_of_month


# function return a dataframe selected from elk index by bank and range date given  
def search_by_bank_and_date (bank, date):
    first_date , last_date = get_first_and_last_day_of_month(date)
    my_results = es.search(
            index="rabii_releve", 
            # scroll='10m', 
            body={
                "size": 20,
                "query": {
                    "bool":{
                        "must":[
                            {
                                "range": {
                                    "date_opr": {
                                        "gte": first_date, "lte": last_date
                                    }
                                }
                            },
                            {
                                "match": {
                                    'Banque' : bank
                                    }
                            }
                        
                        ]
                    }
                }
            }, # close body
            
            )

    df = pd.DataFrame()
    if my_results['hits']['total']['value'] > 0 :
        # print (my_results['hits']['total']['value'])
        list_Doc = []
        for doc in my_results["hits"]["hits"]:
            list_Doc.append (doc["_source"])

        df = pd.DataFrame(list_Doc)
        print(len(df))
        # print(df2)

        print(df.info())
        df.drop(['@timestamp', 'reference', 'lignes', '@version'], axis=1, inplace=True)

    return (df)
















