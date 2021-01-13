import time
import requests 
import os
import utils as tool
import cassandraSent as bd
from selenium.webdriver.common.by import By

browser=tool.returnChromeSettings()
#Example of folder : MX/a/2015/000162
url="https://siga.impi.gob.mx/newSIGA/content/common/principal.jsf"
response= requests.get(url)
status= response.status_code
if status==200:
    #Wait some time
    browser.get(url)
    time.sleep(10)   

startTime=tool.getTime()
endTime=0
resultSet=bd.returnQueryResult('select lscontrol from thesis.cjf_control where id_control=10')
lsControl=[]
if resultSet:
    for row in resultSet:
        lsControl=row[0]
        folder=str(lsControl[0])+"/"+str(lsControl[1])+"/"+str(lsControl[2])+"/"+str(StartID).zfill(6)
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
               
            
                   



  
       