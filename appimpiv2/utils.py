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
import datetime


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

lsWebField=[
            'Oficina, No de Patente y Tipo de documento',
            'Tipo de documento',
            'Fecha de concesión',
            'Número de solicitud',
            'Expediente',
            'Fecha de presentación',
            'Número de solicitud internacional',
            'Fecha de presentación internacional',
            'Número de publicación internacional',
            'Fecha de publicación internacional',
            'Inventor(es)',
            'Titular',
            'Agente',
            'Clasificación CIP',
            'Título',
            'Resumen',
            'Fecha de Puesta en Circulación',
            'Solicitante(s)',
            'Clasificación CPC',
            'Prioridad (es)',
            'Denominación',
            'Clase',
            'URL',
            'Número del Oficio',
            'Registro de Marca',
            'Productos y Servicios',
            'Datos del Titular',
            'Resolución',
            'Renovada Hasta',
            'Locarno',
            'Licenciatario',
            'URL publicación',
            'Descripción general del asunto',
            'Fecha del Oficio',
            'Enlace electrónico',
            'Nuevo Titular',
            'Set',
            'Número de concesión',
            'Divisional',
            'Divisional de'
        
        ]

def appendInfoToFile(path,filename,strcontent):
    txtFile=open(path+filename,'a+')
    txtFile.write(strcontent)
    txtFile.close()


