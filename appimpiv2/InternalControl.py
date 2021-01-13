import os

class cInternalControl:
    idControl=10
    timeout=70
    hfolder='appimpiv2' 
    heroku=True
    rutaHeroku='/app/'+hfolder
    rutaLocal=os.getcwd()+'\\'+hfolder+'\\'
    download_dir='Download_impiv2'
    enablePdf=False
    impi1=False
      