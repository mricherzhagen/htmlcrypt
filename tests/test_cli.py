# pylint: disable=missing-module-docstring,missing-function-docstring,duplicate-code

import pathlib
import sys
from typing import Optional
import pytest
import htmlcrypt.__main__


def create_test_file(path: pathlib.Path) -> None:
    assert not path.exists()
    path.write_text("Test content file")
    assert path.is_file()


def run_with_args(*args: str) -> None:
    del sys.argv[1:]
    sys.argv.extend(args)
    htmlcrypt.__main__.main()


def run_with_files(
    inputfile: pathlib.Path,
    encrypted: Optional[pathlib.Path] = None,
    decrypt: Optional[pathlib.Path] = None,
    password: str = "password",
) -> None:
    args = [str(inputfile), "-p", password]
    if encrypted is not None:
        args.extend(["-e", str(encrypted)])
    if decrypt is not None:
        args.extend(["-d", str(decrypt)])
    run_with_args(*args)
    if encrypted is not None:
        assert encrypted.is_file()
    else:
        if decrypt is not None:
            assert decrypt.with_suffix(decrypt.suffix + ".content.encrypted")
        else:
            assert inputfile.with_suffix(inputfile.suffix + ".encrypted").is_file()
    if decrypt is not None:
        assert decrypt.is_file()


def test_missing_file(tmp_path: pathlib.Path) -> None:
    input_file_path = tmp_path / "input.txt"
    assert not input_file_path.exists()
    with pytest.raises(SystemExit):
        run_with_args(str(input_file_path), "-p", "password")


def test_single_arg(tmp_path: pathlib.Path) -> None:
    input_file_path = tmp_path / "input.txt"
    create_test_file(input_file_path)
    run_with_files(input_file_path)


def test_specify_encrypted_filename(tmp_path: pathlib.Path) -> None:
    input_file_path = tmp_path / "input.txt"
    encrypted_file_path = tmp_path / "encrypted_input.encrypted"
    create_test_file(input_file_path)
    run_with_files(input_file_path, encrypted=encrypted_file_path)


def test_specify_encrypted_filename_with_subfolder(tmp_path: pathlib.Path) -> None:
    input_file_path = tmp_path / "input.txt"
    encrypted_file_path = tmp_path / "subfolder" / "encrypted_input.encrypted"
    assert not encrypted_file_path.parent.exists()
    encrypted_file_path.parent.mkdir()
    assert encrypted_file_path.parent.is_dir()
    create_test_file(input_file_path)
    run_with_files(input_file_path, encrypted=encrypted_file_path)


def test_specify_decryption_filename(tmp_path: pathlib.Path) -> None:
    input_file_path = tmp_path / "input.txt"
    create_test_file(input_file_path)
    decrypt_file_path = tmp_path / "decrypt.html"
    assert not decrypt_file_path.exists()
    run_with_files(input_file_path, decrypt=decrypt_file_path)


def test_specify_all_filenames(tmp_path: pathlib.Path) -> None:
    input_file_path = tmp_path / "input.txt"
    create_test_file(input_file_path)
    decrypt_file_path = tmp_path / "decrypt.html"
    encrypted_file_path = tmp_path / "encrypted_content"
    assert not decrypt_file_path.exists()
    assert not encrypted_file_path.exists()
    run_with_files(
        input_file_path, encrypted=encrypted_file_path, decrypt=decrypt_file_path
    )


def test_empty_password(tmp_path: pathlib.Path) -> None:
    input_file_path = tmp_path / "input.txt"
    create_test_file(input_file_path)
    run_with_files(input_file_path, password="")
