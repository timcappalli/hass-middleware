# Home Assistant Middleware
**Curent Version:** 2020.07.10

This is a middleware web app to make creating Home Assistant sensors a bit easier.


## Configuration
### Required Environment Variables
`CPPM_FQDN`: [string] Fully qualified domain name of CPPM (ex: cppm.mydomain.com)

`CPPM_CLIENT_ID`: [string] CPPM OAuth 2.0 cilent_id

`CPPM_CLIENT_SECRET`: [string] CPPM OAuth 2.0 cilent_secret

`HASS_TOKEN`: [string] Home Assistant long term token

`HASS_FQDN`: [string] Home Assistant FQDN (include :port if not running on 443)
### Optional Environment Variables
`APP_DEBUG`: [boolean] Run the app in debug mode (Default: False)

`APP_PORT`: [integer] Web app port (Default: 5000)

`APP_USERNAME`: [string] Username for HTTP Basic Auth (Default: hass-middleware)

`APP_PASSWORD`: [string] Password for HTTP Basic Auth (Default: Home#AssistantIsGr8t!)

`TLS_CERT_FILENAME`: [string] Filename for PEM-encoded certificate (Default: none)

`TLS_KEY_FILENAME`: [string] Filename for PEM-encoded private key (Default: none)
#### .env file
```
CPPM_FQDN=
CPPM_CLIENT_ID=
CPPM_CLIENT_SECRET=
HASS_TOKEN=
HASS_FQDN=
#APP_DEBUG=
#APP_PORT=
#APP_USERNAME=
#APP_PASSWORD=
#TLS_CERT_FILENAME=
#TLS_KEY_FILENAME=
```

## Usage
Local

`python3 app.py`

Container

`docker build --no-cache -t hass-middleware:2020.07.10 .`

`docker run -d -p 5000:5000 hass-middleware:2020.07.10 --env-file <.env-filename>`

### Endpoints

GET `/cppm/session-count`

* Get the current number of active network sessions from CPPM

POST `/hass/presence-update`

Payload
```
{
    "state": "away",
    "hassEntityId": "device_tracker.my_devicename"
}
```
* Update the state of a device for presence. 

## Change Log
### 2020.07.09 (2020-07-10)
* Added Home Assistant presence update

### 2020.07.08 (2020-07-08)
* Initial release with CPPM Session Count


## License and Other Information
This repo is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

Author: @timcappalli