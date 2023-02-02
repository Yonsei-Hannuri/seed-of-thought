import os
import requests
import json
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

def validateResponse(response):
    if response.status_code == 500:
        googlErrorNotification = "구글 드라이브 사용자 등록 중 에러가 발생했습니다. 이메일이 정확한지 확인해주세요."
        raise Exception(googlErrorNotification + "\n" +json.loads(response.text)['error']['message'])


def getCreds():
    SCOPES = ['https://www.googleapis.com/auth/drive']
    creds = None
    #The file token.json stores the user's access and refresh tokens, and is 
    #created automatically when the authorization flow completes for the first time.None
    if os.path.exists('./token.json'):
        creds = Credentials.from_authorized_user_file('./token.json', SCOPES)
    #If there are no valid credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else: 
            raise Exception("구글 드라이브 인증 중에서 에러가 발생했습니다. 구글 드라이브 토큰이 만료되었습니다. 개발자에게 대응을 요청하세요")
        with open('./token.json', 'w') as token:
            token.write(creds.to_json())

    return creds


def registerReader(email, folderId):
    creds = getCreds()
    access_token = json.loads(creds.to_json())['token']
    headers = {"Authorization": "Bearer "+access_token, "Content-Type": "application/json"}
    params = {
            'role': 'reader', 
            'type': 'user',
            'emailAddress': email,
        }
    r = requests.post(
        "https://www.googleapis.com/drive/v3/files/{}/permissions".format(folderId),
        headers=headers,
        data=json.dumps(params)
    )
    validateResponse(r);
    permissionId = json.loads(r.text)['id']
    return permissionId

def registerWriter(email, folderId):
    creds = getCreds()
    access_token = json.loads(creds.to_json())['token']
    headers = {"Authorization": "Bearer "+access_token, "Content-Type": "application/json"}
    params = {
            'role': 'writer', 
            'type': 'user',
            'emailAddress': email,
        }
    r = requests.post(
        "https://www.googleapis.com/drive/v3/files/{}/permissions".format(folderId),
        headers=headers,
        data=json.dumps(params)
    )
    validateResponse(r);
    permissionId = json.loads(r.text)['id']
    return permissionId

def deleteMember(permissionId, folderId):
    creds = getCreds()
    access_token = json.loads(creds.to_json())['token']

    headers = {"Authorization": "Bearer "+access_token, "Content-Type": "application/json"}

    r = requests.delete(
        "https://www.googleapis.com/drive/v3/files/{}/permissions/{}".format(folderId, permissionId),
        headers=headers,
    )
    return r

def savePDF(fileName, parentFolderId, PDF, mimeType="application/pdf"):
    creds = getCreds()
    access_token = json.loads(creds.to_json())['token']

    headers = {"Authorization": "Bearer "+access_token, "Content-Type": "application/json"}

    params = {
        "name": fileName,
        "parents": [parentFolderId],
        "mimeType": mimeType,
    }
    r = requests.post(
        "https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable",
        headers=headers,
        data=json.dumps(params)
    )
    location = r.headers['Location']

    # 2. Upload the file
    blob = PDF.read()
    size = len(blob) #이런 방식으로 사이즈를 확인하는게 괜찮은지(성능적으로)? 또 큰 파일도 잘 다룰수 있는지?

    headers = {"Content-Range": "bytes 0-" + str(size-1) + "/" + str(size)}
    r = requests.put(
        location,
        headers=headers,
        data = PDF
    )
    result = json.loads(r.text)
    googleId = result['id']

    return googleId

def deletePDF(googleId):
    creds = getCreds()
    access_token = json.loads(creds.to_json())['token']

    headers = {"Authorization": "Bearer "+access_token}
    response = requests.delete(
        "https://www.googleapis.com/drive/v3/files/fileId/?fileId={}".format(googleId),
        headers=headers,
    )
    
    return response