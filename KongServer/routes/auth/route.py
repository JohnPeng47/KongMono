from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.requests import Request

from google_auth_oauthlib.flow import Flow

from .schema import User, AuthenticateRequest
from .db import create_db_user
from .utils import create_access_token

from typing import List

router = APIRouter()


@router.post("/user/")
def create_user(user: User):
    result = create_db_user(user)
    if result.inserted_id:
        # Generate token
        access_token = create_access_token(user.username)

        response = JSONResponse(
            content={"msg": "User created successfully"}, status_code=status.HTTP_201_CREATED)
        # Set token as a cookie
        response.set_cookie(key="access_token",
                            value=access_token, httponly=True)

        return response
    else:
        raise HTTPException(
            status_code=500, detail="An error occurred while inserting the user.")


@router.post("/authenticate/")
def authenticate_user(request: AuthenticateRequest):
    return {"token": create_access_token(request.username)}

from starlette.responses import RedirectResponse

@router.get("/oauth-redirect")
async def oauth_redirect(request: Request):
    # The OAuth provider should have sent a code as a query parameter
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Missing code parameter")

    try:
        # Now we'll create the flow again but we'll add the received code
        flow = Flow.from_client_secrets_file(
            'client_secrets_web.json',  # The file with your client secrets
            scopes=["https://www.googleapis.com/auth/forms.body"],  # The scopes you requested
            redirect_uri="https://learnwithkong.com/oauth-redirect"  # Make sure this matches your application's redirect URI
        )

        # We'll exchange the code for a token
        flow.fetch_token(code=code)

        # Now you have the credentials, you can save them to a secure place
        credentials = flow.credentials

        # Serialize the credentials and save them to a secure place like a database
        # Here's a simple example using pickle, but you should encrypt this data in production
        import pickle
        with open("token.pickle", "wb") as token_file:
            pickle.dump(credentials, token_file)

        # Redirect the user to the page where you want them after the process is complete
        return RedirectResponse(url="/success")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
