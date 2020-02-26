![cast-sh](art/cast-sh-header.png)
<p align="center">
    <a href="https://github.com/PipeFlow/cast-sh/actions?query=workflow%3A%22build%22">
        <img src="https://github.com/PipeFlow/cast-sh/workflows/build/badge.svg"
            alt="Build Status"/></a>
    <a href="https://github.com/PipeFlow/cast-sh/graphs/contributors" alt="Contributors">
        <img src="https://img.shields.io/github/contributors/PipeFlow/cast-sh" /></a>
    <a href='https://coveralls.io/github/PipeFlow/cast-sh?branch=dev'><img src='https://coveralls.io/repos/github/PipeFlow/cast-sh/badge.svg?branch=dev' alt='Coverage Status' /></a>
    <a href="https://www.python.org/downloads/">
        <img src="https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-blue"
            alt="Python 3.5-3.7"/></a>
    <a class="reference external" href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
    <a href="https://github.com/PipeFlow/cast-sh/pulse" alt="Activity">
        <img src="https://img.shields.io/github/commit-activity/m/pipeflow/cast-sh" /></a>
    <a href="https://github.com/PipeFlow/cast-sh/blob/dev/LICENSE" alt="License">
        <img src="https://img.shields.io/github/license/PipeFlow/cast-sh" /></a>
    <a href="https://app.fossa.com/projects/git%2Bgithub.com%2Fpod-cast%2Fcast-sh?ref=badge_shield" alt="FOSSA Status"><img src="https://app.fossa.com/api/projects/git%2Bgithub.com%2Fpod-cast%2Fcast-sh.svg?type=shield"/></a>
    <a href="https://gitter.im/PipeFlowOrg/cast-sh?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge" alt="Gitter"><img src="https://badges.gitter.im/PipeFlowOrg/cast-sh.svg"/></a>
    <a href="https://lgtm.com/projects/g/PipeFlow/cast-sh/alerts/">
        <img src="https://img.shields.io/lgtm/alerts/g/PipeFlow/cast-sh"
            alt="Total alerts"/></a>
    <a href="https://lgtm.com/projects/g/PipeFlow/cast-sh/context:python"><img alt="Language grade: Python" src="https://img.shields.io/lgtm/grade/python/g/PipeFlow/cast-sh.svg?logo=lgtm&logoWidth=18"/></a>
    <a href="https://lgtm.com/projects/g/PipeFlow/cast-sh/context:javascript"><img alt="Language grade: JavaScript" src="https://img.shields.io/lgtm/grade/javascript/g/PipeFlow/cast-sh.svg?logo=lgtm&logoWidth=18"/></a>
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
  --password PASSWORD       set a password for accessing cast-sh
                            sessions (default: admin)
```
#### A password can be set using an environment variable as well.
Unix
```
export PASSWORD="weakpassword"
```
Windows
```
set PASSWORD="weakpassword"
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
[![](https://sourcerer.io/fame/hericlesme/pipeflow/cast-sh/images/0)](https://sourcerer.io/fame/hericlesme/pipeflow/cast-sh/links/0)[![](https://sourcerer.io/fame/hericlesme/pipeflow/cast-sh/images/1)](https://sourcerer.io/fame/hericlesme/pipeflow/cast-sh/links/1)[![](https://sourcerer.io/fame/hericlesme/pipeflow/cast-sh/images/2)](https://sourcerer.io/fame/hericlesme/pipeflow/cast-sh/links/2)[![](https://sourcerer.io/fame/hericlesme/pipeflow/cast-sh/images/3)](https://sourcerer.io/fame/hericlesme/pipeflow/cast-sh/links/3)[![](https://sourcerer.io/fame/hericlesme/pipeflow/cast-sh/images/4)](https://sourcerer.io/fame/hericlesme/pipeflow/cast-sh/links/4)[![](https://sourcerer.io/fame/hericlesme/pipeflow/cast-sh/images/5)](https://sourcerer.io/fame/hericlesme/pipeflow/cast-sh/links/5)[![](https://sourcerer.io/fame/hericlesme/pipeflow/cast-sh/images/6)](https://sourcerer.io/fame/hericlesme/pipeflow/cast-sh/links/6)[![](https://sourcerer.io/fame/hericlesme/pipeflow/cast-sh/images/7)](https://sourcerer.io/fame/hericlesme/pipeflow/cast-sh/links/7)

## License
<a href="https://app.fossa.com/projects/git%2Bgithub.com%2Fpod-cast%2Fcast-sh?ref=badge_large" alt="FOSSA Status"><img src="https://app.fossa.com/api/projects/git%2Bgithub.com%2Fpod-cast%2Fcast-sh.svg?type=large"/></a>

## Code of Conduct
Everyone interacting with the [cast-sh](https://github.com/PipeFlow/cast-sh) codebase and issue tracker is expected to follow our [Code of Conduct](https://github.com/PipeFlow/cast-sh/blob/dev/CODE_OF_CONDUCT.md).
