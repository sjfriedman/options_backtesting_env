"""Helper utilities for Google Secret Manager and Firestore.

This module provides small, focused functions for:
- Retrieving a JSON secret from Secret Manager and returning it as a dict
- Reading a single value from a Firestore document by key
- Storing a JSON-serializable value to a Firestore document

All functions assume Application Default Credentials are available and the
caller has appropriate IAM permissions.
"""

from loguru import logger
import json
from google.cloud import secretmanager, firestore

def retrieve_google_secret_dict(gcp_id, secret_id, version_id="latest") -> dict:
    """Return a secret value from Secret Manager as a Python dict.

    Parameters
    ----------
    gcp_id: str
        Google Cloud project ID that holds the secret.
    secret_id: str
        Secret name in Secret Manager.
    version_id: str, optional
        Secret version to access, defaults to "latest".

    Returns
    -------
    dict
        Parsed JSON content of the secret.
    """
    client = secretmanager.SecretManagerServiceClient()

    name = f"projects/{gcp_id}/secrets/{secret_id}/versions/{version_id}"

    secret_response = client.access_secret_version(request={"name": name})

    secret_string = secret_response.payload.data.decode("UTF-8")

    secret_dict = json.loads(secret_string)

    logger.debug(f"Retrieved {version_id} secret value for {secret_id}.")

    return secret_dict

def retrieve_firestore_value(collection_id, document_id, key) -> str:
    """Read a single field value from a Firestore document.

    Parameters
    ----------
    collection_id: str
        Firestore collection name.
    document_id: str
        Firestore document ID within the collection.
    key: str
        The field to retrieve from the document.

    Returns
    -------
    str | None
        The field value if present, otherwise None.
    """
    db = firestore.Client()

    try:
        document = db.collection(collection_id).document(document_id)

        doc = document.get()

        if doc.exists:
            logger.debug(f"Successfully retrieved {key} value.")
            return doc.get(key)

        else:
            logger.error(f"Failed to retrieve {key} value")

    except Exception as e:

        logger.error(f"Failed to retrieve {key} value")

        return None

def store_firestore_value(project_id, collection_id, document_id, value):
    """Write a JSON-serializable value to a Firestore document.

    If the document does not exist, it will be created. Existing fields are
    overwritten by the provided value.

    Parameters
    ----------
    project_id: str
        Google Cloud project ID.
    collection_id: str
        Firestore collection name.
    document_id: str
        Firestore document ID within the collection.
    value: Any
        JSON-serializable content to store.
    """
    db = firestore.Client(project=project_id)

    collection = db.collection(collection_id)

    document = collection.document(document_id)

    document.set(value)

    logger.debug(f"Updated {document_id} value.")
