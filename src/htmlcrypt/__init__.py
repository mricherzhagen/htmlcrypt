"""
Tool for encrypting HTML files for later decryption with JavaScript.

Depends on pycryptodome.
"""

__all__ = [
    "encrypt_file",
    "write_decrypt_file",
]

from .encrypt import encrypt_file
from .decrypt import write_decrypt_file
