<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/badge/OS-macOS-blue.svg?longCache=True)]()

#### Installation
```bash
$ [sudo] pip install mac-open-apps
```

#### Scripts usage
command|`usage`
-|-
`open-apps` |`usage: open-apps app ...`

#### Examples
```bash
$ open-apps Discord iTerm "Google Chrome" Skype "Sublime Text" Terminal
```

`~/Library/LaunchAgents/apps.plist`
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>apps</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/open-apps</string>
        <string>Discord</string>
        <string>iTerm</string>
        <string>Google Chrome</string>
        <string>Skype</string>
        <string>Sublime Text</string>
        <string>Terminal</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>