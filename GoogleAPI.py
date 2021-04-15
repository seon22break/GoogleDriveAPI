#!/usr/bin/python3
# encoding: utf-8

import os
import pickle
import os.path
import io
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient import errors

class GoogleAPI:
    def __init__(self,path):

        SCOPES = ['https://www.googleapis.com/auth/drive']

        super().__init__()

        # Establecemos las rutas absolutas de los ficheros necesarios
        # para la autenticacion
        tokenFile = path+"/token.pickle"
        credentialsFile = path+"/credentials.json"
        # Si no existe el fichero Token, realizamos la conexion
        if os.path.exists(tokenFile):
            with open(tokenFile, 'rb') as token:
                creds = pickle.load(token)
        
            # Si no existen unas credenciales válidas
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                    credentialsFile, SCOPES)
                    creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open(tokenFile, 'wb') as token:
                    pickle.dump(creds, token)
            
            self.service = build('drive', 'v3', credentials=creds)
    
    def getFilesInFolder(self,folderId):
            # Call the Drive v3 API
            query="'%s' in parents" % folderId
            results = self.service.files().list(q=query, pageSize=199, spaces='drive',fields="nextPageToken, files(id, name,parents,size)").execute()
            items = results.get('files', [])
            return items
    
    def downloadFile(self,fileID : str ,filename : str):
        #Hacemos una solicitud a la API de Google Drive para pedir el fichero que queremos descargar 
            
        request = self.service.files().get_media(fileId=fileID)

        fh = io.FileIO(filename, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
    
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))

    def uploadFile(self,folderUploadId : str , mimetype : str, filename : str):
        # Folder where upload files
        body = {'name': filename, 'mimeType': mimetype,"parents":[folderUploadId]}

        media = MediaFileUpload(filename, mimetype=mimetype,resumable=True)
        
        fiahl = self.service.files().create(body=body, media_body=media)
        
        response = None
        while response is None:
            status, response = fiahl.next_chunk()
            if status:
                print("Uploaded %d%%." % int(status.progress() * 100))
        print('Upload File: %s' % filename)

    def renameFile(self,folderID,name):
        body = {'name': name}
        try:
            self.service.files().update(fileId=folderID,body=body).execute()
        except:
            print("PUTO ERROR")
