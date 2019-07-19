Run the `build.sh` script from the project root:

```sh
docker/drama-free-django/build.sh
```

This will run a CentOS 6 container to generate a [drama-free-django](https://github.com/cfpb/drama-free-django) release artifact in the project root named `cfgov_current_build.zip`.

To run a basic test of the artifact:

```sh
docker/drama-free-django/test.sh
```

This will run a CentOS 6 container to validate the built artifact by extracting it and running Django
[`collectstatic`](https://docs.djangoproject.com/en/1.11/ref/contrib/staticfiles/#collectstatic).
