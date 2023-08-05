<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/badge/OS-macOS-blue.svg?longCache=True)]()

#### Installation
```bash
$ [sudo] pip install mac-speech-cache
```

#### How it works
```
~/Library/Caches/speech-cache/<hash>.aiff
```

#### Scripts usage
command|`usage`
-|-
`speech-cache` |`usage: speech-cache [-v voice] [-f in | message]`

#### Examples
```bash
# say "$@"
$ afplay "$(speech-cache "$@")"
```

make cache for multiple files and voices:
```bash
$ find . -name "*.txt" | xargs -I{} speech-cache -f {} -v Milena
$ find . -name "*.txt" | xargs -I{} speech-cache -f {} -v Yuri
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>