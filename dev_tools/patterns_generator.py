import argparse
import io
import json
import tarfile
import tempfile
import xml.etree.ElementTree as ElementTree
from datetime import datetime
from pathlib import Path
from re import findall, match
from typing import Dict, Generator, Tuple

import requests

argparser = argparse.ArgumentParser(
    prog="pattern_generator",
    add_help=True,
    description="Pattern generator to phone-gen",
)
argparser.add_argument(
    "-t", "--tag", dest="tag", help="libphonenumber tag", default="latest"
)

root = Path(__file__).absolute().parent.parent

TEMPLATE = """# -*- coding: utf-8 -*-
\"""
Auto-generated file {datetime} UTC
Resource: https://github.com/google/libphonenumber {version}
\"""


PATTERNS = {patterns}

"""
XML_FILE = "PhoneNumberMetadata.xml"
ARCHIVE_PATH = "libphonenumber-{version}/resources/{file}"
SOURCE_TAG = "https://github.com/google/libphonenumber/archive/{tag}.tar.gz"


class RegexCompiler:
    def __init__(self, pattern: str):
        pattern = pattern.replace("\n", "").replace(" ", "").replace("?:", "")
        pattern = pattern.replace(r"\d", r"[\d]").replace(",", ":")
        self.pattern = f"({pattern})"

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
            code = attrs.get("id", "1")
            if code.isdigit():
                continue
            value = {"code": attrs.get("countryCode", "")}
            for fixed_line in territory.iter(self.line_tag):
                for national_number_pattern in fixed_line.iter(self.pattern_tag):
                    value["pattern"] = RegexCompiler(
                        national_number_pattern.text
                    ).compile()
            for mobile_tag in territory.iter(self.mobile_tag):
                for national_number_pattern in mobile_tag.iter(self.pattern_tag):
                    value["mobile"] = RegexCompiler(
                        national_number_pattern.text
                    ).compile()

            yield code, value


def get_latest() -> str:
    response = requests.get("https://github.com/google/libphonenumber/releases/latest")
    return response.url.split("/")[-1]


def parsing_xml(file: Path):
    with file.open("rb") as _file:
        parser = Parser(_file.read().decode())
        return {code: value for code, value in parser.render()}


def parsing_version(tag: str) -> str:
    version = match(
        r".*(?P<major>\d{1,2})\.(?P<minor>\d{1,2})\.(?P<patch>\d{1,2}).*", tag
    )
    if version:
        return f"{version.group('major')}.{version.group('minor')}.{version.group('patch')}"
    raise ValueError(f"Invalid tag: {version}")


def main():
    args = argparser.parse_args()
    tag = get_latest() if args.tag == "latest" else args.tag
    if tag:
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
            patterns_path = root.joinpath("phone_gen", "patterns.py")
            with patterns_path.open("wb") as _file:
                temp = TEMPLATE.format(
                    datetime=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                    patterns=json.dumps(
                        {"info": f"libphonenumber {tag}", "data": data},
                        indent=4,
                    ),
                    version=tag,
                )
                _file.write(temp.encode())


if __name__ == "__main__":
    main()
