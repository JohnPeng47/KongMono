from __future__ import print_function

import os
import pickle

from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from apiclient import discovery
from httplib2 import Http

CLIENT_SECRETS_FILE = 'client_secrets_web.json'  # Update this with your client_secrets.json file location
SCOPES = ['https://www.googleapis.com/auth/forms.body']
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"
TOKEN_FILE = 'token.pickle'

creds = None

# The file token.pickle stores the user's access and refresh tokens.
# Check if the file exists and load the credentials.
if os.path.exists(TOKEN_FILE):
    with open(TOKEN_FILE, 'rb') as token:
        creds = pickle.load(token)

# If there are no (valid) credentials available, let the user log in.
# if not creds or not creds.valid:
#     if creds and creds.expired and creds.refresh_token:
#         print("Refereshing creds..")
#         creds.refresh(Request())
#     else:
#         print(creds)
#         print("Generating new oauth request...")
#         # Use the client_secrets.json file to identify the application requesting
#         # authorization. The client ID (from that file) and access scopes are required.
#         flow = Flow.from_client_secrets_file(
#             CLIENT_SECRETS_FILE,
#             scopes=SCOPES,
#             # Specify the URI to redirect to after the user completes the authorization flow.
#             redirect_uri='https://learnwithkong.com/oauth-redirect'  # Update this with your actual redirect URI
#         )
        
#         # Generate URL for request to Google's OAuth 2.0 server.
#         # User will be prompted to follow this URL and complete the authorization flow.
#         auth_url, _ = flow.authorization_url(
#             # Enable offline access so that you can refresh an access token without
#             # re-prompting the user for permission. Recommended for web server apps.
#             access_type='offline',
#             # Enable incremental authorization. Recommended as a best practice.
#             include_granted_scopes='true'
#         )
#         print("AuthURL: ", auth_url)

        
form_service = build('forms', 'v1', credentials=creds, discoveryServiceUrl=DISCOVERY_DOC, static_discovery=False)

# Request body for creating a form
NEW_FORM = {
    "info": {
        "title": "Quickstart form",
    }
}

# Request body to add a multiple-choice question
NEW_QUESTION = {
    "requests": [{
        "createItem": {
            "item": {
                "title": "Why are you gay?",
                "questionItem": {
                    "question": {
                        "required": True,
                        "choiceQuestion": {
                            "type": "RADIO",
                            "options": [
                                {"value": "1965"},
                                {"value": "1967"},
                                {"value": "1969"},
                                {"value": "1971"}
                            ],
                            "shuffle": True
                        }
                    }
                },
            },
            "location": {
                "index": 0
            }
        }
    }]
}

# Creates the initial form
result = form_service.forms().create(body=NEW_FORM).execute()

# Adds the question to the form
question_setting = form_service.forms().batchUpdate(formId=result["formId"], body=NEW_QUESTION).execute()

# Prints the result to show the question has been added
get_result = form_service.forms().get(formId=result["formId"]).execute()
print(get_result)