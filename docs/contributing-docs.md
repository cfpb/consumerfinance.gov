# Contributing to the Docs

Our documentation is written as Markdown files and served via GitHub Pages
by [MkDocs](https://www.mkdocs.org/).

## Writing the docs

As our documentation is written in Markdown,
the [base Markdown specification](https://daringfireball.net/projects/markdown/)
is a useful reference. MkDocs also includes
[some documentation to get you started writing in Markdown](https://www.mkdocs.org/user-guide/writing-your-docs/#writing-with-markdown).

In addition to standard Markdown, our documentation supports the following extensions:

- [Admonitions](https://python-markdown.github.io/extensions/admonition/)
    adds specially called-out text anywhere within the document
    as notes, warnings, and other types.

- [BetterEm](https://facelessuser.github.io/pymdown-extensions/extensions/betterem/)
    improves the handling of bold and italics.

- [MagicLink](https://facelessuser.github.io/pymdown-extensions/extensions/magiclink/)
    provides automatic linking for URLs in the Markdown text.

- [SuperFences](https://facelessuser.github.io/pymdown-extensions/extensions/superfences/)
    makes a number of improvements to standard Markdown code fences.

- [Tilde](https://facelessuser.github.io/pymdown-extensions/extensions/tilde/)
    adds support for creating `<del></del>` tags with `~~`.

- [Tables](https://python-markdown.github.io/extensions/tables/)
    adds support for tables to standard Markdown.

When creating new documents, they should be added to the
[mkdocs.yml file](https://github.com/cfpb/consumerfinance.gov/blob/main/mkdocs.yml)
in the appropriate place under `nav:` to get them to appear in the sidebar navigation.
For example:

```
nav:
- Introduction: index.md
```

## Running the docs locally

### With Docker

When running consumerfinance.gov using [Docker-compose](../installation/#docker-based-installation),
this documentation is running by default at http://localhost:8888.

### Manually

When using
[the stand-alone installation](../installation/#stand-alone-installation)
of consumerfinance.gov,
you can run these docs with:

```bash
workon consumerfinance.gov
pip install -r requirements/docs.txt
mkdocs serve -a :8888
```

Once running, they are accessible at http://localhost:8888.

## Deploying the docs to GitHub Pages

Every time a PR is merged to main,
GitHub Actions will build and deploy the documentation to
https://cfpb.github.io/consumerfinance.gov/.
See [How we use GitHub Actions](../github-actions/) for more info.

If you would like to deploy to a fork of consumerfinance.gov owned by another user
you can provide the `-r` argument:

```bash
mkdocs gh-deploy -r USER
```

Where `USER` is the GitHub user.
The docs will then be available at https://USER.github.io/consumerfinance.gov/ after a short period of time.

See the
[the MkDocs documentation](https://www.mkdocs.org/user-guide/deploying-your-docs/)
for more information.
