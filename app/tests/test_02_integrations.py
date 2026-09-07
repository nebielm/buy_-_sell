import io
import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch
from urllib.parse import urlparse

import pytest
from fastapi import HTTPException

from app.routes import utils


class FakeImageUpload:
    """Minimal UploadFile-compatible object for S3 unit tests."""

    def __init__(self, filename):
        self.filename = filename
        self.size = 4
        self.content_type = "image/jpeg"
        self.file = io.BytesIO(b"test")


@pytest.mark.parametrize(
    ("bucket_name", "filename"),
    [
        ("profile-images", "profile.jpg"),
        ("listing-images", "listing.jpg"),
    ],
)
def test_upload_url_uses_the_selected_bucket_and_region(bucket_name, filename):
    """Return the URL for the bucket that actually received the object."""
    with patch("app.routes.utils.boto3.client") as boto_client:
        result = utils.upload_file(FakeImageUpload(filename), bucket_name)

    boto_client.return_value.upload_fileobj.assert_called_once()
    parsed_url = urlparse(result)
    assert parsed_url.scheme == "https"
    assert parsed_url.netloc == f"{bucket_name}.s3.eu-north-1.amazonaws.com"
    assert parsed_url.path.endswith(f"_{filename}")


def test_application_imports_without_openai_api_key(tmp_path):
    """Importing the application must not construct an OpenAI client."""
    project_root = Path(__file__).resolve().parents[2]
    environment = os.environ.copy()
    environment["OPENAI_API_KEY"] = ""
    environment["SQLALCHEMY_DATABASE_URL"] = f"sqlite:///{tmp_path}/import.sqlite"

    result = subprocess.run(
        [sys.executable, "-c", "import app.main"],
        cwd=project_root,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr


def test_local_tests_override_a_configured_remote_database():
    """Ordinary test runs ignore a remote application database URL."""
    project_root = Path(__file__).resolve().parents[2]
    environment = os.environ.copy()
    environment.pop("GITHUB_ACTIONS", None)
    environment["SQLALCHEMY_DATABASE_URL"] = "postgresql://user:password@remote.example/test"

    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import os; import app.tests.conftest; "
            "print(os.environ['SQLALCHEMY_DATABASE_URL'])",
        ],
        cwd=project_root,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert result.stdout.strip().startswith("sqlite:///")


def test_ci_tests_reject_a_non_local_database():
    """Even CI cannot opt into a remote database accidentally."""
    project_root = Path(__file__).resolve().parents[2]
    environment = os.environ.copy()
    environment["GITHUB_ACTIONS"] = "true"
    environment["SQLALCHEMY_DATABASE_URL"] = "postgresql://user:password@remote.example/test"

    result = subprocess.run(
        [sys.executable, "-c", "import app.tests.conftest"],
        cwd=project_root,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode != 0
    assert "Tests refuse to use a non-local GitHub Actions database." in result.stderr


def test_ai_description_without_api_key_returns_controlled_error(monkeypatch):
    """Calling the optional AI path without configuration fails explicitly."""
    monkeypatch.setenv("OPENAI_API_KEY", "")

    with pytest.raises(HTTPException) as exc_info:
        utils.generate_description(keywords="bike", parameters="condition: used")

    assert exc_info.value.status_code == 503
    assert exc_info.value.detail == (
        "AI description generation is unavailable: OPENAI_API_KEY is not configured."
    )
