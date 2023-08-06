# Mail Trigger

[![PyPI](https://img.shields.io/pypi/v/mailtrigger.svg?color=brightgreen)](https://pypi.org/project/mailtrigger/)
[![Travis](https://travis-ci.com/craftslab/mailtrigger.svg?branch=master)](https://travis-ci.com/craftslab/mailtrigger)
[![Coverage](https://coveralls.io/repos/github/craftslab/mailtrigger/badge.svg?branch=master)](https://coveralls.io/github/craftslab/mailtrigger?branch=master)
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

Several *Mail Trigger* parameters can be set in the directory [config](https://github.com/craftslab/mailtrigger/blob/master/mailtrigger/config).

An example of configuration in [mailer.json](https://github.com/craftslab/mailtrigger/blob/master/mailtrigger/config/mailer.json):

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

An example of configuration in [scheduler.json](https://github.com/craftslab/mailtrigger/blob/master/mailtrigger/config/scheduler.json):

```
{
  "interval": 10
}
```

An example of configuration in [trigger.json](https://github.com/craftslab/mailtrigger/blob/master/mailtrigger/config/trigger.json):

```
{
  "gerrit": {
    "host": "localhost",
    "port": 8080
  },
  "jenkins": {
    "host": "localhost",
    "port": 8081
  },
  "jira": {
    "host": "localhost",
    "port": 8082
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

@gerrit review <host>:<port>
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
@jenkins build <host>:<port> JOB [--parameter <PARAMETER> | -p <PARAMETER>]
@jenkins help
@jenkins list
@jenkins list <host>:<port>
@jenkins query <host>:<port> JOB
@jenkins rebuild <host>:<port> JOB
@jenkins stop <host>:<port> JOB
@jenkins verify <host>:<port> JOB
```



#### Jira Trigger

```
TBD
```



#### Trigger Help

```
@help
```



## License Apache

Project License can be found [here](https://github.com/craftslab/mailtrigger/blob/master/LICENSE).
