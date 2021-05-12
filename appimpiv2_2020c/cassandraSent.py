import json
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import SimpleStatement
import os
from InternalControl import cInternalControl

objControl=cInternalControl()
timeOut=objControl.timeout
idControl=objControl.idControl
hfolder=objControl.hfolder

lsRes=[] 

def getCluster():
    #Connect to Cassandra
    objCC=CassandraConnection()
    cloud_config={}
    zip_file='secure-connect-dbquart_serverless.zip'
    cloud_config['init-query-timeout']=10
    cloud_config['connect_timeout']=10
    cloud_config['set-keyspace-timeout']=10
    secure_bundle=''
    if objControl.heroku:
        secure_bundle= objControl.rutaHeroku+'/'+zip_file
    else:
        secure_bundle: objControl.rutaLocal+zip_file

    cloud_config['secure_connect_bundle'] =secure_bundle   
    auth_provider = PlainTextAuthProvider(objCC.cc_user,objCC.cc_pwd)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider) 

    return cluster  

def insertarJSON(table,json_doc):
    cluster=getCluster()
    session = cluster.connect()
    session.default_timeout=timeOut
    jsonS=json.dumps(json_doc)           
    insertSt="INSERT INTO "+table+" JSON '"+jsonS+"';" 
    future = session.execute_async(insertSt)
    future.result()  
    record_added=True
    lsRes.append(record_added)
    cluster.shutdown()

    return lsRes

def returnQueryResult(querySt):
    cluster=getCluster()
    session = cluster.connect()
    session.default_timeout=timeOut
    result=''
    future = session.execute_async(querySt)
    result=future.result()
    cluster.shutdown()

    return result

def executeNonQuery(querySt):
    cluster=getCluster()
    session = cluster.connect()
    session.default_timeout=timeOut
    future = session.execute_async(querySt)
    future.result()
    cluster.shutdown()

def getLargeQuery(query):
    cluster = getCluster()
    session = cluster.connect()
    session.default_timeout=70     
    statement = SimpleStatement(query, fetch_size=1000)
    lsResultSet=[]
    for row in session.execute(statement):
        lsResultSet.append(row)
                
    cluster.shutdown()
    return lsResultSet

def getShortQuery(query):
    res=''
    cluster=getCluster()
    session = cluster.connect()
    session.default_timeout=70
    #Check wheter or not the record exists      
    future = session.execute_async(query)
    res=future.result()
    cluster.shutdown()

    return res 

def getFieldsFromTable(keyspace,table):
    query="select column_name from system_schema.columns WHERE keyspace_name = '"+keyspace+"' AND table_name = '"+table+"';"
    columns_list=''
    columns_list=getShortQuery(query)
    lsFields=[]
    for col in columns_list:
        lsFields.append(col[0])

    fieldsForQuery=','.join(lsFields) 

    return fieldsForQuery             
    



            

   
class CassandraConnection():
    cc_user='psXzplCMoTnTjWLSeAblXSkr'
    cc_keyspace='thesis'
    cc_pwd='_vGwtwEUsOxj9ZuSbm6SOJhyQOsU-s9QEzX7ZWZcRYKeew9sOqPeFmKr-pDzsIoisiF8aInS1HjSs7_fqZ9EZaMS96TNCwn_yReyjZvHuys+_fGSBuHKZz_+NTj6Z6L0'
        

