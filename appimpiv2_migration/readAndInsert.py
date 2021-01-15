import cassandraSent as bd
import os
import utils as tool
from InternalControl import cInternalControl
import json
import uuid

objControl=cInternalControl()

lsYears=['2016','2017','2018','2019','2020']
"""
resultSet=bd.returnQueryResult('select page from thesis.cjf_control where id_control='+str(objControl.idControl)+' ;')
page=0
if resultSet:
    for row in resultSet:
        page=int(row[0])


year=page
"""


for year in lsYears:
    print('Migrating year ',str(year))
    query='select id,actor,agent,branchreg,cip,class,cpc,cset,dateconcesion,dateoncirculation,dates,demanded,denomination,description,divisional,divisional_de,errorsolved,featuredate,folder,folioexit,gaceta,internatdatefeature,internatfoldernum,internatpubdate,internatpubnum,inventor,licenciatario,locarno,lsnewfields,main,maindata,noconcesion,officepatenttypedoc,oficiodate,oficionum,pc,priority,prodserv,reneweduntil,requester,resolution,sample,section,secuencia,summary,title,typedoc,url,year from thesis.impi_docs_master where year='+str(year)+' ALLOW FILTERING'
    #lsFields 28
    #secuencia 43
    #year 48
    lsField=['id','actor','agent','branchreg','cip','class','cpc','cset','dateconcesion','dateoncirculation','dates','demanded','denomination','description','divisional','divisional_de','errorsolved','featuredate','folder','folioexit','gaceta','internatdatefeature','internatfoldernum','internatpubdate','internatpubnum','inventor','licenciatario','locarno','lsnewfields','main','maindata','noconcesion','officepatenttypedoc','oficiodate','oficionum','pc','priority','prodserv','reneweduntil','requester','resolution','sample','section','secuencia','summary','title','typedoc','url','year']
    lsResultSet=[]
    lsResultSet=bd.getLargeQuery(query)

    if lsResultSet:
        for row in lsResultSet:
            if objControl.heroku:        
                json_doc=tool.devuelveJSON('/app/'+objControl.hfolder+'/json_file.json')
            else:
                json_doc=tool.devuelveJSON(objControl.rutaLocal+'/json_file.json')
            colCount=0
            for col in row:
                if colCount==28:
                    if col is not None:
                        for item in col:
                            json_doc[lsField[colCount]].append(item)
                elif colCount==43 or colCount==48:        
                    json_doc[lsField[colCount]]=int(col)
                else:
                    json_doc[lsField[colCount]]=str(col)
                colCount+=1

            #Save info
            query="select id from thesis.impi_docs_masters where folder='"+json_doc['folder']+"' and gaceta='"+json_doc['gaceta']+"' and sample='"+json_doc['sample']+"' and section='"+json_doc['section']+"' and secuencia="+str(json_doc['secuencia'])+" ALLOW FILTERING ;"
            result=bd.returnQueryResult(query)   
            if result: 
                folder=json_doc['folder']
                gaceta=json_doc['gaceta']
                secuencia=str(json_doc['secuencia'])
                print('Folder: ',folder, 'and Gaceta: ',gaceta, ' and Sequence: ',secuencia,' existed')
                query='delete from thesis.impi_docs_master where id='+json_doc['id']+' '
                bd.executeNonQuery(query)
                print('Deleted...')
            else:
                old_id=json_doc['id']
                json_doc['id']=str(uuid.uuid4())
                lsRes=bd.insertarJSON('thesis.impi_docs_masters',json_doc)      
                if lsRes[0]==True:
                    print('Record added')
                    query='delete from thesis.impi_docs_master where id='+old_id+' '
                    bd.executeNonQuery(query)
                    print('Deleted...')
    else:
        print('No records')  

    print('Done with year:',str(year)) 
                 
              
    

                
                

                

