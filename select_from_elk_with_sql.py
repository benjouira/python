from elasticsearch import Elasticsearch
import pymssql
import pandas as pd

def total_releve_valide_par_banque(annee = '2022'):
    es=Elasticsearch(hosts=['http://192.168.10.198:9200'], http_auth=('khalil', 'a12345678'))
    print(es.ping())
    d=es.sql.query(body={"fetch_size": 10000,'query': "select Valider,Banque,count(*) as total from pfe_xrelevehistorique  where year(Date_opr)="+annee+" group by Valider,Banque"})
    colonnes=[a["name"] for a in d["columns"]]
    data=d["rows"]
    print(len(data),'-----')
    df=pd.DataFrame(data,columns=colonnes)
    # df.to_excel('./f.xlsx')
    # d=es.sql.query(body={"fetch_size": 10000,'query': 'SELECT count(*) from "rabii_releve"'})
    # print(df)
    return(df)


    

def total_releve_valide_et_rapproche_par_banque(annee = '2022'):
    es=Elasticsearch(hosts=['http://192.168.10.198:9200'], http_auth=('khalil', 'a12345678'))
    print(es.ping())
    d=es.sql.query(body={"fetch_size": 10000,'query': "select Valider,Banque,count(*) as total from pfe_xrelevehistorique where year(Date_opr)="+annee+" and Rapprocher <>'' and Rapprocher is not null group by Valider,Banque"})
    colonnes=[a["name"] for a in d["columns"]]
    data=d["rows"]
    # print(len(data),'-----')
    df=pd.DataFrame(data,columns=colonnes)
    # df.to_excel('./f.xlsx')
    # d=es.sql.query(body={"fetch_size": 10000,'query': 'SELECT count(*) from "rabii_releve"'})
    # print(df)
    return(df)

    
    
# def releve_non_equilibre(annee = '2022'):
#     es=Elasticsearch(hosts=['http://192.168.10.198:9200'], http_auth=('khalil', 'a12345678'))
#     print(es.ping())
#     d=es.sql.query(body={"fetch_size": 10000,'query': "select * from gaccpe ge where year(GaccPE_Date)="+annee+" and GaccJou_Code like '%ATB%'and exists(select * from gaccpd gd where gd.gaccpe_num=ge.gaccpe_num group by gd.gaccpe_num having sum(gd.GaccPD_Debit-GaccPD_credit)<>0)"})
#     colonnes=[a["name"] for a in d["columns"]]
#     data=d["rows"]
#     # print(len(data),'-----')
#     df=pd.DataFrame(data,columns=colonnes)
#     # df.to_excel('./f.xlsx')
#     # d=es.sql.query(body={"fetch_size": 10000,'query': 'SELECT count(*) from "rabii_releve"'})
#     # print(df)
#     return(df)

# ************** query from sql


def releve_non_equilibre (annee='2022'):
    conn_default = pymssql.connect(server='192.168.10.216', user='sa', password='123', database='mas')
    cursor_default = conn_default.cursor(as_dict=True)

    req="select * from gaccpe ge where year(GaccPE_Date)="+annee+" and exists(select * from gaccpd gd where gd.gaccpe_num=ge.gaccpe_num group by gd.gaccpe_num having sum(gd.GaccPD_Debit-GaccPD_credit)<>0)"
    df=pd.read_sql_query(req,conn_default)
    # df["Date_Modif"]=df["Date_Modif"].astype(str).replace('NaT','').str.slice(0, 10)

    # df["Date_Modif"]=pd.to_datetime(df['Date_Modif'])
    # df["Date_Modif"].fillna(np.nan)
    return(df)
