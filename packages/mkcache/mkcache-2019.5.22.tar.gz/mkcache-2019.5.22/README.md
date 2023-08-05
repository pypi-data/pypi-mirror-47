<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/badge/OS-Unix-blue.svg?longCache=True)]()

#### Installation
```bash
$ [sudo] pip install mkcache
```

#### How it works
```
$XDG_CACHE_HOME/mkcache/<hash>
```

#### Config
```bash
export MKCACHE=path/to/cache # ~/.cache/mkcache by default
```

#### Scripts usage
command|`usage`
-|-
`mkcache` |`usage: mkcache args ...`

#### Examples
speed up macOS tts with mkcache:
```bash
path="$(mkcache "$@")"
! [ -e "$path" ] && /usr/bin/say "$@" -o "$path"
afplay "$path"
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>