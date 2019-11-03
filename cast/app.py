#!/usr/bin/env python3
import argparse
from flask import Flask, render_template, request, send_from_directory
import flask_socketio
from werkzeug.exceptions import BadRequest

from .logger import Logging
import pty
import os
import subprocess
import select
import shlex

__version__ = "0.0.1"

app = Flask(__name__, template_folder=".",
            static_folder=".", static_url_path="")
app.config["fd"] = None
app.config["child_pid"] = None
app.config["current_session"] = None
app.config["sessions"] = {}
app.config["log_file"] = r'log_data/'
socketio = flask_socketio.SocketIO(app)


def read_and_forward_pty_output(session_id):
    max_read_bytes = 1024 * 20
    app.config["current_session"] = session_id

    while True:

        socketio.sleep(0.01)

        if session_id in app.config["sessions"]:
            file_desc = app.config["sessions"][app.config["current_session"]]["fd"]

            if file_desc:
                timeout_sec = 0
                (data_ready, _, _) = select.select(
                    [file_desc], [], [], timeout_sec)
                if data_ready:
                    output = os.read(file_desc, max_read_bytes).decode()
                    socketio.emit(
                        "client-output", {"output": output, "ssid": app.config["current_session"]}, namespace="/cast")


@app.route("/")
def index():
    log = Logging(app.config["current_session"])
    log.make_log_folder()
    return render_template("index.html")


@socketio.on("new-session", namespace="/cast")
def new_session(data=None):
    """To register session on WebSocket server
    Similar to 'connect()', used for adding a new tab session
    """
    session_id = ''
    if data is not None:
        session_id = data["session_id"]
    print("new-session: {}\n".format(session_id))

    if session_id in app.config["sessions"]:
        return

    (child_pid, fd) = pty.fork()

    if child_pid == 0:
        # child: run system command
        subprocess.run(app.config["cmd"])
    else:
        # parent: stream input/output from child to Socketio web channel
        app.config["sessions"][session_id] = {}
        app.config["sessions"][session_id]["fd"] = fd
        app.config["sessions"][session_id]["child_pid"] = child_pid

        cmd = " ".join(shlex.quote(c) for c in app.config["cmd"])

        print("new-session: child pid is", child_pid)
        print(
            "new-session: starting background task with command `{}` to continously read "
            "and forward pty output to client".format(cmd)
        )
        """
        print(
            f"new-session: starting background task with command `{cmd}` to continously read "
            "and forward pty output to client"
        )
        """

        socketio.start_background_task(
            target=read_and_forward_pty_output, session_id=session_id)

        print("new-session: task started")


@socketio.on("connect", namespace="/cast")
def connect(data=None):
    session_id = request.values.get('session_id') if not request.values.get(
        'session_id') is None else ''
    if session_id == '' and data is not None:
        session_id = data["session_id"]
        print("connect: {}\n".format(session_id))

    # Create new session only when id not in records
    if session_id in app.config["sessions"]:
        return

    (child_pid, fd) = pty.fork()

    if child_pid == 0:
        # child: start system command
        subprocess.run(app.config["cmd"])
    else:
        # parent: print info, stream child input/output to socketio
        # Store sessions by ssid
        print("opening a new session")
        app.config["sessions"] = {}
        app.config["sessions"][session_id] = {}
        app.config["sessions"][session_id]["fd"] = fd
        app.config["sessions"][session_id]["child_pid"] = child_pid

        cmd = " ".join(shlex.quote(c) for c in app.config["cmd"])

        print("connect: child pid is", child_pid)
        print(
            "connect: starting background task with command `{}` to continously read "
            "and forward pty output to client".format(cmd)
        )
        """
        print(
            f"new-session: starting background task with command `{cmd}` to continously read "
            "and forward pty output to client"
        )
        """

        # Output terminal message corresponding to ssid
        socketio.start_background_task(
            target=read_and_forward_pty_output, session_id=session_id)

        print("connect: task started")


@socketio.on("client-input", namespace="/cast")
def client_input(data):
    # Update current session
    app.config["current_session"] = data["session_id"]
    print("input: {}".format(app.config['sessions']))
    log = Logging(app.config["current_session"])

    if data["session_id"] in app.config["sessions"]:
        file_desc = app.config["sessions"][data["session_id"]]["fd"]

        if file_desc:
            if data["input"] == '':
                # When switching sessions, send a key to update terminal content
                os.write(file_desc, b'\x00')
            else:
                log.write_log(data['input'])
                os.write(file_desc, data["input"].encode())


# This is the route handler for DOWNLOADING the log file. Maybe a bit buggy. Please report if found

@app.route("/download/<string:file_path>")
def download(file_path):
    try:
        return send_from_directory(app.config["log_file"], filename=file_path, as_attachment=True)
    except BadRequest as e:
        return 404


def main():
    parser = argparse.ArgumentParser(
        description=(
            "An adorable instance of your terminal in your browser."
            "https://github.com/hericlesme/cast-sh"
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-p", "--port", default=5000,
                        help="port to run server on")
    parser.add_argument("--debug", action="store_true",
                        help="debug the server")
    parser.add_argument("--version", action="store_true",
                        help="print version and exit")
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
    print("serving on http://0.0.0.0:{}".format(args.port))
    app.config["cmd"] = [args.command] + shlex.split(args.cmd_args)
    socketio.run(app, host="0.0.0.0", debug=args.debug, port=args.port)


if __name__ == "__main__":
    main()
