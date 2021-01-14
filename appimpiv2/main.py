import time
import requests 
import os
import utils as tool
import cassandraSent as bd
from selenium.webdriver.common.by import By
from InternalControl import cInternalControl


objControl=cInternalControl()

browser=tool.returnChromeSettings()
resultSet=bd.returnQueryResult('select lscontrol,page,limit_iteration from thesis.cjf_control where id_control='+str(objControl.idControl)+' ;')
lsControl=[]
page=0
limit_it=0
endTime=0
folder=''
if resultSet:
    for row in resultSet:
        lsControl=row[0]
        page=int(row[1])
        limit_it=int(row[2])
        folder=str(lsControl[0])+"/"+str(lsControl[1])+"/"+str(lsControl[2])+"/"
#Example of folder : MX/a/2015/000162
url="https://siga.impi.gob.mx/newSIGA/content/common/principal.jsf"

response= requests.get(url)
status= response.status_code
if status==200:
    browser.get(url)
    time.sleep(5)   
    startTime=tool.getTime()
    #Wait some time
    for num in range(page,limit_it):
        print('Starting in page:',str(num))
        folder=folder+str(num).zfill(6) 
        #Click on "Búsqueda Simple"
        btnBusqueda=tool.devuelveElemento('//*[@id="j_idt23"]/p[4]/a',browser)
        btnBusqueda.click()
        time.sleep(5)
        txtBuscar=tool.devuelveElemento('//*[@id="busquedaSimpleForm:cadenaBusquedaText"]',browser)
        txtBuscar.send_keys(folder)
        time.sleep(10)
        btnBuscar=tool.devuelveElemento('//*[@id="busquedaSimpleForm:buscar"]',browser)
        btnBuscar.click()
        time.sleep(5)
        txtResultados=tool.devuelveElemento('//*[@id="busquedaSimpleForm:j_idt62"]',browser)
        chunks=txtResultados.text.split(':')
        res=int(chunks[1])
        print('Rows:',str(res))
        if res>0:
            print('Reading folder: ',folder)
            for i in range(0,res):
                tool.processRows(browser,i,folder,res) 
            print('--------------------------------')    
            print('Done with folder:',folder)  
            print('--------------------------------')
            print('Restarting sequential NO FOUND counter to Zero')
            query="update thesis.cjf_control set noinfolimit=0 where id_control="+str(objControl.idControl)+"; "
            bd.executeNonQuery(query)
            query='update thesis.cjf_control set page='+str(num+1)+' where id_control=10'
            bd.executeNonQuery(query)
            
        else:
            print('Zero rows in the search...bye bye')
            #Look and update nolimit count
            query="select noinfolimit from thesis.cjf_control where id_control="+str(objControl.idControl)+"  ALLOW FILTERING"
            resultSet=bd.returnQueryResult(query)
            if resultSet:
                for row in resultSet:
                    countNoFound=int(str(row[0]))
                    countNoFound+=1
                    query="update thesis.cjf_control set noinfolimit="+str(countNoFound)+" where id_control="+str(objControl.idControl)+";" 
                    bd.executeNonQuery(query)
                    if countNoFound>=20:
                        print('20 times NOT FOUND reached, please change query initial conditions') 
                        os.sys.exit(0)     

        endTime=tool.getTime()
        minutes=tool.getDifferenceInMinutes(startTime,endTime)  
        print('Checking time...')
        if minutes>30:
            print('-----------------------------------------') 
            print('Hey, 30 mins done! Turn me back on!') 
            print('-----------------------------------------') 
            os.sys.exit(0)    
               
            
                   



  
       