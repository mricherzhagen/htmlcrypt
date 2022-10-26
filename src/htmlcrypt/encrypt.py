"""
Define methods for encrypting file with password
"""

import typing
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256


# pylint: disable=too-few-public-methods
class _SupportsRead(typing.Protocol):
    # pylint: disable=missing-function-docstring
    def read(self, amount: int) -> bytes:
        ...


class _SupportsEncrypt(typing.Protocol):
    # pylint: disable=missing-function-docstring
    def encrypt(self, data: bytes) -> bytes:
        ...

    def encrypt_and_digest(self, data: bytes) -> typing.Tuple[bytes, bytes]:
        ...


def _create_salt(rand: _SupportsRead) -> bytes:
    "Create the salt using the default config using the provided random source"
    return rand.read(32)


def _derive_key(password: str, salt: bytes) -> bytes:
    "Derive the encryption key using PBKDF2 from password and salt"
    return PBKDF2(
        password,
        salt,
        count=100_000,
        dkLen=32,
        hmac_hash_module=SHA256,
    )


def _create_nonce(rand: _SupportsRead) -> bytes:
    "Create the nonce using the default config using the provided random source"
    return rand.read(16)


def _get_cipher(key: bytes, nonce: bytes) -> _SupportsEncrypt:
    "Create the AES Cipher"
    return typing.cast(_SupportsEncrypt, AES.new(key, AES.MODE_GCM, nonce=nonce))


def _encrypt_file_to_file(
    cipher: _SupportsEncrypt, inputfile: typing.BinaryIO, outputfile: typing.BinaryIO
) -> bytes:
    "Use the proved cipher to encrypt the content of inputfile and write to outputfile"
    while True:
        chunk = inputfile.read(1024)
        if not chunk:
            break
        outputfile.write(cipher.encrypt(chunk))
    encrypted, digest = cipher.encrypt_and_digest(b"")
    outputfile.write(encrypted)
    return digest


def encrypt_file(
    password: str, input_file: typing.BinaryIO, output_file: typing.BinaryIO
) -> None:
    "Encrypt file with password and write to output"
    rand = Random.new()

    salt = _create_salt(rand)
    key = _derive_key(password, salt)
    nonce = _create_nonce(rand)
    cipher = _get_cipher(key, nonce)

    output_file.write(salt)
    output_file.write(nonce)
    digest = _encrypt_file_to_file(cipher, input_file, output_file)
    output_file.write(digest)
