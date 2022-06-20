from elasticsearch import Elasticsearch

import pandas as pd

def total_releve_valide_par_banque():
    es=Elasticsearch(hosts=['http://192.168.10.198:9200'], http_auth=('khalil', 'a12345678'))
    print(es.ping())
    d=es.sql.query(body={"fetch_size": 10000,'query': "select Valider,Banque,count(*) as total from pfe_xrelevehistorique  where year(Date_opr)=2022 group by Valider,Banque"})
    colonnes=[a["name"] for a in d["columns"]]
    data=d["rows"]
    print(len(data),'-----')
    df=pd.DataFrame(data,columns=colonnes)
    # df.to_excel('./f.xlsx')
    # d=es.sql.query(body={"fetch_size": 10000,'query': 'SELECT count(*) from "rabii_releve"'})
    # print(df)
    return(df)


    

