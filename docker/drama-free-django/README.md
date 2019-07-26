# Docker-based drama-free-django build and test tools

## Build

Run the `build.sh` script from the project root:

```sh
docker/drama-free-django/build.sh
```

This will run a CentOS 6 container to generate a [drama-free-django](https://github.com/cfpb/drama-free-django) release artifact in the project root named `cfgov_current_build.zip`.

## Test

To run a basic test of the artifact:

```sh
docker/drama-free-django/test.sh
```

This will run a CentOS 6 container to validate the built artifact by extracting it and running Django
[`collectstatic`](https://docs.djangoproject.com/en/1.11/ref/contrib/staticfiles/#collectstatic).

## Notes

1. When running the container as a user that exists on the host, but not in the container, you may notice a warnings similar to:

    ```
    /usr/bin/id: cannot find name for user ID 502
    ```

    ...and...

    ```
    warning Skipping preferred cache folder "/.cache/yarn" because it is not writable.
    warning Selected the next writable cache folder in the list, will be "/tmp/.yarn-cache-501".
    ```

    This is not anything to worry about. It simply means the uid/gid don't match any users/groups setup in the container.
