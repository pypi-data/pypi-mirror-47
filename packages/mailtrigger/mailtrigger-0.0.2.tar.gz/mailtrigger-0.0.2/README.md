# Mail Trigger

[![PyPI](https://img.shields.io/pypi/v/mailtrigger.svg?color=brightgreen)](https://pypi.org/project/mailtrigger/)
[![Travis](https://travis-ci.com/craftslab/mailtrigger.svg?branch=master)](https://travis-ci.com/craftslab/mailtrigger)
[![Coverage Status](https://coveralls.io/repos/github/craftslab/mailtrigger/badge.svg?branch=master)](https://coveralls.io/github/craftslab/mailtrigger?branch=master)
[![License](https://img.shields.io/github/license/craftslab/mailtrigger.svg?color=brightgreen)](https://github.com/craftslab/mailtrigger/blob/master/LICENSE)



## Requirements

- Python (3.7+)
- pip
- python-dev



## Installation

On Ubuntu / Mint, install *Mail Trigger* with the following commands:

```bash
sudo apt update
sudo apt install python3-dev python3-pip python3-setuptools
sudo pip3 install mailtrigger
```

On OS X, install *Mail Trigger* via [Homebrew](https://brew.sh/) (or via [Linuxbrew](https://linuxbrew.sh/) on Linux):

```
TBD
```

On Windows, install *Mail Trigger* with the following commands:

```
TBD
```



## Updating

```bash
pip3 install mailtrigger --upgrade
```



## Settings

Several *Mail Trigger* parameters can be set in the file [config.json](https://github.com/craftslab/mailtrigger/blob/master/source/config/config.json).

An example of config.json:

```
{
  "debug": false,
  "pop3": {
    "host": "pop.example.com",
    "pass": "pass",
    "port": 995,
    "ssl": true,
    "user": "user"
  },
  "smtp": {
    "host": "smtp.example.com",
    "pass": "pass",
    "port": 465,
    "ssl": true,
    "user": "user"
  }
}
```



## Usage

### Title

```
[trigger]: Write your description here
```

**Note: `[trigger]` is the reserved word in title**



### Recipient

The recipient is mail receiver as *Mail Trigger*.



### Content

#### Gerrit Trigger

```
@gerrit help
@gerrit list
@gerrit restart <host>
@gerrit start <host>
@gerrit stop <host>
@gerrit verify <host>

@gerrit <host>:<port> review
  [--project <PROJECT> | -p <PROJECT>]
  [--branch <BRANCH> | -b <BRANCH>]
  [--message <MESSAGE> | -m <MESSAGE>]
  [--notify <NOTIFYHANDLING> | -n <NOTIFYHANDLING>]
  [--submit | -s]
  [--abandon | --restore]
  [--rebase]
  [--move <BRANCH>]
  [--publish]
  [--json | -j]
  [--delete]
  [--verified <N>] [--code-review <N>]
  [--label Label-Name=<N>]
  [--tag TAG]
  {COMMIT | CHANGEID,PATCHSET}
```



#### Jenkins Trigger

```
@jenkins help
@jenkins list
@jenkins <host>:<port> build JOB [--parameter <PARAMETER> | -p <PARAMETER>]
@jenkins <host>:<port> list
@jenkins <host>:<port> query JOB
@jenkins <host>:<port> rebuild JOB
@jenkins <host>:<port> stop JOB
@jenkins <host>:<port> verify JOB
```



#### Jira Trigger

```
@jira help
```



#### Trigger Help

```
@help
```



## License Apache

Project License can be found [here](https://github.com/craftslab/mailtrigger/blob/master/LICENSE).
