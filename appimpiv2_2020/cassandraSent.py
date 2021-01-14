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
    cloud_config=''
    if objControl.heroku:
        cloud_config= {'secure_connect_bundle': objControl.rutaHeroku+'/secure-connect-dbquart.zip'}
    else:
        cloud_config= {'secure_connect_bundle': objControl.rutaLocal+'secure-connect-dbquart.zip'}


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
    



            

   
class CassandraConnection():
    cc_user='quartadmin'
    cc_keyspace='thesis'
    cc_pwd='P@ssw0rd33'
        

