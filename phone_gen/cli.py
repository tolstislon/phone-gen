import argparse

from . import __version__
from ._generator import NumberGeneratorException, PhoneNumber, PhoneNumberNotFound

parser = argparse.ArgumentParser(
    prog="phone-gen",
    add_help=True,
    description="International phone number generation",
)
parser.add_argument(
    "-v",
    "--version",
    action="version",
    version=f"%(prog)s {__version__} ({PhoneNumber.info()})",
)
parser.add_argument(
    "country",
    help='Country code or country name. Example: "GB" or "GBR" or "Great Britain"',
    metavar="country",
    nargs="+",
)
parser.add_argument(
    "-f",
    "--not-full",
    action="store_false",
    help="Get a phone number without a country code",
    dest="full",
)
parser.add_argument(
    "-m",
    "--mobile",
    action="store_true",
    help="Get mobile phone number",
    dest="mobile",
)
parser.add_argument(
    "-n",
    "--national",
    action="store_true",
    help="Get national phone number",
    dest="national",
)


def main() -> None:
    args = parser.parse_args()
    country = " ".join(args.country)
    try:
        phone_number = PhoneNumber(country)
        if args.national:
            number = phone_number.get_national(args.full)
        elif args.mobile:
            number = phone_number.get_mobile(args.full)
        else:
            number = phone_number.get_number(args.full)
        print(number)
    except (PhoneNumberNotFound, NumberGeneratorException) as error:
        print(f"Error: {error.args[0]}")
