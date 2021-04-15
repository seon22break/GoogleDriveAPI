# GoogleDriveAPI
Google Drive API es una característica propia del Google Drive que nos permite realizar funciones dentro de nuestro sistema de almacenamiento Drive. He creado esta clase con la única finalidad de facilitar a los usuarios el uso de esta API, cuyo ritmo de aprendizaje puede ser algo lento. 

# Instalation

* Instalación de las dependencias necesarias para Google Drive

```
 pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

```

* Descarga de credenciales. Esto permite a Google Drive la identificación de la cuenta.  LINK: <a href="https://developers.google.com/workspace/guides/create-project">Aquí</a>

* Importar la clase en mi archivo python. 
```
 from GoogleAPI import *
```

* Instanciar la clase con la ruta donde se encuentra el directorio. Esto permite al script ser ejecutado, siempre teniendo en cuenta cual es la ruta donde se encuentran el tocken y el archivo credentials. 

```
  google = GoogleAPI("/opt/lampp/htdocs/Backup-Drive")

```

* Y ahora solo quéda usarlo .... 

# Métodos disponibles
<table>
  <thead>
    <tr>
      <td>Método</td>
      <td>Parámetros necesarios</td>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>uploadFile</td>
      <td>String: FolderID , String : mimetype, String: filename</td>
    </tr>
    <tr>
      <td>downloadFile</td>
      <td>String: FolderID, String: filename</td>
    </tr>
    <tr>
      <td>getFilesInFolder</td>
      <td>String: FolderID</td>
    </tr>
    <tr>
      <td>renameFile</td>
      <td>String: FolderID, String: name</td>
    </tr>
  </tbody>
</table>
