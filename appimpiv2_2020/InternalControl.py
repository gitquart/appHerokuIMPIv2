import os

class cInternalControl:
    idControl=12
    version='2020'
    timeout=70
    hfolder='appimpiv2_'+version 
    heroku=False
    rutaHeroku='/app/'+hfolder
    rutaLocal=os.getcwd()+'\\'+hfolder+'\\'
    download_dir='Download_'+hfolder
    enablePdf=False
    impi1=False
      