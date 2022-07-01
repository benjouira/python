import pymssql
import json

from bson.json_util import dumps
class DBASE:
    def __init__(self,ser,dbname):
        self.conn=pymssql.connect(server=ser, user='sa', password='123', database=dbname)
        self.cursor = self.conn.cursor(as_dict=True)
        self.ser=ser
        self.dbname=dbname
        self.tablename=[]
        self.fields=[]
        self.Proccedures=[]

    def getTablesNames(self):
        req="SELECT TABLE_NAME \
              FROM INFORMATION_SCHEMA.TABLES \
              WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_CATALOG='"+self.dbname+"'"
        #execution
        self.cursor.execute(req)
        self.tablename=json.loads(dumps(self.cursor))
        return self.tablename

    def getTableFields(self,tbl):
        #requete de recuperation des champs d'une table sql
        req="select column_name as nom ,data_type as type from information_schema.columns where table_name = '"+tbl['TABLE_NAME']+"'"
        #[{nom:att,type:type_att}]
        self.cursor.execute(req)
        self.fields=json.loads(dumps(self.cursor))
        #print("*****",self.fields)
        return self.fields
        
    def getProcceduresStockesUti(self):
        #Category = 0 > Proc Stock utilisateur
        #Category = 2 > Proc Stock System
        req="SELECT name FROM sysobjects WHERE Type = 'P' AND category = '0'"
        self.cursor.execute(req)
        self.Proccedures=json.loads(dumps(self.cursor))
        #print("*/*/*/*/*/",self.Proccedures)
        return self.Proccedures
    
    def getJobs(self):
        #job_id
        req="SELECT name FROM msdb.dbo.sysjobs"
        self.cursor.execute(req)
        self.Jobs=json.loads(dumps(self.cursor))
        #print("+++++++",self.Jobs)
        return self.Jobs

class Explorer:
    def __init__(self):
        self.SocList=[]
        
    def getAllDB(self):
        conn=pymssql.connect(server='192.168.10.216', user='sa', password='123', database='MAS')
        cursor = conn.cursor(as_dict=True)
        ReqGetSocietes="select BD_NameConn,BD_Serer,BD_Test from ref..bd where bd_test=0"
        cursor.execute(ReqGetSocietes)
        self.SocList=json.loads(dumps(cursor))
        return self.SocList

e=Explorer()
e.getAllDB()
#for i in e.SocList:
#    print(i)
db=DBASE(e.SocList[1]['BD_Serer'],e.SocList[1]['BD_NameConn'])
db.getTablesNames()
#for j in db.tablename:
#   print("------",j)
db.getTableFields(db.tablename[0])
# db.getProcceduresStockesUti()
# db.getJobs()

