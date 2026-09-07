"""Configure a disposable database before the application is imported by tests."""

import os
import tempfile
from urllib.parse import urlparse


_test_database_directory = tempfile.TemporaryDirectory(prefix="buy_sell_tests_")


def _github_actions_database_url():
    """Use CI's PostgreSQL service only when it resolves to the local runner."""
    if os.getenv("GITHUB_ACTIONS") != "true":
        return None
    database_url = os.getenv("SQLALCHEMY_DATABASE_URL")
    if not database_url:
        return None
    hostname = urlparse(database_url).hostname
    if hostname not in {"localhost", "127.0.0.1", "::1"}:
        raise RuntimeError("Tests refuse to use a non-local GitHub Actions database.")
    return database_url


os.environ["SQLALCHEMY_DATABASE_URL"] = (
    _github_actions_database_url()
    or f"sqlite:///{_test_database_directory.name}/test.sqlite"
)
