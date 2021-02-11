import os
import json

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account

ENV_TOKEN = 'GOOGLE_API_TOKEN'

def get_credentials(scopes, client_secrets_json_file = None, service_json_file = None):
    # Authenicate using service account json file if it exists
    if service_json_file:
        with open(service_json_file) as f:
            f_dict = json.load(f)
            client_email = f_dict['client_email']
            print(f"Authenticating using: {client_email}")
        return service_credentials(scopes, service_json_file)
    
    # Authenicate using environment variable stored user token if it exists
    if client_secrets_json_file:
        with open(client_secrets_json_file) as f:
            f_dict = json.load(f)
            client_id = f_dict['installed']['client_id']
            print(f"Authenticating using: {client_id}")
        return user_credentials(scopes, client_secrets_json_file)

    

def user_credentials(scopes, client_secrets_json_file = None):
    """Shows basic usage of the Docs API.
    Returns a Google .
    """
    credentials = None
    env_token = ENV_TOKEN
    env_user_token = 'GOOGLE_API_USER_TOKEN'
    # The environment variable stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.getenv(env_user_token):
        env_creds = json.loads(os.getenv(env_user_token))
        credentials = Credentials.from_authorized_user_info(env_creds)
        os.environ[env_token] = credentials.to_json()
    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_json_file, scopes)
            credentials = flow.run_console()
        # Save the credentials for the next run
        os.environ[env_user_token] = credentials.to_json()
        os.environ[env_token] = credentials.to_json()

    return credentials


def service_credentials(scopes, service_json_file):
    credentials = None
    env_token = ENV_TOKEN
    env_service_token = 'GOOGLE_API_SERVICE_TOKEN'
    # The environment variable stores the service account's access, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.getenv(env_service_token):
        env_creds = json.loads(os.getenv(env_service_token))
        credentials = service_account.Credentials.from_service_account_info(env_creds)
        os.environ[env_token] = credentials.to_json()
    # If there are no (valid) credentials available, let the service account log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired:
            credentials.refresh(Request())
        else:
            credentials = service_account.Credentials.from_service_account_file(service_json_file,scopes=scopes)
        # Save the credentials for the next run
        os.environ[env_service_token] = credentials.to_json()
        os.environ[env_token] = credentials.to_json()

    return credentials