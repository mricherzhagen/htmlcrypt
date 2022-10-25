"""
Provide command line interface for htmlcrypt tool
"""

import argparse
import pathlib
from getpass import getpass
from . import encrypt_file


def main() -> None:
    """Use sys.argv arguments to specify file for encryption"""
    parser = argparse.ArgumentParser(
        prog="python -m htmlcrypt", description="Encrypt HTML file with password"
    )
    parser.add_argument(
        "-p",
        "--password",
        help="""Password for encrypting/decrypting.
        Will ask for password from stdin if not specified""",
    )
    input_file_arg = parser.add_argument(
        "file", type=pathlib.Path, help="File to encrypt"
    )
    output_file_arg = parser.add_argument(
        "-o", "--output", type=pathlib.Path, help="Encrypted filename"
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_const",
        const=True,
        help="Overwrite existing output file",
    )

    args = parser.parse_args()

    if args.password:
        password = args.password
    else:
        while True:
            password = getpass("Password: ")
            if password == getpass("Confirm: "):
                break
            print("Passwords did not match. Try again")

    input_file_arg.type = argparse.FileType("rb")
    output_file_arg.type = argparse.FileType("xb" if not args.force else "wb")
    output_file_arg.default = args.file.name + ".encrypted"
    args = parser.parse_args()

    print(f"Encrypting {args.file.name} to {args.output.name}")

    with args.file as input_file:
        with args.output as output_file:
            encrypt_file(password, input_file, output_file)


if __name__ == "__main__":
    main()
