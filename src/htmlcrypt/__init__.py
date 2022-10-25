"""
Tool for encrypting HTML files for later decryption with JavaScript.

Depends on pycryptodome.
"""

from .encrypt import encrypt_file
from .decrypt import write_decrypt_file
