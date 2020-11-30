from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import cassandraSent as bd
import PyPDF2
import uuid
import base64
import time
import json
import os
import sys
from textwrap import wrap


download_dir='/app/Downloadimpi'

"""
Casos
Nota: Si no existiera un caso en el código, que termine el programa y muestre qué caso es para agregarlo con sus campos
"""
lsCasos=[
'Notificaciones, conforme al párrafo segundo del art. 183 de la Ley de la Propiedad Industrial',
'Patentes, Registros de Modelos de Utilidad y de Diseños Industriales',
'Licencias, Transmisiones y Cambios en Solicitudes, Patentes y Registros',
'Solicitudes de Patente, de Registros de Modelo de Utilidad y de Diseños Industriales',
'Requisitos de Examen de Forma y Fondo, Abandonos de Solicitudes de Patentes y Registros',
'Gaceta de Notificaciones de la Dirección Divisional de Patentes',
'Solicitudes de Marcas, Avisos y Nombres Comerciales presentadas ante el Instituto',
'Marcas Registradas, Avisos y Nombres Comerciales',
'Conservación de los Derechos',
'Notificaciones de Protección a la Propiedad Intelectual'

]

def appendInfoToFile(path,filename,strcontent):
    txtFile=open(path+filename,'a+')
    txtFile.write(strcontent)
    txtFile.close()


