# Single Sign-On

The consumerfinance.gov codebase support single sign-on (SSO) with [Open ID Connect (OIDC) providers](https://openid.net/). We use Mozilla's [mozilla-django-oidc](https://mozilla-django-oidc.readthedocs.io/en/stable/) library for OIDC support.

## Local implementation

Our implementation of OIDC SSO uses a custom subclass of mozilla-django-oidc's `OIDCAuthenticationBackend`, found in `login.auth.CFPBOIDCAuthenticationBackend`, that supports additional OIDC claims processing. This enables us to map OIDC roles to Django groups and/or superuser permissioning, and lets us synchronize a user's name to the profile information in the OIDC provider.

If the `OIDC_OP_ADMIN_ROLE` setting is defined, Django's `is_superuser` will be set for users who the OIDC provider reports as having this role identifier.

Every user who is authorized in the SSO provider will be assigned to a "Wagtail Users" group. This enables all members to log into the Wagtail admin.

This group is created with the `wagtailadmin.access_admin` permission once via data migration in the `login` app. If for any reason this group is removed, it will need to be recreated, otherwise new SSO users will not be able to login without an admin user assigning them the `wagtailadmin.access_admin` permission manually.

## Testing OIDC single sign-on locally

For development of mozilla-django-oidc, Mozilla [uses a test OIDC provider](https://github.com/mozilla/docker-test-mozilla-django-oidc), which is published to Docker Hub as `mozilla/oidc-testprovider:oidc_testprovider-latest`. This test provider is a Django project that uses [django-oidc-provider](https://django-oidc-provider.readthedocs.io/) as the OIDC provider application.

We make use of this test provider to enable local testing and development related to SSO for consumerfinance.gov. The OIDC test provider is available in the `docker-compose.sso.yml` file.

For consumerfinance.gov, our compose file adds another set of fixture data that adds `localhost:8000` as a client in addition to the test provider's built-in [`testrp` client that Mozilla uses for local development](https://github.com/mozilla/mozilla-django-oidc?tab=readme-ov-file#local-development).

### Run the test OIDC provider

fasdfoasdfo
The test OIDC provider can be run with:

```shell
docker-compose -f docker-compose.sso.yml up
```

This will start the test provider at http://localhost:8080.

### Create a user in the test OIDC provider

To sign-in via the test provider requires a user. mozilla-django-oidc defaults to using email address to map users between the OIDC provider and the client, and we do not override this default.

Navigate to http://localhost:8080 and you will see an option to sign up, as well as log in. Sign up using an email address you know is already set up as a user in your local consumerfinance.gov database.

### Configure the consumerfinance.gov environment

Our `.env_SAMPLE` file includes SSO-related environment variables with defaults intended for local development against the test OIDC provider.

Either uncomment or add the following lines to your `.env` file:

```shell
export ENABLE_SSO=True
export OIDC_RP_CLIENT_ID=4
export OIDC_RP_CLIENT_SECRET=itsasecret
export OIDC_RP_SIGN_ALGO=HS256
export OIDC_OP_AUTHORIZATION_ENDPOINT=http://localhost:8080/openid/authorize
export OIDC_OP_TOKEN_ENDPOINT=http://localhost:8080/openid/token
export OIDC_OP_USER_ENDPOINT=http://localhost:8080/openid/userinfo
```

And then make sure to `source` it:

```shell
source .env
```

### Run consumerfinance.gov and log in

Start or restart your local consumerfinance.gov instance, then visit http://localhost:8000/admin. Click "Sign in with Single Sign-On".

This should redirect you to the test OIDC provider at http://localhost:8080/openid/authorize with a prompt to authorize "Wagtail (Local HS256)" (the name of the client application as configured in the test provider) to access the OIDC user's address.

Click "Authorize", and you should be returned to http://localhost:8000/admin, logged in as the expected user.

## References

For more information on our OIDC single sign-on implementation, please refer to:

- [mozilla-django-oidc documentation](https://mozilla-django-oidc.readthedocs.io/en/stable/)
- [mozilla-django-oidc's settings documentation](https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html)
- [Open ID Connect specification](https://openid.net/specs/openid-connect-core-1_0.html#StandardClaims)

Additionally, the source code to the following may also be useful:

- [mozilla-django-oidc](https://github.com/mozilla/mozilla-django-oidc)
- [Mozilla's test OIDC provider](https://github.com/mozilla/docker-test-mozilla-django-oidc/tree/main/testprovider)
- [Mozilla's test OIDC client](https://github.com/mozilla/docker-test-mozilla-django-oidc/tree/main/testrp)
- [django-oidc-provider](https://github.com/juanifioren/django-oidc-provider)
