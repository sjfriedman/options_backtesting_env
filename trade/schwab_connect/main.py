"""Cloud Function entrypoint to refresh Schwab OAuth tokens.

This function:
- Reads the app key and secret from Secret Manager via helpers
- Reads the stored refresh_token from Firestore
- Calls the Schwab OAuth token endpoint to obtain new tokens
- Stores the new token JSON in Firestore for downstream clients

Expects Application Default Credentials and appropriate IAM roles.
"""

import os
from flask import Request
import base64
import requests
from loguru import logger

from helpers import retrieve_google_secret_dict, retrieve_firestore_value, store_firestore_value

cs_app_key_secret_dictionary = retrieve_google_secret_dict(gcp_id='schwab-447323', secret_id='cs-app-key')



def refresh_tokens(request):
    """HTTP handler for Google Cloud Functions to refresh tokens.

    The request object is not used. On success, writes the refreshed token
    dictionary to Firestore and returns a simple confirmation string.

    Parameters
    ----------
    request: flask.Request
        Unused request object provided by Cloud Functions runtime.

    Returns
    -------
    str | None
        "Done!" on success, or None on failure.
    """
    logger.info("Initializing...")

    app_key = cs_app_key_secret_dictionary['app-key']
    app_secret = cs_app_key_secret_dictionary['app-secret']

    # Retrieve the current refresh_token from Firestore
    refresh_token_value = retrieve_firestore_value(collection_id='schwab-tokens', document_id='schwab-tokens-auth', key='refresh_token')

    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token_value,
    }
    headers = {
        "Authorization": f'Basic {base64.b64encode(f"{app_key}:{app_secret}".encode()).decode()}',
        "Content-Type": "application/x-www-form-urlencoded",
    }

    refresh_token_response = requests.post(
        url="https://api.schwabapi.com/v1/oauth/token",
        headers=headers,
        data=payload,
    )
    if refresh_token_response.status_code == 200:
        logger.info("Retrieved new tokens successfully using refresh token.")
    else:
        logger.error(
            f"Error refreshing access token: {refresh_token_response.text}"
        )
        return None

    refresh_token_dict = refresh_token_response.json() 
 
    store_firestore_value(project_id='schwab-447323', collection_id='schwab-tokens', document_id='schwab-tokens-auth', value=refresh_token_dict)

    logger.info("Token dict refreshed.")

    return "Done!"


# functions-framework --target=refresh_tokens --source=main.py --debug