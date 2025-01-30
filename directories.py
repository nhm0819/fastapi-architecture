import os
from pathlib import Path

root = Path(os.path.dirname(__file__))

profiles = root.joinpath("profiling")

profiles_pytest = profiles.joinpath("pytest")
if not profiles_pytest.exists():
    profiles_pytest.mkdir(parents=True, exist_ok=True)

profiles_api = profiles.joinpath("api")
if not profiles_api.exists():
    profiles_api.mkdir(exist_ok=True)
