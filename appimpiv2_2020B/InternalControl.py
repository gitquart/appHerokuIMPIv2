import os

class cInternalControl:
    idControl=3
    version='2020B'
    timeout=70
    hfolder='appimpiv2_'+version 
    heroku=True
    rutaHeroku='/app/'+hfolder
    rutaLocal=os.getcwd()+'\\'+hfolder+'\\'
    download_dir='Download_'+hfolder
    enablePdf=False
    impi1=False
      