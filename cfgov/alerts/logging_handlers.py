import logging

from alerts.github_alert import GithubAlert


class CFGovErrorHandler(logging.Handler):
    def emit(self, record):
        GithubAlert({}).post(
            title=record.message,
            body=record.exc_text,
        )
