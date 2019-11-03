![cast-sh](art/cast-sh-header.png)
<p align="center">
    <a href="https://travis-ci.org/pod-cast/cast-sh">
        <img src="https://travis-ci.org/pod-cast/cast-sh.svg?branch=master"
            alt="Build Status"/></a>
    <a href="https://github.com/pod-cast/cast-sh/graphs/contributors" alt="Contributors">
        <img src="https://img.shields.io/github/contributors/pod-cast/cast-sh" /></a>
    <a href='https://coveralls.io/github/pod-cast/cast-sh'><img src='https://coveralls.io/repos/github/pod-cast/cast-sh/badge.svg' alt='Coverage Status' /></a>
    <a href="https://www.python.org/downloads/">
        <img src="https://img.shields.io/badge/python-3.5%20%7C%203.6%20%7C%203.7-blue"
            alt="Python 3.5-3.7"/></a>
    <a href="https://github.com/pod-cast/cast-sh/pulse" alt="Activity">
        <img src="https://img.shields.io/github/commit-activity/m/pod-cast/cast-sh" /></a>
    <a href="https://github.com/pod-cast/cast-sh/blob/master/LICENSE" alt="License">
        <img src="https://img.shields.io/github/license/pod-cast/cast-sh" /></a>
    <a href="https://app.fossa.com/projects/git%2Bgithub.com%2Fpod-cast%2Fcast-sh?ref=badge_shield" alt="FOSSA Status"><img src="https://app.fossa.com/api/projects/git%2Bgithub.com%2Fpod-cast%2Fcast-sh.svg?type=shield"/></a>
    <a href="https://lgtm.com/projects/g/pod-cast/cast-sh/alerts/">
        <img src="https://img.shields.io/lgtm/alerts/g/pod-cast/cast-sh"
            alt="Total alerts"/></a>
    <a href="https://lgtm.com/projects/g/pod-cast/cast-sh/context:python"><img alt="Language grade: Python" src="https://img.shields.io/lgtm/grade/python/g/pod-cast/cast-sh.svg?logo=lgtm&logoWidth=18"/></a>
    <a href="https://lgtm.com/projects/g/pod-cast/cast-sh/context:javascript"><img alt="Language grade: JavaScript" src="https://img.shields.io/lgtm/grade/javascript/g/pod-cast/cast-sh.svg?logo=lgtm&logoWidth=18"/></a>
</p>

## Installation & Prerequisites
Use the package manager pip to install the dependencies before run the application
```
pip3 install -r requirements.txt
```

## Usage
To start the terminal cast application, run:
```
python3 -m cast
```
#### Arguments
```
optional arguments:

  -h, --help                show this help message and exit
  -p [PORT], --port [PORT]  port to run server on (default: 5000)
  --debug                   debug the server (default: False)
  --version                 print version and exit (default: False)
  --command COMMAND         Command to run in the terminal (default: bash)
  --cmd-args CMD_ARGS       arguments to pass to command (i.e. --cmd-args='arg1
                            arg2 --flag') (default: )
```
#### Docker
Build image
```
docker build -t cast .
```
Run built image
```
docker run --name cast.sh-container -p 5000:5000/tcp -i -t cast
```
## Screenshots
![screenshots](/art/screenshots.png)

## Contributing
![Contribute](/art/contribute.svg)
[![](https://sourcerer.io/fame/hericlesme/pod-cast/cast-sh/images/0)](https://sourcerer.io/fame/hericlesme/pod-cast/cast-sh/links/0)[![](https://sourcerer.io/fame/hericlesme/pod-cast/cast-sh/images/1)](https://sourcerer.io/fame/hericlesme/pod-cast/cast-sh/links/1)[![](https://sourcerer.io/fame/hericlesme/pod-cast/cast-sh/images/2)](https://sourcerer.io/fame/hericlesme/pod-cast/cast-sh/links/2)[![](https://sourcerer.io/fame/hericlesme/pod-cast/cast-sh/images/3)](https://sourcerer.io/fame/hericlesme/pod-cast/cast-sh/links/3)[![](https://sourcerer.io/fame/hericlesme/pod-cast/cast-sh/images/4)](https://sourcerer.io/fame/hericlesme/pod-cast/cast-sh/links/4)[![](https://sourcerer.io/fame/hericlesme/pod-cast/cast-sh/images/5)](https://sourcerer.io/fame/hericlesme/pod-cast/cast-sh/links/5)[![](https://sourcerer.io/fame/hericlesme/pod-cast/cast-sh/images/6)](https://sourcerer.io/fame/hericlesme/pod-cast/cast-sh/links/6)[![](https://sourcerer.io/fame/hericlesme/pod-cast/cast-sh/images/7)](https://sourcerer.io/fame/hericlesme/pod-cast/cast-sh/links/7)

## License
<a href="https://app.fossa.com/projects/git%2Bgithub.com%2Fpod-cast%2Fcast-sh?ref=badge_large" alt="FOSSA Status"><img src="https://app.fossa.com/api/projects/git%2Bgithub.com%2Fpod-cast%2Fcast-sh.svg?type=large"/></a>

## Code of Conduct
Everyone interacting with the [cast-sh](https://github.com/pod-cast/cast-sh) codebase and issue tracker is expected to follow our [Code of Conduct](https://github.com/pod-cast/cast-sh/blob/dev/CODE_OF_CONDUCT.md).