def processRows(browser,row,folder,totalRows):

    gaceta=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':j_idt68"]/thead/tr/td[2]')[0].text
    sample=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':j_idt68"]/thead/tr/td[3]')[0].text
    section=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':j_idt68"]/thead/tr/td[4]')[0].text

    gaceta=str(gaceta).split(':')[1].strip()
    sample=str(sample).split(':')[1].strip()
    section=str(section).split(':')[1].strip()
    
    json_doc=devuelveJSON('/app/appimpiv2/json_file.json')
    json_doc['lsnewfields'].clear()
    json_doc['id']=str(uuid.uuid4())
    json_doc['gaceta']=gaceta
    json_doc['sample']=sample
    year=sample.split(' ')[2]
    json_doc['section']=section
    json_doc['year']=int(year)

    numTablaDetalles=len(browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr'))
    #Start reading details
    if gaceta in lsCasos:
        processCase(json_doc,gaceta,browser,row,numTablaDetalles,folder,totalRows)
    else:
        print('--------------------------------------------')  
        print('Caso: ',gaceta,' no existe')
        os.sys.exit(0)  



def checkField(row,numDetalles,browser,json_doc,folder):
    for i in range(1,numDetalles+1):
        lblField=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr['+str(i)+']/td[1]')[0].text.strip()
        valField=browser.find_elements_by_xpath('//*[@id="busquedaSimpleForm:tabla:'+str(row)+':subTabla_data"]/tr['+str(i)+']/td[2]')[0].text.strip()
        valField=valField.replace("'"," ")
        
        if lblField in lsWebField:
            if lblField=='Oficina, No de Patente y Tipo de documento':
                json_doc['officePatentTypeDoc']=valField
                continue
            if lblField=='Tipo de documento':
                json_doc['typeDoc']=valField
                continue
            if lblField=='Fecha de concesión':
                json_doc['dateConcesion']=valField
                continue
            if lblField=='Número de solicitud' or lblField=='Expediente':
                json_doc['folder']=valField
                continue
            if lblField=='Fecha de presentación':
                json_doc['featureDate']=valField
                continue
            if lblField=='Número de solicitud internacional':
                json_doc['internatFolderNum']=valField
                continue
            if lblField=='Fecha de presentación internacional':
                json_doc['internatDateFeature']=valField
                continue      
            if lblField=='Número de publicación internacional':
                json_doc['internatPubNum']=valField
                continue
            if lblField=='Fecha de publicación internacional':
                json_doc['internatPubDate']=valField
                continue
            if lblField=='Inventor(es)':
                json_doc['inventor']=valField
                continue
            if lblField=='Titular' or lblField=='Nuevo Titular':
                json_doc['main']=valField
                continue
            if lblField=='Agente':
                json_doc['agent']=valField
                continue
            if lblField=='Clasificación CIP':
                json_doc['cip']=valField
                continue
            if lblField=='Título':
                json_doc['title']=valField
                continue
            if lblField=='Resumen':
                json_doc['summary']=valField
                continue
            if lblField=='Fecha de Puesta en Circulación':
                json_doc['dateOnCirculation']=valField
                continue
            if lblField=='Solicitante(s)':
                json_doc['requester']=valField
                continue
            if lblField=='Clasificación CPC':
                json_doc['cpc']=valField
                continue
            if lblField=='Prioridad (es)':
                json_doc['priority']=valField
                continue  
            if lblField=='Denominación':
                json_doc['denomination']=valField
                continue
            if lblField=='Clase':
                json_doc['class']=valField
                continue
            if lblField=='URL' or lblField=='URL publicación' or lblField=='Enlace electrónico':
                json_doc['url']=valField 
                continue      
            if lblField=='Número del Oficio':  
                json_doc['oficioNum']=valField
                continue
            if lblField=='Registro de Marca':
                json_doc['branchreg']=valField 
                continue 
            if lblField=='Productos y Servicios':
                json_doc['prodserv']=valField
                continue
            if lblField=='Datos del Titular':
                json_doc['mainData']=valField
                continue  
            if lblField=='Resolución':
                json_doc['resolution']=valField
                continue
            if lblField=='Renovada Hasta':
                json_doc['renewedUntil']=valField
                continue   
            if lblField=='Locarno':   
                json_doc['locarno']=valField
                continue
            if lblField=='Licenciatario':
                json_doc['licenciatario']=valField
                continue   
            if lblField=='Descripción general del asunto':
                json_doc['description']=valField
                continue
            if lblField=='Fecha del Oficio':
                json_doc['oficioDate']=valField
                continue
            if lblField=='Set':
                json_doc['cset']=valField
                continue 
            if lblField=='Número de concesión':
                json_doc['noConcesion']=valField
                continue
            if lblField=='Divisional':
                json_doc['divisional']=valField
                continue 
            if lblField=='Divisional de':
                json_doc['divisional_de']=valField
                continue

        else:   
            json_doc['lsnewfields'].add('Field:',str(lblField),'->Value:',str(valField))
            print('-----------------------------------------------')
            print('NOT Found label: ',lblField, 'with :',folder)
            print('These NOT found label and values are stored in lsnewfields in cassandra')
            print('------The program has ended-------------------------')
            os.sys.exit(0)




def processCase(json_doc,gaceta,browser,row,numDetalles,folder,totalRows):
    if lsCasos[0]==gaceta:
        checkField(row,numDetalles,browser,json_doc,folder)
    if lsCasos[1]==gaceta:
        checkField(row,numDetalles,browser,json_doc,folder)    
    if lsCasos[2]==gaceta:
        checkField(row,numDetalles,browser,json_doc,folder)
    if lsCasos[3]==gaceta:
        checkField(row,numDetalles,browser,json_doc,folder)
    if lsCasos[4]==gaceta:
        checkField(row,numDetalles,browser,json_doc,folder)
    if lsCasos[5]==gaceta:
        checkField(row,numDetalles,browser,json_doc,folder)
    if lsCasos[6]==gaceta:
        checkField(row,numDetalles,browser,json_doc,folder)
    if lsCasos[7]==gaceta:
        checkField(row,numDetalles,browser,json_doc,folder)    
    if lsCasos[8]==gaceta:
        checkField(row,numDetalles,browser,json_doc,folder)
    if lsCasos[9]==gaceta:
        checkField(row,numDetalles,browser,json_doc,folder)

    #Insert to DB
    rowSec=row+1
    query="select id from thesis.impi_docs_master where folder='"+json_doc['folder']+"' and gaceta='"+json_doc['gaceta']+"' and sample='"+json_doc['sample']+"' and section='"+json_doc['section']+"' and secuencia="+str(rowSec)+" ALLOW FILTERING ;"
    result=bd.returnQueryResult(query)   
    if result: 
        folder=json_doc['folder']
        print('Folder: ',folder, 'and Gaceta: ',gaceta, ' existed')
    else:
        lsRes=bd.insertarJSON('thesis.impi_docs_master',json_doc)      
        if lsRes[0]==True:
            print('Record added')
        
    #Check if the total of Rows are done, then update inimp1=1
    if rowSec==totalRows:
        print('Total rows:',str(totalRows),' and current Row:',str(rowSec))
        res=bd.returnQueryResult("select id from thesis.impi_docs where folder='"+str(folder)+"' ALLOW FILTERING") 
        if res:
            for row in res:
                strid=str(row[0])   
                res=bd.returnQueryResult('update thesis.impi_docs set inimpi2=1 where id='+strid)
                print('Folder:',folder,' updated with inimpi2=1 in impi_docs (impi1)')
                        
               
            

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

def getTime():
    return datetime.datetime.now() 

def getDifferenceInMinutes(startTime,endTime):
    time_delta=endTime-startTime
    totalSecond=time_delta.total_seconds()
    minutes=totalSecond/60 

    return minutes                         