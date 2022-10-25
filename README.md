# HTMLCrypt

Inspired/Based on [MaxLaumeister/PageCrypt](https://github.com/MaxLaumeister/PageCrypt).

## Usage

`decrypt.html` decrypts `content.html.encrypted` from same folder. Change `const encryptedFileName = 'content.html.encrypted';` to change to a different filename.

Use `python3 -m htmlcrypt -p $PASS -o content.html.encrypted input_file.html` to encrypt `input_file.html` with password from `$PASS`.

```
usage: python -m htmlcrypt [-h] [-p PASSWORD] [-o OUTPUT] [-f] file

Encrypt HTML file with password

positional arguments:
  file                  File to encrypt

options:
  -h, --help            show this help message and exit
  -p PASSWORD, --password PASSWORD
                        Password for encrypting/decrypting. Will ask for password from stdin if not specified
  -o OUTPUT, --output OUTPUT
                        Encrypted filename
  -f, --force           Overwrite existing output file
```
