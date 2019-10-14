# cast.sh

<p align="left">
    <a href="https://github.com/hericlesme/cast-sh/graphs/contributors" alt="Contributors">
        <img src="https://img.shields.io/github/contributors/hericlesme/cast-sh" /></a>
    <a href="https://github.com/hericlesme/cast-sh/pulse" alt="Activity">
        <img src="https://img.shields.io/github/commit-activity/m/hericlesme/cast-sh" /></a>
    <a href="https://lgtm.com/projects/g/hericlesme/cast-sh/alerts/">
        <img src="https://img.shields.io/lgtm/alerts/g/hericlesme/cast-sh"
            alt="Total alerts"/></a>
</p>

An adorable instance of your terminal in your browser


## Prerequisites
You need to install the dependencies before run the application
```
pip3 install -r requirements.txt
```

## Run
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
