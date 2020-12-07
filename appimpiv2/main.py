import time
import requests 
import os
import utils as tool
import cassandraSent as bd
from selenium.webdriver.common.by import By

browser=tool.returnChromeSettings()
#Get a bunch of folder (expedientes)
url="https://siga.impi.gob.mx/newSIGA/content/common/principal.jsf"
response= requests.get(url)
status= response.status_code
if status==200:
    #Wait some time
    browser.get(url)
    time.sleep(10)   

startTime=tool.getTime()
endTime=0
resultSet=bd.returnQueryResult('select folder,inimpi2 from thesis.impi_docs where inimpi2<1 ALLOW FILTERING')
if resultSet:
    for row in resultSet:
        folder=''
        inimpi2=''
        folder=str(row[0])  
        inimpi2=str(row[1])
        if inimpi2!='1':
            #Click on "Búsqueda Simple"
            btnBusqueda=tool.devuelveElemento('//*[@id="j_idt23"]/p[4]/a',browser)
            btnBusqueda.click()
            time.sleep(10)
            txtBuscar=tool.devuelveElemento('//*[@id="busquedaSimpleForm:cadenaBusquedaText"]',browser)
            txtBuscar.send_keys(folder)
            time.sleep(10)
            btnBuscar=tool.devuelveElemento('//*[@id="busquedaSimpleForm:buscar"]',browser)
            btnBuscar.click()
            time.sleep(10)
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
                for i in range(1,3):
                    browser.back()    
                       
            else:
                print('Zero rows in the search...bye bye')
                os.sys.exit(0)

            endTime=tool.getTime()
            minutes=tool.getDifferenceInMinutes(startTime,endTime)  
            print('Checking time...')
            if minutes>30:
                print('-----------------------------------------') 
                print('Hey, 30 mins done! Turn me back on!') 
                print('-----------------------------------------') 
                os.sys.exit(0)    
else:
    print('Something went wrong with result set in cassandra...Zero rows') 
    os.sys.exit(0)                
            
                   



  
       