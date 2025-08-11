### Schwab Account Client (starter)

`trade/account_info/AccountsTrading.py` provides a minimal example for authenticated calls to the Schwab trading API.

Current capabilities:

- Initialize with an access token read from Firestore (you must implement the retrieval function or import it from `helpers.py`).
- Fetch the account hash value via `/trader/v1/accounts/accountNumbers`.


## Setup

Ensure you have run the Schwab OAuth initialization in `docs/schwab_connect.md` so Firestore contains a valid `access_token` (and your refresh flow is set up to keep it current).

Install dependencies used in your client code, for example:

```
pip install requests pandas google-cloud-firestore loguru
```


## Editing the example

The provided example includes placeholders you must replace:

- Firestore lookup keys: `collection_id`, `document_id`, `key` for your access token field
- Missing imports: add `requests`, `pandas`, and the Firestore helper you plan to use

Suggested changes in `AccountsTrading.py`:

1) Add imports at top:

```python
import requests
import pandas
from trade.schwab_connect.helpers import retrieve_firestore_value
```

2) Replace placeholders in `refresh_access_token` with your Firestore layout, e.g.:

```python
self.access_token = retrieve_firestore_value(
    collection_id="schwab-tokens",
    document_id="schwab-tokens-auth",
    key="access_token",
)
```

3) Instantiate and use:

```python
if __name__ == "__main__":
    accounts_trading = AccountsTrading()
    print(accounts_trading.account_hash_value)
```


## Notes

- Tokens expire quickly. Ensure your refresh Cloud Function is scheduled and that your client either pulls the latest `access_token` from Firestore before requests or handles 401s by reloading the token.
- For trading beyond account lookups, follow Schwab API docs for endpoints, request bodies, and permissions.


