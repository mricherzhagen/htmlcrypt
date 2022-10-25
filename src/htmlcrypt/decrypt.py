"""
Define methods for generating the HTML file used to decrypt the content
"""

import typing
import re
import os.path
import shutil
from importlib.resources import files


def write_decrypt_file(decrypt_file: typing.TextIO, encrypted_file_path: str) -> None:
    """
    Write HTML to `decrypt_file` argument that will prompt to decrypt file from
    `encrypted_file_path` with password.
    Generates a relative path.
    """
    rex = re.compile(r"const encryptedFileName = 'content.html.encrypted';")
    encrypted_file_rel_path = os.path.relpath(
        encrypted_file_path, os.path.dirname(decrypt_file.name)
    )
    value = f"const encryptedFileName = '{encrypted_file_rel_path}';"
    with files(__package__).joinpath("decrypt.html").open("r") as decrypt_template:
        for line in decrypt_template:
            newline, nreplace = rex.subn(value, line)
            decrypt_file.write(newline)
            if nreplace > 0:
                break
        else:
            assert False, "Could not find filename pattern in decrypt.html template"
        # Copy remaining file content
        shutil.copyfileobj(decrypt_template, decrypt_file)
