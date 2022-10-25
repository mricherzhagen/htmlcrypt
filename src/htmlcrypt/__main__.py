"""
Provide command line interface for htmlcrypt tool
"""

import argparse
import pathlib
from getpass import getpass
from .encrypt import encrypt_file


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
    encrypted_file_arg = parser.add_argument(
        "-e", "--encrypted", type=pathlib.Path, help="Encrypted filename"
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_const",
        const=True,
        help="Overwrite existing output file",
    )

    args = parser.parse_args()

    encrypted_file_arg.default = (
        args.decrypt.name + ".content.encrypted"
        if args.decrypt
        else args.file.name + ".encrypted"
    )
    args = parser.parse_args()

    file_set = {args.file.resolve(), args.encrypted.resolve()}
    if len(file_set) != 2:
        parser.error(
            "You cannot supply the same file as input file and --encrypted argument"
        )

    if args.password:
        password = args.password
    else:
        while True:
            password = getpass("Password: ")
            if password == getpass("Confirm: "):
                break
            print("Passwords did not match. Try again")

    input_file_arg.type = argparse.FileType("rb")
    encrypted_file_arg.type = argparse.FileType("xb" if not args.force else "wb")
    args = parser.parse_args()

    print(f"Encrypting {args.file.name} to {args.encrypted.name}")

    with args.file as input_file:
        with args.encrypted as output_file:
            encrypt_file(password, input_file, output_file)


if __name__ == "__main__":
    main()
