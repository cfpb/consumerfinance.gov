import logging

from alerts.github_alert import GithubAlert


class CFGovErrorHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, record):
        GithubAlert({}).post(
            title=record.message[:30],
            body=record.message,
        )
