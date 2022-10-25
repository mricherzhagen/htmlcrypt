# HTMLCrypt

Inspired/Based on [MaxLaumeister/PageCrypt](https://github.com/MaxLaumeister/PageCrypt).

## Usage

`decrypt.html` decrypts `content.html.encrypted` from same folder. Change `const encryptedFileName = 'content.html.encrypted';` to change to a different filename.

Use `htmlcrypt -p $PASS -o content.html.encrypted input_file.html` to encrypt `input_file.html` with password from `$PASS`.

```
usage: htmlcrypt [-h] [-p PASSWORD] [-e ENCRYPTED] [-d DECRYPT] [-f] file

Encrypt HTML file with password

positional arguments:
  file                  File to encrypt

options:
  -h, --help            show this help message and exit
  -p PASSWORD, --password PASSWORD
                        Password for encrypting/decrypting. Will ask for password from stdin if not specified
  -e ENCRYPTED, --encrypted ENCRYPTED
                        Encrypted filename
  -d DECRYPT, --decrypt DECRYPT
                        Location to generate the decryption .html file. Relative path to encrypted file will be injected into file.
  -f, --force           Overwrite existing output file
```
