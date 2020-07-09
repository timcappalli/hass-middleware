#!/usr/bin/env python3
import requests
import os
import json
import time
from flask import Flask
from flask_basicauth import BasicAuth

_VERSION_ = "2020.07.08"
_AUTHOR_ = "@timcappalli"

app = Flask(__name__)
basic_auth = BasicAuth(app)

app.config['BASIC_AUTH_FORCE'] = True


def token_handling():
    token = None

    current_time = int(time.time())

    if os.path.isfile("cppm_token.json"):
        if DEBUG:
            print("[DEBUG] cppm_token.json exists.")
        with open('cppm_token.json') as f:
            token_file = json.load(f)

        current_time_plus_thirty = current_time + 30

        # check cached token validity
        expires_on_cached = float(token_file['expires_on'])
        if expires_on_cached > current_time_plus_thirty and CPPM_FQDN == token_file['resource']:
            access_token = token_file['access_token']
            if DEBUG:
                print("[DEBUG] Cached token still valid.\n")
            token = access_token

        else:
            token = None

    if token is not None:
        return token

    else:
        # get new token
        url = CPPM_TOKEN_ENDPOINT
        headers = {"content-type": "application/x-www-form-urlencoded"}
        payload = {"grant_type": "client_credentials", "client_id": CPPM_CLIENT_ID, "client_secret": CPPM_CLIENT_SECRET}

        try:
            if APP_DEBUG:
                print(f"[DEBUG] No cached token. Attempting to acquire new token from endpoint {CPPM_TOKEN_ENDPOINT}.")
            r = requests.post(url, headers=headers, data=payload, timeout=15)
            r.raise_for_status()
            json_response = json.loads(r.text)

            if DEBUG:
                print(f"[DEBUG] {json_response}")

            # token caching
            token_cache = {'access_token': json_response['access_token'], 'expires_on': current_time + int(json_response['expires_in']), 'resource': CPPM_FQDN}
            with open('cppm_token.json', 'w') as tokenfile:
                json.dump(token_cache, tokenfile)

            if DEBUG:
                print("[DEBUG] Token cached to file.")
            return json_response['access_token']

        # TODO: Return status code instead of quitting
        except Exception as e:
            if r.status_code == 400:
                print(e)
                exit(1)
            else:
                print(e)
                exit(1)

# CPPM stuff
@basic_auth.required
@app.route("/cppm/session-count")
def cppm_session_count():
    token = token_handling()
    url = f'https://{CPPM_FQDN}/api/session'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    filter = {"acctstoptime": {"$exists": False}}
    params = {"calculate_count": "true", "limit": 1, "filter": json.dumps(filter)}

    try:

        r = requests.get(url=url, headers=headers, params=params, timeout=15)
        r.raise_for_status()
        response = r.json()
        if DEBUG:
            print(f"[DEBUG] Response: {response}")

        session_count = {"active_sessions": response['count']}
        return str(response['count']), 200
        #return jsonify(session_count), 200

    except Exception as e:
        print(f"[{r.status_code}]: {e}")

        return '', 500


if __name__ == '__main__':
    DEBUG = False

    # GRAB ENV VARIABLES
    CPPM_FQDN = os.environ.get('CPPM_FQDN')
    CPPM_CLIENT_ID = os.environ.get('CPPM_CLIENT_ID')
    CPPM_CLIENT_SECRET = os.environ.get('CPPM_CLIENT_SECRET')

    APP_DEBUG = os.environ.get('APP_DEBUG')
    APP_PORT = os.environ.get('APP_PORT')
    APP_USERNAME = os.environ.get('APP_USERNAME')
    APP_PASSWORD = os.environ.get('APP_PASSWORD')
    TLS_CERT_FILENAME = os.environ.get('TLS_CERT_FILENAME')
    TLS_KEY_FILENAME = os.environ.get('TLS_KEY_FILENAME')

    if APP_DEBUG == 'True':
        DEBUG = True
        print(f"App debugging ENABLED.\n")

    if APP_PORT is None:
        APP_PORT = 5000

    if TLS_CERT_FILENAME is not None and TLS_KEY_FILENAME is not None:
        APP_TLS = True
    else:
        APP_TLS = False

    if CPPM_FQDN is None or CPPM_CLIENT_ID is None or CPPM_CLIENT_SECRET is None:
        print('Missing required environment variables for CPPM.')
        exit(1)

    if APP_USERNAME is None:
        APP_USERNAME = 'hass-middleware'

    if APP_PASSWORD is None:
        APP_PASSWORD = 'Home#AssistantIsGr8t!'

    # STATIC GLOBALS
    CPPM_TOKEN_ENDPOINT = f'https://{CPPM_FQDN}/api/oauth'

    print(CPPM_TOKEN_ENDPOINT)

    app.config['BASIC_AUTH_USERNAME'] = APP_USERNAME
    app.config['BASIC_AUTH_PASSWORD'] = APP_PASSWORD

    # START FLASK APP
    url = f"{CPPM_TOKEN_ENDPOINT}"
    r = requests.get(url, timeout=10)

    if r.status_code == 405:
        print('CPPM is reachable! Starting app...\n')

        if APP_TLS:
            app.run(ssl_context=(TLS_CERT_FILENAME, TLS_KEY_FILENAME), host='0.0.0.0', port=APP_PORT, debug=DEBUG)
        else:
            app.run(host='0.0.0.0', port=APP_PORT, debug=DEBUG)
    else:
        print('CPPM not reachable. Exiting...')
        exit(1)
