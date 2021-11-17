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
from google.oauth2.credentials import Credentials


class GoogleAPI:
    def __init__(self,path):

        SCOPES = ['https://www.googleapis.com/auth/drive']

        super().__init__()
        creds = None
   
        # Si no existe el fichero Token, realizamos la conexion
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        
        # Si no existen unas credenciales válidas
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", 'w') as token:
                token.write(creds.to_json())
            
            
        self.service = build('drive', 'v3', credentials=creds)
    
    def getFilesInFolder(self,folderId):
            # Call the Drive v3 API
            query="'%s' in parents" % folderId
            results = self.service.files().list(q=query, pageSize=199, spaces='drive',fields="nextPageToken, files(id, name,parents,size)").execute()
            items = results.get('files', [])
            return items
    
    def downloadFile(self,fileID : str ,filename : str,mime:str,typeProcess:str):
        #Hacemos una solicitud a la API de Google Drive para pedir el fichero que queremos descargar
        if typeProcess == 'default':
            request = self.service.files().export_media(fileId=fileID, mimeType=mime)
        else:
            request = self.service.files().get_media(fileId=fileID)

        fh = io.FileIO(filename, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()

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

    def findFolder(self,folderFind:str):
        page_token = None
        while True:
            response = self.service.files().list(q="name='"+folderFind+"'",
                                                spaces='drive',
                                                fields='nextPageToken, files(id, name)',
                                                pageToken=page_token).execute()
            for file in response.get('files', []):
                if file.get('name') == folderFind:
                    # Process change
                    return file

            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
