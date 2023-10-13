# Running documentation site locally

If you would like to browse this documentation site locally, you can do so
with [`mkdocs`](https://www.mkdocs.org/):

```sh
pip install -r requirements/docs.txt
mkdocs serve
```

Documentation will be available locally at
[http://localhost:8000/](http://localhost:8000/).

!!! note

    If you are currently running the consumerfinance.gov site locally and
    would like to access the docs at a different port, run,
    for example `mkdocs serve -a localhost:8001` to serve the docs at port 8001.
