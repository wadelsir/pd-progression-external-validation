"""Capture runtime and installed package versions for Supplementary File S1."""

from __future__ import annotations

from datetime import datetime, timezone
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
import json
import platform
import subprocess

PACKAGES = [
    "numpy",
    "pandas",
    "scikit-learn",
    "matplotlib",
    "joblib",
    "python-docx",
    "PyYAML",
    "openpyxl",
]


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    output_dir = root / "metadata" / "software_environment"
    output_dir.mkdir(parents=True, exist_ok=True)

    package_versions = {}
    for package in PACKAGES:
        try:
            package_versions[package] = version(package)
        except PackageNotFoundError:
            package_versions[package] = None

    runtime = {
        "recorded_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "operating_system": platform.platform(),
        "machine": platform.machine(),
        "packages": package_versions,
    }

    (output_dir / "runtime_information.json").write_text(
        json.dumps(runtime, indent=2), encoding="utf-8"
    )
    with (output_dir / "requirements-lock.txt").open("w", encoding="utf-8") as handle:
        subprocess.run(
            ["python", "-m", "pip", "freeze"],
            stdout=handle,
            check=True,
            text=True,
        )

    print(f"Environment captured in: {output_dir}")


if __name__ == "__main__":
    main()
