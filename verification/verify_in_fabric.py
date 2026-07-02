"""
Verification script — checks your real MS Fabric workspace

Prerequisites:
  pip install azure-identity requests

How authentication works:
  - azure-identity opens your browser (or device login) once to sign in
    with your organizational account.
  - It gets a token automatically — same login as app.fabric.microsoft.com
  - That token is used to call the Fabric REST API directly.
"""

import requests
from azure.identity import InteractiveBrowserCredential


FABRIC_BASE = "https://api.fabric.microsoft.com/v1"
SCOPE = "https://api.fabric.microsoft.com/.default"


def get_token():
    """
    Opens a browser window once to log you in with your org account.
    After that it caches the token so you don't need to log in every run.
    """
    print("Opening browser for login (use your org account)...")
    credential = InteractiveBrowserCredential()
    token = credential.get_token(SCOPE).token
    print("Login successful.\n")
    return token


def get_headers(token):
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


def list_workspaces(token):
    """Step 1 - list all workspaces your account can see."""
    url = f"{FABRIC_BASE}/workspaces"
    resp = requests.get(url, headers=get_headers(token))

    if resp.status_code != 200:
        print(f"Failed to list workspaces: {resp.status_code}")
        print(resp.text)
        return []

    workspaces = resp.json().get("value", [])
    print(f"Found {len(workspaces)} workspace(s):\n")
    for ws in workspaces:
        print(f"  - {ws['displayName']}  (id: {ws['id']})")
    return workspaces


def search_lakehouses(token):
    """
    Step 2 - use Catalog Search to find all Lakehouses across all workspaces.
    This is exactly the API call from the SKILL.md you benchmarked against.
    """
    url = f"{FABRIC_BASE}/catalog/search"
    body = {
        "search": "",
        "filter": "Type eq 'Lakehouse'",
        "pageSize": 100,
    }

    print("\nSearching for Lakehouses across all workspaces...")
    resp = requests.post(url, headers=get_headers(token), json=body)

    if resp.status_code != 200:
        print(f"Failed: {resp.status_code}")
        print(resp.text)
        return

    items = resp.json().get("value", [])
    print(f"Found {len(items)} Lakehouse(s):\n")
    for item in items:
        ws_name = item.get("hierarchy", {}).get("workspace", {}).get("displayName", "unknown")
        print(f"  - {item.get('displayName')}  (workspace: {ws_name})")

    if not items:
        print("No Lakehouses found - your workspace may be empty, which is fine.")
        print("If you expected to see some, confirm your account has Viewer")
        print("access to those workspaces in app.fabric.microsoft.com.")


def main():
    print("=" * 55)
    print("FABRIC WORKSPACE VERIFICATION (Python, no Azure CLI)")
    print("=" * 55 + "\n")

    token = get_token()
    list_workspaces(token)
    search_lakehouses(token)

    print("\nVerification complete.")
    print("If you saw your workspace and Lakehouses above, your")
    print("fabric account is working correctly for this project.")


if __name__ == "__main__":
    main()
