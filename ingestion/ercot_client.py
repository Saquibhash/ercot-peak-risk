import os, time, requests
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = "fec253ea-0d06-4272-a5e6-b478baeecd70"   # public client id from ERCOT's guide
TOKEN_URL = ("https://ercotb2c.b2clogin.com/ercotb2c.onmicrosoft.com/"
             "B2C_1_PUBAPI-ROPC-FLOW/oauth2/v2.0/token")
BASE = "https://api.ercot.com/api/public-reports"      # confirm in the API Explorer

_token = {"value": None, "at": 0.0}

def get_token():
    if _token["value"] and time.time() - _token["at"] < 50 * 60:
        return _token["value"]
    r = requests.post(TOKEN_URL, data={
        "username": os.environ["ERCOT_USERNAME"],
        "password": os.environ["ERCOT_PASSWORD"],
        "grant_type": "password",
        "scope": f"openid {CLIENT_ID} offline_access",
        "client_id": CLIENT_ID,
        "response_type": "id_token",
    }, timeout=30)
    r.raise_for_status()
    _token.update(value=r.json()["id_token"], at=time.time())
    return _token["value"]

def get(path, **params):
    headers = {"Authorization": f"Bearer {get_token()}",
               "Ocp-Apim-Subscription-Key": os.environ["ERCOT_SUB_KEY"]}
    r = requests.get(f"{BASE}/{path}", headers=headers, params=params, timeout=60)
    r.raise_for_status()
    return r.json()