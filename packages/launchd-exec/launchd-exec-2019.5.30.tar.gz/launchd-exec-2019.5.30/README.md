<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/badge/OS-MacOS-blue.svg?longCache=True)]()

#### Installation
```bash
$ [sudo] pip install launchd-exec
```

#### Scripts usage
command|`usage`
-|-
`launchd-exec` |`usage: launchd-exec command [args ...]`

#### Examples
```bash
$ launchd-exec bash -l path/to/script.sh
launchd-exec.<hash> # label

$ pid="$(/bin/launchctl list | grep "$label" | awk '{print $1}')"
```

logs:
```
~/Library/Logs/launchd-exec/<hash>/out.log
~/Library/Logs/launchd-exec/<hash>/err.log
~/Library/Logs/launchd-exec/<hash>/launchd.plist
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>