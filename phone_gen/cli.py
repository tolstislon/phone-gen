import argparse

from . import __version__
from ._generator import NumberGeneratorException, PhoneNumber, PhoneNumberNotFound

parser = argparse.ArgumentParser(
    prog="phone-gen",
    add_help=True,
    description="International phone number generation",
)
parser.add_argument(
    "-v", "--version", action="version", version="%(prog)s {}".format(__version__)
)
parser.add_argument("country", help="Country code example: GB", metavar="country")
parser.add_argument(
    "-n",
    "--not-full",
    action="store_false",
    help="Get a phone number without a country code",
    dest="full",
)


def main():
    args = parser.parse_args()
    try:
        print(PhoneNumber(args.country).get_number(args.full))
    except (PhoneNumberNotFound, NumberGeneratorException) as error:
        print("Error: {}".format(error.args[0]))
