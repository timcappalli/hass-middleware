# Home Assistant Middleware

This is a middleware web app to make creating Home Assistant sensors a bit easier.


## Configuration
### Required Environment Variables
`CPPM_FQDN`: [string] Fully qualified domain name of CPPM (ex: cppm.mydomain.com)

`CPPM_CLIENT_ID`: [string] CPPM OAuth 2.0 cilent_id

`CPPM_CLIENT_SECRET`: [string] CPPM OAuth 2.0 cilent_secret
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

`docker build --no-cache -t hass-middleware:2020.07.09 .`

`docker run -d -p 5000:5000 hass-middleware --env-file <.env-filename>`

## Change Log
### 2020.07.08 (2020-07-08)
* Initial release with CPPM Session Count


## License and Other Information
This repo is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

Author: @timcappalli