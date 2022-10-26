"""
Provide command line interface for htmlcrypt tool
"""

import argparse
import pathlib
from getpass import getpass
from .encrypt import encrypt_file
from .decrypt import write_decrypt_file


# pylint: disable=too-many-branches
def main() -> None:
    """Use sys.argv arguments to specify file for encryption"""
    parser = argparse.ArgumentParser(
        prog="python -m htmlcrypt" if __name__ == "__main__" else None,
        description="Encrypt HTML file with password",
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
    decrypt_file_arg = parser.add_argument(
        "-d",
        "--decrypt",
        type=pathlib.Path,
        help="""Location to generate the decryption .html file.
        Relative path to encrypted file will be injected into file.""",
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
        str(args.decrypt.with_suffix(args.decrypt.suffix + ".content.encrypted"))
        if args.decrypt
        else str(args.file.with_suffix(args.file.suffix + ".encrypted"))
    )
    args = parser.parse_args()

    file_set = {args.file.resolve(), args.encrypted.resolve()}
    if len(file_set) != 2:
        parser.error(
            "You cannot supply the same file as input file and --encrypted argument"
        )

    if args.decrypt:
        file_set.add(args.decrypt.resolve())
        if len(file_set) != 3:
            parser.error(
                "The decryption file cannot be the same as the input or encrypted file"
            )

    if args.password is not None:
        password = args.password
    else:
        while True:
            password = getpass("Password: ")
            if password == getpass("Confirm: "):
                break
            print("Passwords did not match. Try again")

    input_file_arg.type = argparse.FileType("rb")
    encrypted_file_arg.type = argparse.FileType("xb" if not args.force else "wb")
    decrypt_file_arg.type = argparse.FileType("x" if not args.force else "w")
    args = parser.parse_args()

    print(f"Encrypting {args.file.name} to {args.encrypted.name}")

    with args.file as input_file:
        with args.encrypted as output_file:
            encrypt_file(password, input_file, output_file)

    if args.decrypt:
        print(f"Writing decrypt file to {args.decrypt.name}")
        write_decrypt_file(args.decrypt, args.encrypted.name)


if __name__ == "__main__":
    main()
