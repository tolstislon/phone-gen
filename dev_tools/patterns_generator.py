import json
import xml.etree.ElementTree as ElementTree
from datetime import datetime
from pathlib import Path
from re import findall
from typing import Dict, Generator, Tuple

import requests

RESOURCE = "https://raw.githubusercontent.com/google/libphonenumber/master/resources/PhoneNumberMetadata.xml"

TEMPLATE = """# -*- coding: utf-8 -*-
\"""
Auto-generated file {datetime} UTC

Resource: https://github.com/google/libphonenumber {version}
\"""


PATTERNS = {patterns}

"""


class RegexCompiler:
    def __init__(self, pattern: str):
        pattern = pattern.replace("\n", "").replace(" ", "").replace("?:", "")
        pattern = pattern.replace(r"\d", r"[\d]").replace(",", ":")
        self.pattern = "({})".format(pattern)

    def _group(self, group: str) -> str:
        groups = findall(r"\((.*)\)", group)
        if groups:
            for i in groups:
                group.replace(group, self._group(i))
        return "|".join("({})".format(i) for i in group.split("|"))

    def compile(self) -> str:
        return self.pattern.replace(self.pattern, self._group(self.pattern))


class Parser:
    def __init__(self, source: str):
        self.root = ElementTree.fromstring(source)
        self.line_tag = "fixedLine"
        self.pattern_tag = "nationalNumberPattern"

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
            yield code, value


def get_latest() -> str:
    response = requests.get("https://github.com/google/libphonenumber/releases/latest")
    return response.url.split("/")[-1]


def main():
    response = requests.get(RESOURCE)
    parser = Parser(response.text)
    data = {code: value for code, value in parser.render()}
    root_path = Path(__file__).absolute().parent.parent
    file = root_path.joinpath("phone_gen", "patterns.py")
    version = get_latest()
    with file.open("wb") as _file:
        temp = TEMPLATE.format(
            datetime=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            patterns=json.dumps(
                {"info": "libphonenumber {}".format(version), "data": data}, indent=4
            ),
            version=version,
        )
        _file.write(temp.encode())


if __name__ == "__main__":
    main()
