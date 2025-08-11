### Deployment guide

This guide covers local development setup and deploying the Schwab token refresh function to Google Cloud.


## Local development

1) Python environment:

```
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r trade/schwab_connect/requirements.txt
```

2) Google credentials:

```
gcloud auth login
gcloud auth application-default login
```

Ensure your ADC principal has access to Secret Manager and Firestore.

3) Initialize tokens interactively (first-time only):

```
python -c "import trade.schwab_connect.init_auth as ia; print(ia.main(None))"
```

4) Run the refresh function locally (optional):

```
cd trade/schwab_connect
functions-framework --target=refresh_tokens --source=main.py --debug
```


## Cloud Function deploy (Gen 2)

Prereqs:

- APIs enabled: Cloud Functions, Cloud Build, Secret Manager, Firestore, Cloud Run, Artifact Registry
- Service account with roles: Cloud Functions Developer, Cloud Build Editor, Secret Manager Secret Accessor, Cloud Datastore User (adjust per org policy)

Option A: Cloud Build (CI)

```
gcloud builds submit --config=trade/schwab_connect/cloudbuild.yaml trade/schwab_connect
```

Option B: Direct deploy

```
gcloud functions deploy refresh_tokens \
  --gen2 \
  --runtime=python312 \
  --region=us-east1 \
  --source=trade/schwab_connect \
  --entry-point=refresh_tokens \
  --trigger-http \
  --memory=256MB \
  --timeout=90s \
  --min-instances=0 \
  --max-instances=1
```

Note: Consider removing `--allow-unauthenticated` and securing invocation via IAM or a signed URL.


## Scheduler

Create a Cloud Scheduler job that hits the function URL on a cadence (e.g., every 15–30 minutes) to keep tokens fresh.

Example:

```
gcloud scheduler jobs create http refresh-schwab-tokens \
  --schedule="*/30 * * * *" \
  --uri="https://REGION-PROJECT.cloudfunctions.net/refresh_tokens" \
  --http-method=GET \
  --oidc-service-account-email=YOUR_INVOKER_SA@PROJECT.iam.gserviceaccount.com
```


