#!/usr/bin/env python3
import argparse
from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room
import pty
import os
import subprocess
import select
import termios
import struct
import fcntl
import shlex

__version__ = "0.0.1"

app = Flask(__name__, template_folder=".", static_folder=".", static_url_path="")
app.config["fd"] = None
app.config["child_pid"] = None
app.config["curr_session"] = None
app.config["sessions"] = {}
socketio = SocketIO(app)

def read_and_forward_pty_output():
    max_read_bytes = 1024 * 20
    while True:
        session = app.config["sessions"][app.config["curr_session"]]

        socketio.sleep(0.01)
        if app.config["sessions"][app.config["curr_session"]]["fd"]:
            timeout_sec = 0
            (data_ready, _, _) = select.select([app.config["sessions"][app.config["curr_session"]]["fd"]], [], [], timeout_sec)
            if data_ready:
                output = os.read(app.config["sessions"][app.config["curr_session"]]["fd"], max_read_bytes).decode()
                socketio.emit("client-output", {"output": output }, namespace="/cast")


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("client-input", namespace="/cast")
def client_input(data):

    print(data["session_id"])

    if app.config["sessions"][data["session_id"]]["fd"]:
        os.write(app.config["sessions"][data["session_id"]]["fd"], data["input"].encode())
        app.config["curr_session"] = data["session_id"]

@socketio.on("connect", namespace="/cast")
def connect():

    session_id = request.args.get('session_id')
        
    app.config["curr_session"] = session_id
    
    app.config["sessions"][session_id] = {"fd": None, "child_pid": None}



    if (app.config["sessions"][session_id]["child_pid"]):
        # (child_pid2, fd2) = pty.fork()
        # app.config["fd2"] = fd2
        # app.config["child_pid2"] = child_pid2
        # cmd2 = " ".join(shlex.quote(c) for c in app.config["cmd"])
        return

    (child_pid, fd) = pty.fork()

    if child_pid == 0:
        subprocess.run(app.config["cmd"])
    else:
        print(session_id)
        app.config["sessions"][session_id]["fd"] = fd
        app.config["sessions"][session_id]["child_pid"] = child_pid
       
        cmd = " ".join(shlex.quote(c) for c in app.config["cmd"])
       
        print("child pid is", child_pid)
        print(
            "starting background task with command `{cmd}` to continously read "
            "and forward pty output to client"
        )
       
        socketio.start_background_task(target=read_and_forward_pty_output)
       
        print("task started")


def main():
    parser = argparse.ArgumentParser(
        description=(
            "An adorable instance of your terminal in your browser."
            "https://github.com/hericlesme/cast-sh"
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-p", "--port", default=5000, help="port to run server on")
    parser.add_argument("--debug", action="store_true", help="debug the server")
    parser.add_argument("--version", action="store_true", help="print version and exit")
    parser.add_argument(
        "--command", default="bash", help="Command to run in the terminal"
    )
    parser.add_argument(
        "--cmd-args",
        default="",
        help="arguments to pass to command (i.e. --cmd-args='arg1 arg2 --flag')",
    )
    args = parser.parse_args()
    if args.version:
        print(__version__)
        exit(0)
    print(f"serving on http://0.0.0.0:{args.port}")
    app.config["cmd"] = [args.command] + shlex.split(args.cmd_args)
    socketio.run(app, host="0.0.0.0", debug=args.debug, port=args.port)


if __name__ == "__main__":
    main()
