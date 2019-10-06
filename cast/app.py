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
app.config["current_session"] = None
app.config["sessions"] = {}
socketio = SocketIO(app)

def setup_default_session(session_id):
    app.config["current_session"] = session_id
    app.config["sessions"][session_id] = {"fd": None, "child_pid": None}

    return app.config["sessions"][session_id]

def read_and_forward_pty_output(session_id):
    max_read_bytes = 1024 * 20
    app.config["current_session"] = session_id
    while True:

        if session_id in app.config["sessions"]:
            file_desc = app.config["sessions"][app.config["current_session"]]["fd"]

            socketio.sleep(0.01)
            if file_desc:
                timeout_sec = 0
                (data_ready, _, _) = select.select([file_desc], [], [], timeout_sec)
                if data_ready:
                    output = os.read(file_desc, max_read_bytes).decode()
                    socketio.emit("client-output", {"output": output, "ssid": app.config["current_session"] }, namespace="/cast")


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("client-input", namespace="/cast")
def client_input(data):

    # Update current session
    app.config["current_session"] = data["session_id"]
    print("input: {}".format(app.config["sessions"]))

    if data["session_id"] in app.config["sessions"]:
        file_desc = app.config["sessions"][data["session_id"]]["fd"]

        if file_desc:
            if data["input"] == '':
                # When switching session, send a key to update terminal content
                os.write(file_desc, b'\x00')
            else:
                os.write(file_desc, data["input"].encode())


@socketio.on("new-session", namespace="/cast")
def new_session(data=None):
    """To register session on WebSocket server
    Similar to 'connect()'
    """
    session_id = ''
    if data is not None:
        session_id = data["session_id"]
    print("new-session: {}\n\n".format(session_id))

    if session_id in app.config["sessions"].keys():
        return


    (child_pid, fd) = pty.fork()

    if child_pid == 0:
        subprocess.run(app.config["cmd"])
    else:
        app.config["sessions"][session_id] = {}
        app.config["sessions"][session_id]["fd"] = fd
        app.config["sessions"][session_id]["child_pid"] = child_pid

        cmd = " ".join(shlex.quote(c) for c in app.config["cmd"])

        print("child pid is", child_pid)
        print(
            "starting background task with command `{cmd}` to continously read "
            "and forward pty output to client"
        )

        socketio.start_background_task(target=read_and_forward_pty_output, session_id=session_id)

        print("task started")


@socketio.on("connect", namespace="/cast")
def connect():
    session_id = request.values.get('session_id') if not request.values.get('session_id') == None else ''
    if session_id == '' and data is not None:
        session_id = data["session_id"]
        print("new-session: {}\n\n".format(session_id))

    # Create new session only when ssid does not in records
    if session_id in app.config["sessions"].keys():
        return


    (child_pid, fd) = pty.fork()

    if child_pid == 0:
        subprocess.run(app.config["cmd"])
    else:
        # Store sessions by ssid
        app.config["sessions"][session_id] = {}
        app.config["sessions"][session_id]["fd"] = fd
        app.config["sessions"][session_id]["child_pid"] = child_pid
       
        cmd = " ".join(shlex.quote(c) for c in app.config["cmd"])
       
        print("child pid is", child_pid)
        print(
            "starting background task with command `{cmd}` to continously read "
            "and forward pty output to client"
        )
       
        # Output terminal message corresponding to ssid
        socketio.start_background_task(target=read_and_forward_pty_output, session_id=session_id)
       
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
