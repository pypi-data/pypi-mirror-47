<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/badge/OS-macOS-blue.svg?longCache=True)]()
[![](https://img.shields.io/pypi/pyversions/mac-speech-commands.svg?longCache=True)](https://pypi.org/project/mac-speech-commands/)

#### Installation
```bash
$ [sudo] pip install mac-speech-commands
```

#### Functions
function|`__doc__`
-|-
`mac_speech_commands.replace(text, functions)` |replace speech commands in text with functions output

#### Examples
russian minutes plural:
```python
import mac_speech_commands
import plural_ru

def ru_minutes(value):
    return "%s %s" % (value.replace("1","одну"),plural_ru.ru(int(value),['минуту','минуты','минут']))

text="... длится [[ru:minutes 10]]"
functions = {"ru:minutes":ru_minutes}

mac_speech_commands.replace(text,functions)
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>