def processRows(browser,row):

    gaceta=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':j_idt68"]/thead/tr/td[2]')[0].text
    sample=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':j_idt68"]/thead/tr/td[3]')[0].text
    section=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':j_idt68"]/thead/tr/td[4]')[0].text

    gaceta=str(gaceta).split(':')[1].strip()
    sample=str(sample).split(':')[1].strip()
    section=str(section).split(':')[1].strip()
    
    json_doc=devuelveJSON('/app/appimpiv2/json_file.json')
    json_doc['id']=str(uuid.uuid4())
    json_doc['gaceta']=gaceta
    json_doc['sample']=sample
    year=sample.split(' ')[2]
    json_doc['section']=section
    json_doc['year']=int(year)

    numTablaDetalles=len(browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr'))
    #Start reading details
    if gaceta in lsCasos:
        processCase(json_doc,gaceta,browser,row,numTablaDetalles)
    else:
        print('--------------------------------------------')  
        print('Caso: ',gaceta,' no existe')
        os.sys.exit(0)  

    

def processCase(json_doc,gaceta,browser,row,numDetalles):
    if lsCasos[0]==gaceta:
        if numDetalles==6:
            json_doc['folder']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[1]/td[2]')[0].text.strip()
            json_doc['oficioDate']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[2]/td[2]')[0].text.strip()
            json_doc['oficioNum']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[3]/td[2]')[0].text.strip()
            json_doc['description']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[4]/td[2]')[0].text.strip()
            json_doc['url']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[5]/td[2]')[0].text.strip()
            json_doc['dateOnCirculation']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[6]/td[2]')[0].text.strip()
        if numDetalles==7:
            json_doc['folder']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[1]/td[2]')[0].text.strip()
            json_doc['noConcesion']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[2]/td[2]')[0].text.strip()  
            json_doc['oficioDate']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[3]/td[2]')[0].text.strip()
            json_doc['oficioNum']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[4]/td[2]')[0].text.strip()
            json_doc['description']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[5]/td[2]')[0].text.strip()
            json_doc['url']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[6]/td[2]')[0].text.strip()
            json_doc['dateOnCirculation']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[7]/td[2]')[0].text.strip()   
    if lsCasos[1]==gaceta:
        json_doc['officePatentTypeDoc']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[1]/td[2]')[0].text.strip()
        json_doc['typeDoc']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[2]/td[2]')[0].text.strip()
        json_doc['dateConcesion']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[3]/td[2]')[0].text.strip()
        json_doc['folder']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[4]/td[2]')[0].text.strip()
        json_doc['featureDate']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[5]/td[2]')[0].text.strip()
        json_doc['internatFolderNum']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[6]/td[2]')[0].text.strip()
        json_doc['internatDateFeature']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[7]/td[2]')[0].text.strip()
        json_doc['internatPubNum']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[8]/td[2]')[0].text.strip()
        json_doc['internatPubDate']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[9]/td[2]')[0].text.strip()
        json_doc['inventor']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[10]/td[2]')[0].text.strip()
        json_doc['main']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[11]/td[2]')[0].text.strip()
        json_doc['agent']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[12]/td[2]')[0].text.strip()
        if numDetalles==17:
            json_doc['cip']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[13]/td[2]')[0].text.strip()
            json_doc['cpc']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[14]/td[2]')[0].text.strip()
            json_doc['title']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[15]/td[2]')[0].text.strip()
            json_doc['summary']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[16]/td[2]')[0].text.strip()
            json_doc['dateOnCirculation']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[17]/td[2]')[0].text.strip()
        if numDetalles==18:
            json_doc['priority']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[13]/td[2]')[0].text.strip()
            json_doc['cip']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[14]/td[2]')[0].text.strip()
            json_doc['cpc']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[15]/td[2]')[0].text.strip()
            json_doc['title']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[16]/td[2]')[0].text.strip()
            json_doc['summary']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[17]/td[2]')[0].text.strip()
            json_doc['dateOnCirculation']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[18]/td[2]')[0].text.strip()
    if lsCasos[2]==gaceta:
        json_doc['folder']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[1]/td[2]')[0].text.strip()
        json_doc['main']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[2]/td[2]')[0].text.strip()
        json_doc['dateOnCirculation']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[3]/td[2]')[0].text.strip()
    if lsCasos[3]==gaceta:
        json_doc['folder']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[1]/td[2]')[0].text.strip()
        json_doc['featureDate']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[2]/td[2]')[0].text.strip()
        if numDetalles==11:
            json_doc['requester']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[3]/td[2]')[0].text.strip()
            json_doc['inventor']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[4]/td[2]')[0].text.strip()
            json_doc['agent']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[5]/td[2]')[0].text.strip()
            json_doc['cip']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[6]/td[2]')[0].text.strip()
            json_doc['title']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[7]/td[2]')[0].text.strip()
            json_doc['cpc']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[8]/td[2]')[0].text.strip()
            json_doc['summary']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[9]/td[2]')[0].text.strip()
            json_doc['errorSolved']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[10]/td[2]')[0].text.strip()
            json_doc['dateOnCirculation']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[11]/td[2]')[0].text.strip()
        if numDetalles==12:
            json_doc['requester']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[3]/td[2]')[0].text.strip()
            json_doc['inventor']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[4]/td[2]')[0].text.strip()
            json_doc['agent']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[5]/td[2]')[0].text.strip()
            json_doc['priority']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[6]/td[2]')[0].text.strip()
            json_doc['cip']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[7]/td[2]')[0].text.strip()
            json_doc['title']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[8]/td[2]')[0].text.strip()
            json_doc['cpc']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[9]/td[2]')[0].text.strip()
            json_doc['summary']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[10]/td[2]')[0].text.strip()
            json_doc['errorSolved']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[11]/td[2]')[0].text.strip()
            json_doc['dateOnCirculation']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[12]/td[2]')[0].text.strip()
        if numDetalles==14:
            json_doc['internatFolderNum']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[3]/td[2]')[0].text.strip()
            json_doc['internatDateFeature']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[4]/td[2]')[0].text.strip()
            json_doc['internatPubNum']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[5]/td[2]')[0].text.strip()
            json_doc['internatPubDate']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[6]/td[2]')[0].text.strip()
            json_doc['requester']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[7]/td[2]')[0].text.strip()
            json_doc['inventor']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[8]/td[2]')[0].text.strip()
            json_doc['agent']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[9]/td[2]')[0].text.strip()
            json_doc['priority']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[10]/td[2]')[0].text.strip()
            json_doc['cip']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[11]/td[2]')[0].text.strip()
            json_doc['title']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[12]/td[2]')[0].text.strip()
            json_doc['summary']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[13]/td[2]')[0].text.strip()
            json_doc['dateOnCirculation']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[14]/td[2]')[0].text.strip()
    if lsCasos[4]==gaceta:
        json_doc['requester']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[1]/td[2]')[0].text.strip()
        json_doc['oficioNum']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[2]/td[2]')[0].text.strip()  
        json_doc['folder']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[3]/td[2]')[0].text.strip()
        json_doc['agent']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[4]/td[2]')[0].text.strip()
        json_doc['dateOnCirculation']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[5]/td[2]')[0].text.strip()
    if lsCasos[5]==gaceta:
        json_doc['description']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[1]/td[2]')[0].text.strip()
        json_doc['folder']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[2]/td[2]')[0].text.strip()  
        json_doc['noConcesion']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[3]/td[2]')[0].text.strip()
        json_doc['oficioDate']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[4]/td[2]')[0].text.strip()
        json_doc['oficioNum']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[5]/td[2]')[0].text.strip()
        json_doc['url']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[6]/td[2]')[0].text.strip()
        json_doc['dateOnCirculation']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[7]/td[2]')[0].text.strip()
    if lsCasos[6]==gaceta:
        json_doc['folder']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[1]/td[2]')[0].text.strip()
        json_doc['featureDate']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[2]/td[2]')[0].text.strip()  
        json_doc['denomination']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[3]/td[2]')[0].text.strip()
        json_doc['class']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[4]/td[2]')[0].text.strip()
        json_doc['url']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[5]/td[2]')[0].text.strip()
        json_doc['dateOnCirculation']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[6]/td[2]')[0].text.strip()
    if lsCasos[7]==gaceta:    
        json_doc['branchreg']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[1]/td[2]')[0].text.strip()
        json_doc['dateConcesion']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[2]/td[2]')[0].text.strip()  
        json_doc['folder']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[3]/td[2]')[0].text.strip()
        json_doc['featureDate']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[4]/td[2]')[0].text.strip()
        json_doc['denomination']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[5]/td[2]')[0].text.strip()
        json_doc['class']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[6]/td[2]')[0].text.strip()
        json_doc['prodserv']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[7]/td[2]')[0].text.strip()
        json_doc['main']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[8]/td[2]')[0].text.strip()
        json_doc['dateOnCirculation']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[9]/td[2]')[0].text.strip()
    if lsCasos[8]==gaceta:
        json_doc['resolution']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[1]/td[2]')[0].text.strip()
        json_doc['branchreg']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[2]/td[2]')[0].text.strip()  
        json_doc['class']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[3]/td[2]')[0].text.strip()
        json_doc['denomination']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[4]/td[2]')[0].text.strip()
        json_doc['renewedUntil']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[5]/td[2]')[0].text.strip()
        json_doc['dateOnCirculation']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[6]/td[2]')[0].text.strip()
    if lsCasos[9]==gaceta:
        json_doc['folioexit']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[1]/td[2]')[0].text.strip()
        json_doc['dates']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[2]/td[2]')[0].text.strip()  
        json_doc['description']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[3]/td[2]')[0].text.strip()
        json_doc['pc']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[4]/td[2]')[0].text.strip()
        json_doc['actor']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[5]/td[2]')[0].text.strip()
        json_doc['demanded']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[6]/td[2]')[0].text.strip()
        json_doc['url']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[7]/td[2]')[0].text.strip()
        json_doc['dateOnCirculation']=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr[8]/td[2]')[0].text.strip()

    #Insert to DB
    query="select id from thesis.impi_docs_master where folder='"+json_doc['folder']+"' and gaceta='"+json_doc['gaceta']+"' and sample='"+json_doc['sample']+"' and section='"+json_doc['section']+"' ALLOW FILTERING ;"
    result=bd.returnQueryResult(query)   
    if result: 
        folder=json_doc['folder']
        print('Folder: ',folder, 'and Gaceta: ',gaceta, ' existed')
    else:
        lsRes=bd.insertarJSON('thesis.impi_docs_master',json_doc)      
        if lsRes[0]==True:
            print('Record added')    
            

"""
readPDF is done to read a PDF no matter the content, can be image or UTF-8 text
"""
def readPDF(file):  
    with open(download_dir+'/'+file, "rb") as pdf_file:
        bContent = base64.b64encode(pdf_file.read()).decode('utf-8')
    
    return bContent  
    

"""
This is the method to call when fetching the pdf enconded from cassandra which is a list of text
but that text is really bytes.
"""
def decodeFromBase64toNormalTxt(b64content):
    normarlText=base64.b64decode(b64content).decode('utf-8')
    return normarlText


def getPDFfromBase64(bContent):
    #Tutorial : https://base64.guru/developers/python/examples/decode-pdf
    bytes = base64.b64decode(bContent, validate=True)
    # Write the PDF contents to a local file
    f = open(download_dir+'/result.pdf', 'wb')
    f.write(bytes)
    f.close()
    return "PDF delivered!"

def TextOrImageFromBase64(bContent):
    #If sData got "EOF" is an image, otherwise is TEXT
    sData=str(bContent)
    if "EOF" in sData:
        res=getPDFfromBase64(bContent) 
    else:
        res=decodeFromBase64toNormalTxt(bContent)

    return res 

def devuelveJSON(jsonFile):
    with open(jsonFile) as json_file:
        jsonObj = json.load(json_file)
    
    return jsonObj 

def processPDF(json_sentencia,lsRes):
    lsContent=[]  
    for file in os.listdir(download_dir): 
        strFile=file.split('.')[1]
        if strFile=='PDF' or strFile=='pdf':
            strContent=readPDF(file) 
            print('Start wrapping text...') 
            lsContent=wrap(strContent,1000)  
            json_documento=devuelveJSON('/app/appimpi/json_documento.json')
            if lsRes[0]:
                json_documento['idDocumento']=json_sentencia['id']
            else:
                json_documento['idDocumento']=lsRes[1]

            json_documento['documento']=json_sentencia['document']
            json_documento['fuente']='impi'
            totalElements=len(lsContent)
            result=insertPDFChunks(0,0,0,totalElements,lsContent,json_documento,0)
            if result==False:
                print('PDF Ended!')       
           
        
def insertPDFChunks(startPos,contador,secuencia,totalElements,lsContent,json_documento,done):
    if done==0:
        json_documento['lspdfcontent'].clear()
        json_documento['id']=str(uuid.uuid4())
        for i in range(startPos,totalElements):
            if i!=totalElements-1:
                if contador<=20:
                    json_documento['lspdfcontent'].append(lsContent[i])
                    contador=contador+1
                else:
                    currentSeq=secuencia+1
                    json_documento['secuencia']=currentSeq
                    res=bd.insertPDF(json_documento) 
                    if res:
                        print('Chunk of pdf added:',str(i),'from ',str(totalElements),' sequence:',str(currentSeq))  
                    else:
                        print('Chunk of pdf already existed:',str(i),'from ',str(totalElements),' sequence:',str(currentSeq)) 

                    return insertPDFChunks(i,0,currentSeq,totalElements,lsContent,json_documento,0) 
            else:
                json_documento['lspdfcontent'].append(lsContent[i])
                currentSeq=secuencia+1
                json_documento['secuencia']=currentSeq
                res=bd.insertPDF(json_documento) 
                if res:
                    print('Last Chunk of pdf added:',str(i),'from ',str(totalElements),' sequence:',str(currentSeq))
                else:
                    print('Last Chunk of pdf already existed:',str(i),'from ',str(totalElements),' sequence:',str(currentSeq))

                return  insertPDFChunks(i,0,currentSeq,totalElements,lsContent,json_documento,1)
    else:
        return False            

                             
def readPyPDF(file):
    #This procedure produces a b'blabla' string, it has UTF-8
    #PDF files are stored as bytes. Therefore to read or write a PDF file you need to use rb or wb.
    lsContent=[]
    pdfFileObj = open(download_dir+'/'+file, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    pags=pdfReader.numPages
    for x in range(0,pags):
        pageObj = pdfReader.getPage(x)
        #UTF-8 is the right encodeing, I tried ascii and didn't work
        #1. bContent is the actual byte from pdf with utf-8, expected b'bla...'
        bcontent=base64.b64encode(pageObj.extractText().encode('utf-8'))
        lsContent.append(str(bcontent.decode('utf-8')))
                         
    pdfFileObj.close()    
    return lsContent                


def returnChromeSettings():
    chromedriver_autoinstaller.install()
    options = Options()
    profile = {"plugins.plugins_list": [{"enabled": True, "name": "Chrome PDF Viewer"}], # Disable Chrome's PDF Viewer
               "download.default_directory": download_dir , 
               "download.prompt_for_download": False,
               "download.directory_upgrade": True,
               "download.extensions_to_open": "applications/pdf",
               "plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
               }           

    options.add_experimental_option("prefs", profile)
    browser=webdriver.Chrome(options=options)  

    return browser   

def initialDownloadDirCheck():
    print('Checking if download folder exists...')
    isdir = os.path.isdir(download_dir)
    if isdir==False:
        print('Creating download folder...')
        os.mkdir(download_dir)
        print('Download directory created...')
    for file in os.listdir(download_dir):
        os.remove(download_dir+'/'+file)
        print('Download folder empty...')   

def devuelveElemento(xPath, browser):
    cEle=0
    while (cEle==0):
        cEle=len(browser.find_elements_by_xpath(xPath))
        if cEle>0:
            ele=browser.find_elements_by_xpath(xPath)[0]

    return ele                     