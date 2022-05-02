---
sidebar_position: 1
---

# Authentication

Swiple uses [FastAPI Users](https://fastapi-users.github.io/fastapi-users/) and [HTTPX OAuth](https://frankie567.github.io/httpx-oauth/) to manage Username/Password and OAuth access. One or multiple OAuth providers can be used at a time.

### Supported OAuth Providers
* [Github](#github)
* [Google](#google)
* [Microsoft](#microsoft)
* [Okta](#okta)

### OAuth

To set up OAuth, add an OAuth provider to `backend/app/config/config.py`.

:::caution Caution
Do not check in `OAUTH_SECRET` or `SECRET_KEY` to your codebase. The examples below are for testing only.

For production, please use a secrets store like AWS Parameter Store or AWS Secrets Manager. Please see [Retrieving `OAUTH_SECRET` and `SECRET_KEY`](#retrieving-oauth_secret-and-secret_key) for examples.
:::

All providers will require a redirect URL. The redirect URL structure is as follows:
`{UI_HOST_URL}/login?provider={provider_name}`


#### Github
```python
GITHUB_OAUTH_ENABLED = True
GITHUB_OAUTH_CLIENT_ID = "---Redacted---"
GITHUB_OAUTH_SECRET = "---Redacted---"
```
**Redirect URL:** {UI_HOST_URL}/login?provider=github

#### Google
```python
GOOGLE_OAUTH_ENABLED = True
GOOGLE_OAUTH_CLIENT_ID = "---Redacted---"
GOOGLE_OAUTH_SECRET = "---Redacted---"
```
**Redirect URL:** {UI_HOST_URL}/login?provider=google

#### Microsoft
```python
MICROSOFT_OAUTH_ENABLED = True
MICROSOFT_OAUTH_CLIENT_ID = "---Redacted---"
MICROSOFT_OAUTH_SECRET = "---Redacted---"
MICROSOFT_OAUTH_TENANT = None  # defaults to "common" when not set
```
**Redirect URL:** {UI_HOST_URL}/login?provider=microsoft

#### Okta
```python
OKTA_OAUTH_ENABLED = True
OKTA_OAUTH_CLIENT_ID = "---Redacted---"
OKTA_OAUTH_SECRET = "---Redacted---"
OKTA_OAUTH_BASE_URL = "[Redacted].okta.com" # do not include HTTP/HTTPS. HTTPS is used.
```
**Redirect URL:** {UI_HOST_URL}/login?provider=okta
<br />

:::info
Do you use an OAuth provider that isn't above? Add it to [HTTPX OAuth here](https://github.com/frankie567/httpx-oauth/tree/master/httpx_oauth/clients).
:::

### Retrieving `OAUTH_SECRET` and `SECRET_KEY`

Add the code snippet that retrieves your `OAUTH_CLIENT_ID` and `OAUTH_SECRET` to `backend/app/config/config.py`

#### Parameter Store - [Docs](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_parameter)

```python
import boto3

client = boto3.client("ssm")

secret = client.get_parameter(
    Name="string",
    WithDecryption=True
)["Parameter"]["Value"]
```


#### Secrets Manager - [Docs](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.get_secret_value)
```python
import boto3

client = boto3.client("secretsmanager")

secret = client.get_secret_value(
    SecretId="string",
)["SecretString"]
```