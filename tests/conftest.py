"""Shared pytest setup.

The integration test reads ``resources/parameters.txt`` relative to the
``STRUCTSIM_PROJECT_DIR`` environment variable. Default it to the repository
root so the whole suite runs with a plain ``pytest`` / ``uv run pytest`` and no
extra environment setup.
"""
import os
from pathlib import Path

os.environ.setdefault("STRUCTSIM_PROJECT_DIR", str(Path(__file__).resolve().parent.parent))
