"""Minimal Schwab account client example.

This module shows how to:
- Load an access token from Firestore
- Call the Schwab account numbers endpoint
- Extract the first account hash value for subsequent requests

Replace the placeholder Firestore keys with your actual collection/document
names and field key for the access token. Ensure your token refresh flow keeps
the `access_token` up to date in Firestore.
"""

import requests
import pandas
from trade.schwab_connect.helpers import retrieve_firestore_value

class AccountsTrading:
    def __init__(self):
        """Initialize client, load token, and fetch account hash value."""
        self.access_token = None
        self.account_hash_value = None
        self.refresh_access_token()
        self.base_url = "https://api.schwabapi.com/trader/v1"
        self.headers = {"Authorization": f"Bearer {self.access_token}"}
        self.get_account_number_hash_value()

    def refresh_access_token(self):
        """Load the latest access token from Firestore."""
        self.access_token = retrieve_firestore_value(
            collection_id="schwab-tokens",
            document_id="schwab-tokens-auth",
            key="access_token",
        )

    def get_account_number_hash_value(self):
        """Fetch the account hash value using the authenticated request."""
        response = requests.get(
            self.base_url + f"/accounts/accountNumbers", headers=self.headers
        )
        response_frame = pandas.json_normalize(response.json())
        self.account_hash_value = response_frame["hashValue"].iloc[0]


if __name__ == '__main__':
    accounts_trading = AccountsTrading()


# functions-framework --target=runAccount --source=AccountsTrading.py --debug