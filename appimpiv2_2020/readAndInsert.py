import cassandraSent as bd
import os
import utils as tool
from InternalControl import cInternalControl
import json

objControl=cInternalControl()
query='select id,actor,agent,branchreg,cip,class,cpc,cset,dateconcesion,dateoncirculation,dates,demanded,denomination,description,divisional,divisional_de,errorsolved,featuredate,folder,folioexit,gaceta,internatdatefeature,internatfoldernum,internatpubdate,internatpubnum,inventor,licenciatario,locarno,lsnewfields,main,maindata,noconcesion,officepatenttypedoc,oficiodate,oficionum,pc,priority,prodserv,reneweduntil,requester,resolution,sample,section,secuencia,summary,title,typedoc,url,year from thesis.impi_docs_master where year=2016 ALLOW FILTERING'
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
                        json_doc[lsField[colCount]].append(col)
            elif colCount==43 or colCount==48:        
                json_doc[lsField[colCount]]=int(col)
            else:
                json_doc[lsField[colCount]]=str(col)
            colCount+=1
    
    
                
                

                

