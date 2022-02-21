import googleapiclient.discovery
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload
from io import BytesIO
from json import loads
from os import getenv

# google drive api setup snippet
scopes = ['https://www.googleapis.com/auth/drive']

with open('dbt-service-account.json') as f:
  lnes = f.readlines()
sc_creds = ''.join(lnes)
service_account_file = loads(sc_creds)
credentials = service_account.Credentials.from_service_account_info(
              service_account_file, scopes=scopes)
drive = googleapiclient.discovery.build('drive', 'v3', credentials=credentials)


def download_folder(folder_id):
    files = drive.files().list(q="'{}' in parents".format(folder_id)).execute().get('files', [])
    if files is []:
        print('google drive api returned empty folder, check api or permissions')
    else:
        print('google drive files found, downloading')
        for file in files:
            if file.get('id', None) is None or file.get('name', None) is None:
                continue
            print('downloading audio file: ' + file.get('name'))
            req = self.drive.files().get_media(fileId=file.get('id'))
            fh = BytesIO()
            downloader = MediaIoBaseDownload(fh, req)
            done = False
            while not done:
                (_, done) = downloader.next_chunk()
            with open(file.get('name'), 'wb') as audio_file:
                audio_file.write(fh.getbuffer())
                
download_folder('1rGM3x4wlxAm0HoJ-P6Oe2_R-ZQ6siruL')
