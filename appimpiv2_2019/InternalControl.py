import os

class cInternalControl:
    idControl=11
    version='2019'
    timeout=70
    hfolder='appimpiv2_'+version 
    heroku=False
    rutaHeroku='/app/'+hfolder
    rutaLocal=os.getcwd()+'\\'+hfolder+'\\'
    download_dir='Download_'+hfolder
    enablePdf=False
    impi1=False
      