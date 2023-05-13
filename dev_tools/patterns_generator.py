import argparse
import io
import json
import tarfile
import tempfile
import xml.etree.ElementTree as ElementTree
from datetime import datetime
from pathlib import Path
from re import findall, match
from typing import Dict, Generator, Tuple, Final

import requests

root: Final[Path] = Path(__file__).absolute().parent.parent

TEMPLATE: Final[str] = """# -*- coding: utf-8 -*-
\"""
Auto-generated file {datetime} UTC
Resource: https://github.com/google/libphonenumber {version}
\"""


PATTERNS = {patterns}

"""
XML_FILE: Final[str] = "PhoneNumberMetadata.xml"
ARCHIVE_PATH: Final[str] = "libphonenumber-{version}/resources/{file}"
SOURCE_TAG: Final[str] = "https://github.com/google/libphonenumber/archive/{tag}.tar.gz"
DATETIME_FORMAT: Final[str] = "%Y-%m-%d %H:%M:%S"


def arg_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="pattern_generator",
        add_help=True,
        description="Pattern generator to phone-gen",
    )
    parser.add_argument(
        "-t", "--tag", dest="tag", help="libphonenumber tag", default="latest"
    )
    return parser.parse_args()


class RegexCompiler:
    _replace_values: Tuple[Tuple[str, str], ...] = (
        ("\n", ""),
        (" ", ""),
        ("?:", ""),
        (r"\d", r"[\d]"),
        (",", ":"),
    )

    def __init__(self, pattern: str):
        self.pattern = f"({self._replace(pattern)})"

    def _replace(self, pattern: str) -> str:
        for i in self._replace_values:
            pattern = pattern.replace(*i)
        return pattern

    def _group(self, group: str) -> str:
        groups = findall(r"\((.*)\)", group)
        if groups:
            for i in groups:
                group.replace(group, self._group(i))
        return "|".join(f"({i})" for i in group.split("|"))

    def compile(self) -> str:
        return self.pattern.replace(self.pattern, self._group(self.pattern))


class Parser:
    def __init__(self, source: str):
        self.root = ElementTree.fromstring(source)
        self.line_tag = "fixedLine"
        self.pattern_tag = "nationalNumberPattern"
        self.mobile_tag = 'mobile'

    def render(self) -> Generator[Tuple[str, Dict[str, str]], None, None]:
        for territory in self.root.iter("territory"):
            attrs = territory.attrib
            if (code := attrs.get("id", "1")).isdigit():
                continue
            value = {"code": attrs.get("countryCode", "")}
            for fixed_line in territory.iter(self.line_tag):
                for national_number_pattern in fixed_line.iter(self.pattern_tag):
                    value["pattern"] = RegexCompiler(national_number_pattern.text).compile()
            for mobile_tag in territory.iter(self.mobile_tag):
                for national_number_pattern in mobile_tag.iter(self.pattern_tag):
                    value["mobile"] = RegexCompiler(national_number_pattern.text).compile()

            yield code, value


def get_latest() -> str:
    response = requests.get("https://github.com/google/libphonenumber/releases/latest")
    return response.url.split("/")[-1]


def parsing_xml(file: Path) -> Dict[str, Dict[str, str]]:
    with file.open("rb") as _file:
        parser = Parser(_file.read().decode())
        return {code: value for code, value in parser.render()}


def parsing_version(tag: str) -> str:
    if version := match(r".*(?P<major>\d{1,2})\.(?P<minor>\d{1,2})\.(?P<patch>\d{1,2}).*", tag):
        return "{major}.{minor}.{patch}".format_map(version.groupdict())
    raise ValueError(f"Invalid tag: {version}")


def main(patterns_tag: str) -> str:
    if tag := get_latest() if patterns_tag == "latest" else patterns_tag:
        version = parsing_version(tag)
        with tempfile.TemporaryDirectory() as tmpdir:
            response = requests.get(SOURCE_TAG.format(tag=tag), stream=True)
            if not response.ok:
                raise ValueError(f"Invalid tag: {tag}")
            with tarfile.open(fileobj=io.BytesIO(response.content)) as tar_file:
                archive_path = ARCHIVE_PATH.format(version=version, file=XML_FILE)
                tar_file.extract(archive_path, tmpdir)
            xml_file = Path(tmpdir, archive_path)
            if not xml_file.exists():
                raise FileNotFoundError(xml_file.absolute())
            data = parsing_xml(xml_file)
            patterns_path = root / "phone_gen" / "patterns.py"
            with patterns_path.open("wb") as _file:
                temp = TEMPLATE.format(
                    datetime=datetime.utcnow().strftime(DATETIME_FORMAT),
                    patterns=json.dumps({"info": f"libphonenumber {tag}", "data": data}, indent=4),
                    version=tag,
                )
                _file.write(temp.encode())
        return version


if __name__ == "__main__":
    args = arg_parser()
    main(patterns_tag=args.tag)
