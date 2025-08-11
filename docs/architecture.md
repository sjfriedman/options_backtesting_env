### Architecture overview

High-level components:

- Research and analytics via Jupyter notebooks over local parquet data
- Schwab OAuth utilities for obtaining and refreshing tokens
- Google Cloud managed services (Secret Manager, Firestore, Cloud Functions, optionally Cloud Scheduler)


## Data flow

1) Raw vendor EOD files live under `read_data/data/raw/`.
2) Cleaning notebooks produce parquet outputs under `read_data/data/clean/`.
3) Backtesting notebooks read parquet data and compute metrics/plots.
4) Blog notebook renders results and exports HTML/PDF with images.


## OAuth and token management

- Secrets: Schwab `app-key` and `app-secret` are stored as JSON in Secret Manager secret `cs-app-key`.
- Initialization: `init_auth.py` opens the authorization URL, the user pastes back the returned URL, and tokens are stored in Firestore `schwab-tokens/schwab-tokens-auth`.
- Refresh: Cloud Function `refresh_tokens` uses the stored `refresh_token` to fetch a new token set and overwrite the Firestore document.
- Consumption: clients (e.g., `AccountsTrading.py`) read `access_token` from Firestore prior to making API requests.


## Security considerations

- Do not store credentials in code or environment variables checked into VCS. Use Secret Manager and Firestore.
- Limit IAM permissions and follow least privilege for service accounts.
- Consider VPC egress and private access if calling external APIs from controlled environments.


