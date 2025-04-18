"""Update CLI."""

import argparse
import logging
import re
import sys
from pathlib import Path
from subprocess import run as cmd
from typing import Final

import requests
from patterns_generator import get_latest, main, parsing_version

ROOT_DIR: Final[Path] = Path(__file__).absolute().parent.parent
logging.basicConfig(format="[%(asctime)s] %(levelname)s:%(message)s", level=logging.INFO)


def arg_parser() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog="update",
        add_help=True,
        description="Update phone-gen patterns",
    )
    parser.add_argument("-u", "--update", dest="update", help="Need to update?", action="store_true")
    parser.add_argument(
        "-p",
        "--ignore-phonenumbers",
        dest="ignore_phonenumbers",
        help="Ignore phonenumbers versions",
        action="store_true",
    )
    parser.add_argument("-b", "--no-black", dest="no_black", help="Do not run black", action="store_true")
    parser.add_argument("-f", "--no-flake", dest="no_flake", help="Do not run flake8", action="store_true")
    parser.add_argument("-t", "--no-tests", dest="no_tests", help="Do not run tests", action="store_true")
    return parser.parse_args()


def is_need_update(version: str) -> bool:
    """Is need update libphonenumber."""
    if (pattern_file := ROOT_DIR / "phone_gen" / "patterns.py").exists():
        with pattern_file.open("r") as _file:
            file = _file.read()
            if match := re.findall(r'libphonenumber v([\d.]+)"', file):
                return version != match[0]
    return True


def check_phonenumbers_libs(version: str) -> bool:
    """Check pypi phonenumbers version."""
    response = requests.get("https://pypi.org/pypi/phonenumbers/json", timeout=60)
    response.raise_for_status()
    releases = response.json()["releases"]
    return version in releases


def update_pipfile(version: str) -> None:
    """Update Pipfile file."""
    logging.info("Update Pipfile")
    if (pipfile_path := ROOT_DIR / "Pipfile").exists():
        with pipfile_path.open("r") as _file:
            pipfile = _file.read()
        pipfile = re.sub(r'phonenumbers\s?=\s?"==[\d.]+"', f'phonenumbers = "=={version}"', pipfile)
        with pipfile_path.open("w") as _file:
            _file.write(pipfile)
        return
    logging.critical("Not found Pipfile")
    sys.exit(-1)


def update_workflow(version: str) -> None:
    """Update GitHub workflow file."""
    logging.debug("Update workflow")
    if (workflow_path := ROOT_DIR / ".github" / "workflows" / "python-package.yml").exists():
        with workflow_path.open("r") as _file:
            workflow = _file.read()
        workflow = re.sub(r"phonenumbers==[\d.]+", f"phonenumbers=={version}", workflow)
        with workflow_path.open("w") as _file:
            _file.write(workflow)
        return
    logging.critical("Not found workflow file")
    sys.exit(-1)


def run(args: argparse.Namespace) -> None:
    """Run update script."""
    version = parsing_version(get_latest())
    if not args.update and not is_need_update(version=version):
        logging.info("No update required")
        sys.exit(0)
    is_phonenumbers = check_phonenumbers_libs(version=version)
    if not is_phonenumbers and not args.ignore_phonenumbers:
        logging.critical(f"No actual version phonenumbers. {version}")
        sys.exit(-1)
    if is_phonenumbers:
        update_pipfile(version=version)
        update_workflow(version=version)

    logging.info("Update requirements")
    cmd(["pipenv", "update", "-d"], cwd=ROOT_DIR, check=False)

    logging.info("Update patterns")
    main(patterns_tag=f"v{version}")

    if not args.no_black:
        logging.info("Run format")
        cmd(["pipenv", "run", "format"], cwd=ROOT_DIR, check=False)
    if not args.no_flake:
        logging.info("Run check")
        cmd(["pipenv", "run", "check"], cwd=ROOT_DIR, check=False)
    if not args.no_tests:
        logging.info("Run tests")
        cmd(["pytest", "tests/"], cwd=ROOT_DIR, check=False)
    logging.info("Done")


if __name__ == "__main__":
    run(args=arg_parser())
