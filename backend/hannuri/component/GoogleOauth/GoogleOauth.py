from pathlib import Path
import os
import requests
import google_auth_oauthlib.flow

class GoogleOauth:
    def __init__(self):
        self.secret_path = os.path.join(Path(__file__).parent.absolute(), 'secret', 'client_secret.json')
        pass

    def get_user_email(self, code, redirect_url):
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            self.secret_path,
            scopes = 'openid https://www.googleapis.com/auth/userinfo.email'
        )
        flow.redirect_uri = redirect_url
        flow.fetch_token(code=code)
        token = flow.credentials.token
        response = requests.get(f'https://www.googleapis.com/oauth2/v1/userinfo?access_token={token}')
        return response.json()['email']
