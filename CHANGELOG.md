# What's new?

## [0.2.1] - 2022-10-27
### Added
- `<title>` for decrypt template

### Fixed
- Don't ask for password from stdin if empty password was supplied with `-p ""`
- Minor code formatting issues in decrypt template
- Issue with Safari Browser: Decrypted content was not shown after click

## [0.2.0] - 2022-10-26
### Added
- Testcases using `tox`

### Changed
- Improve decrypt template. Centered `<div>`, `DOCTYPE`, UTF-8
- set argparse `prog` based on `__name__`
- Set minimum python version to 3.9

### Fixed
- Fix default encrypted filename not placing files next to decrypt file in subfolder

## [0.1.0] - 2022-10-25
### Added
- Check that provided file arguments are unique files
- `--decrypt` argument to generate decryption `.html` file

### Changed
- Rename `-o --output` arg to `-e --encrypted`.

## Unreleased - 2022-10-25
### Added
- Encrypt file with command line tool
- First version packaged with `setuptools` + `pyproject.toml`
