<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/badge/OS-macOS-blue.svg?longCache=True)]()

#### Installation
```bash
$ [sudo] pip install mac-tag-sync
```

#### Requirements
```bash
$ brew install tag
```

#### Scripts usage
command|`usage`
-|-
`tag-sync` |`usage: tag-sync tag path ...`

#### Examples
```bash
$ find ~/git -type d -mindepth 1 -maxdepth 1 | xargs tag-sync "repo"
$ find ~/git -type d -name "*.py" -mindepth 1 -maxdepth 1 | xargs tag-sync "py"
```

#### Links
+   [github.com/jdberry/tag](https://github.com/jdberry/tag)

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>