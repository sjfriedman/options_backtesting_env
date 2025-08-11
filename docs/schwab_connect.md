### Schwab OAuth: Initialization and Token Refresh

This module provides an interactive initializer to capture the first Schwab OAuth tokens and a Google Cloud Function to refresh tokens using the stored `refresh_token`.

Components:

- `trade/schwab_connect/init_auth.py`: interactive initialization to exchange the authorization code for tokens and store them in Firestore.
- `trade/schwab_connect/main.py`: Cloud Function entrypoint `refresh_tokens` that refreshes tokens via the Schwab OAuth endpoint and updates Firestore.
- `trade/schwab_connect/helpers.py`: utilities for Google Secret Manager and Firestore.
- `trade/schwab_connect/requirements.txt`: dependencies for local dev and Cloud Functions runtime.
- `trade/schwab_connect/cloudbuild.yaml`: example Cloud Build config to deploy the function.


## Prerequisites

- GCP project with Secret Manager and Firestore enabled.
- Secret Manager secret `cs-app-key` with latest version containing JSON:

```json
{
  "app-key": "YOUR_SCHWAB_APP_KEY",
  "app-secret": "YOUR_SCHWAB_APP_SECRET"
}
```

- Firestore (Native mode) with collection `schwab-tokens` and document `schwab-tokens-auth`. The code will write the full token response to that document, including `refresh_token` and `access_token`.
- Application Default Credentials available locally (e.g., `gcloud auth application-default login`) or a service account with:
  - Secret Manager Secret Accessor
  - Cloud Datastore User

Note: Code refers to example project ID `schwab-447323`. Replace if needed.


## First-time token initialization (interactive)

1) Install dependencies and set up credentials:

```
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r trade/schwab_connect/requirements.txt
gcloud auth application-default login
```

2) Run the initializer entrypoint in `init_auth.py`:

```
cd trade/schwab_connect
python -c "import init_auth; print(init_auth.main(None))"
```

What happens:

- The script retrieves `app-key` and `app-secret` from Secret Manager.
- It prints and opens the Schwab authorization URL in your browser.
- After authenticating, copy the full returned URL and paste it into the terminal when prompted.
- The script exchanges the authorization code for tokens and writes the token JSON to Firestore at `schwab-tokens/schwab-tokens-auth`.


## Cloud Function: refresh tokens

Entrypoint: `refresh_tokens` in `trade/schwab_connect/main.py`.

Behavior:

- Fetches the current `refresh_token` from Firestore `schwab-tokens/schwab-tokens-auth`.
- Calls `https://api.schwabapi.com/v1/oauth/token` with `grant_type=refresh_token`.
- Stores the new token JSON back to Firestore (overwriting prior values).

Local run (optional):

```
cd trade/schwab_connect
pip install functions-framework
functions-framework --target=refresh_tokens --source=main.py --debug
```

Then POST to `http://127.0.0.1:8080/`.


## Deploying the Cloud Function

Option A: Use the provided Cloud Build config `cloudbuild.yaml` (recommended for CI):

```
gcloud builds submit --config=trade/schwab_connect/cloudbuild.yaml trade/schwab_connect
```

Option B: Direct deploy via gcloud:

```
cd trade/schwab_connect
gcloud functions deploy refresh_tokens \
  --gen2 \
  --runtime=python312 \
  --region=us-east1 \
  --source=. \
  --entry-point=refresh_tokens \
  --trigger-http \
  --memory=256MB \
  --timeout=90s \
  --min-instances=0 \
  --max-instances=1 \
  --allow-unauthenticated
```

Adjust auth, IAM, and network as needed.


## Scheduling automatic refreshes

Use Cloud Scheduler to hit the function HTTP endpoint periodically (e.g., every 30 minutes) to keep tokens fresh. Ensure the principal used by Scheduler can invoke the function (or make the function public only if appropriate).


## Data model in Firestore

Document path: `schwab-tokens/schwab-tokens-auth`

Example stored structure (actual fields depend on Schwab response):

```json
{
  "access_token": "...",
  "refresh_token": "...",
  "token_type": "Bearer",
  "expires_in": 900,
  "scope": "..."
}
```

The `refresh_tokens` function overwrites the document with the latest response each time it runs.


