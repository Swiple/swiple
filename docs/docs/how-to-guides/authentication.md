---
sidebar_position: 3
title: How to use OAuth authentication
---

# Authentication

Swiple uses [FastAPI Users](https://fastapi-users.github.io/fastapi-users/) and [HTTPX OAuth](https://frankie567.github.io/httpx-oauth/) to manage Username/Password and OAuth access. One or multiple OAuth providers can be used at a time.

### Supported OAuth Providers
* [Github](#github)
* [Google](#google)
* [Microsoft](#microsoft)
* [Okta](#okta)

### OAuth

To set up OAuth, add an OAuth provider to `docker/.env`.

:::caution Caution
Do not check in `OAUTH_SECRET` or `SECRET_KEY` to your codebase. The examples below are for testing only.

For production, please use a secrets store like AWS Parameter Store or AWS Secrets Manager. Please see [Retrieving `OAUTH_SECRET` and `SECRET_KEY`](#retrieving-oauth_secret-and-secret_key) for examples.
:::

All providers will require a redirect URL. The redirect URL structure is as follows:
`{UI_HOST_URL}/login?provider={provider_name}`


#### Github
```bash
GITHUB_OAUTH_ENABLED=true
GITHUB_OAUTH_CLIENT_ID="---Redacted---"
GITHUB_OAUTH_SECRET="---Redacted---"
```
**Redirect URL:** {UI_HOST_URL}/login?provider=github

#### Google
```bash
GOOGLE_OAUTH_ENABLED=true
GOOGLE_OAUTH_CLIENT_ID="---Redacted---"
GOOGLE_OAUTH_SECRET="---Redacted---"
```
**Redirect URL:** {UI_HOST_URL}/login?provider=google

#### Microsoft
```bash
MICROSOFT_OAUTH_ENABLED=true
MICROSOFT_OAUTH_CLIENT_ID="---Redacted---"
MICROSOFT_OAUTH_SECRET="---Redacted---"
MICROSOFT_OAUTH_TENANT=null  # defaults to "common" when not set
```
**Redirect URL:** {UI_HOST_URL}/login?provider=microsoft

#### Okta
```bash
OKTA_OAUTH_ENABLED=true
OKTA_OAUTH_CLIENT_ID="---Redacted---"
OKTA_OAUTH_SECRET="---Redacted---"
OKTA_OAUTH_BASE_URL="[Redacted].okta.com" # do not include HTTP/HTTPS. HTTPS is used.
```
**Redirect URL:** {UI_HOST_URL}/login?provider=okta
<br />

:::info
Do you use an OAuth provider that isn't above? Add it to [HTTPX OAuth here](https://github.com/frankie567/httpx-oauth/tree/master/httpx_oauth/clients).
:::
