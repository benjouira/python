import json
import pymssql
import pandas as pd
from bson.json_util import dumps
from anytree import Node, RenderTree
conn=pymssql.connect(server='192.168.10.216', user='sa', password='123', database='MAS')
cursor = conn.cursor(as_dict=True)
req="select docn_code,case when docn_ori is null or docn_ori='' then '-' else docn_ori end as Docn_ori from documentn"
elements=[]
def add_nodes(nodes, parent, child):
    if parent not in nodes:
        nodes[parent] = Node(parent)  
    if child not in nodes:
        nodes[child] = Node(child)
    try:
        nodes[child].parent = nodes[parent]
        x=10
    except:
        nodes[child].parent=None

cursor.execute(req)
lignes = json.loads(dumps(cursor))

for l in lignes:
    if l["Docn_ori"]=='-':
        elements.append([l["docn_code"],""])
    else:
        els=l["Docn_ori"].split(',')
        for e in els:
            elements.append([e,l["docn_code"]])
for l in elements:
    print(l)
data=[d for d in elements if d[1]!='']
data = pd.DataFrame(columns=["Parent","Child"], data=elements)
nodes = {}
for parent, child in zip(data["Parent"],data["Child"]):
    add_nodes(nodes, parent, child)

roots = list(data[~data["Parent"].isin(data["Child"])]["Parent"].unique())
for root in roots:         # you can skip this for roots[0], if there is no forest and just 1 tree
    for pre, _, node in RenderTree(nodes[root]):
        print("%s%s" % (pre, node.name))

df=pd.read_sql_query(req,conn)
print(df)
df["NBS"]=df.docn_code.str.count(',')