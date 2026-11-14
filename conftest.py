import os

import pytest


def pytest_configure(config: pytest.Config) -> None:  # ruff: ignore[unused-function-argument]
    if not os.environ.get("GOOGLE_API_KEY") and not os.environ.get("GEMINI_API_KEY"):
        raise RuntimeError(
            "GOOGLE_API_KEY or GEMINI_API_KEY environment variable is not set. Tests cannot run without it."
        )
