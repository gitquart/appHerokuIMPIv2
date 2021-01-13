import os

class cInternalControl:
    idControl=10
    timeout=70
    hfolder='appimpiv2' 
    heroku=False
    rutaHeroku='/app/'+hfolder
    rutaLocal=os.getcwd()+'\\'+hfolder+'\\'
    download_dir='Download_impi2'
    enablePdf=False
      