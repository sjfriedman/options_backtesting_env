### Options Research and Schwab Trading Utilities

This repository contains:

- Backtesting notebooks for covered calls and related options strategies
- A lightweight publishing flow for a blog post and images
- A Google Cloud Function for refreshing Schwab API OAuth tokens, plus an interactive initializer
- A starter client for Schwab trading account lookups

Use this repo to experiment with options strategies, publish results, and integrate with the Schwab API for authenticated requests.


## Repository structure

```
options/
  backtest/                 # Jupyter notebooks for strategy research
  blog/                     # Blog notebook -> HTML export and images
  read_data/                # Raw EOD files and cleaned parquet data
  trade/
    account_info/           # Starter Schwab account client
    schwab_connect/         # Cloud Function + helpers for OAuth token refresh
  covered_call_leap.ipynb   # Top-level working notebook
  clean_data.ipynb          # Data cleaning/prep notebook
  blog.pdf                  # Pre-rendered blog PDF
```


## Quick start

1) Python environment

- Local notebooks were developed on Python 3.11 (see `venv/`).
- The Cloud Function deploys on Python 3.12 (see `trade/schwab_connect/cloudbuild.yaml`).

Recommended (macOS):

```
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r trade/schwab_connect/requirements.txt
```

2) Open notebooks

```
python -m pip install notebook jupyterlab pandas numpy matplotlib seaborn scipy scikit-learn pyarrow
jupyter lab
```

3) Explore docs

- See `docs/schwab_connect.md` for Schwab OAuth, token storage, and Cloud Function deploy.
- See `docs/accounts_trading.md` for the account client.
- See `docs/data_and_notebooks.md` for data layout and notebooks.
- See `docs/blog.md` for publishing the blog.


## Google Cloud prerequisites (for Schwab OAuth)

You will need:

- A GCP project (example used in code: `schwab-447323`)
- Secret Manager enabled, with secret `cs-app-key` containing JSON:

```
{
  "app-key": "YOUR_SCHWAB_APP_KEY",
  "app-secret": "YOUR_SCHWAB_APP_SECRET"
}
```

- Firestore (Native mode) with collection `schwab-tokens` and document `schwab-tokens-auth` to store tokens. The code will write the entire token JSON response to that document, including `refresh_token` and `access_token`.
- Application Default Credentials locally (e.g., `gcloud auth application-default login`) or a service account for deployments.

Details are in `docs/schwab_connect.md` and `docs/deployment.md`.


## Components

- Backtesting notebooks: strategy research and performance visualizations. See `backtest/` and the top-level `covered_call_leap.ipynb`.
- Data: raw EOD text files under `read_data/data/raw/` and cleaned parquet outputs under `read_data/data/clean/`. See `docs/data_and_notebooks.md`.
- Schwab OAuth utilities: Cloud Function `refresh_tokens` and an interactive initializer to capture the first tokens into Firestore. See `trade/schwab_connect/` and `docs/schwab_connect.md`.
- Account client: `trade/account_info/AccountsTrading.py` is a starter client that retrieves the account hash value once an access token is available. See `docs/accounts_trading.md`.


## Security notes

- Do not commit real credentials, refresh tokens, or access tokens. Store secrets in GCP Secret Manager and tokens in Firestore, as implemented.
- Restrict Cloud Function invocation and service account permissions to least privilege.


## Troubleshooting

- Token refresh failing: ensure the Firestore document `schwab-tokens/schwab-tokens-auth` has a valid `refresh_token`, and that the Secret Manager secret `cs-app-key` has correct `app-key`/`app-secret`.
- Firestore/Secret Manager access: verify ADC is configured (`gcloud auth application-default login`) and the principal has roles `Secret Manager Secret Accessor` and `Cloud Datastore User`.
- Code import issues in the account client: see `docs/accounts_trading.md` for required imports and placeholders to replace.


## License

Proprietary (default). If you intend to open-source, add a LICENSE file and update this section.


