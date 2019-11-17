#!/usr/bin/env python3
import argparse

from flask import (
    Flask,
    render_template,
    request,
    send_from_directory,
    redirect,
    jsonify,
)

import sys

import flask_socketio

from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    set_access_cookies,
)

from werkzeug.exceptions import BadRequest
import json
from .logger import Logging
import pty
import os
import subprocess
import select
import shlex
import random
import string

__version__ = "0.0.1"

app = Flask(__name__, template_folder=".", static_folder=".", static_url_path="")

app.config["fd"] = None
app.config["logged"] = False
app.config["child_pid"] = None
app.config["current_session"] = None
app.config["sessions"] = {}
app.config["log_file"] = r"log_data/"
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]


def random_string(string_length=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(string_length))


app.config["JWT_SECRET_KEY"] = random_string()

jwt = JWTManager(app)
socketio = flask_socketio.SocketIO(app)


def update_session_logger(data):
    app.config["current_session"] = data["session_id"]
    log = Logging(app.config["current_session"])
    return log


def write_input(file_descriptor, data, log):
    if file_descriptor:
        if data["input"] == "":
            os.write(file_descriptor, b"\x00")
        else:
            log.write_log(data["input"])
            os.write(file_descriptor, data["input"].encode())


def read_and_forward_pty_output(session_id):
    max_read_bytes = 1024 * 2
    app.config["current_session"] = session_id

    while True:

        socketio.sleep(0.01)

        if session_id in app.config["sessions"]:
            file_desc = app.config["sessions"][app.config["current_session"]]["fd"]

            if file_desc:
                timeout_sec = 0
                (data_ready, _, _) = select.select([file_desc], [], [], timeout_sec)
                if data_ready:
                    try:
                        output = os.read(file_desc, max_read_bytes).decode()
                        if len(output) > 3 or output == r"\b":
                            socketio.emit(
                                "client-output",
                                {
                                    "output": output,
                                    "ssid": app.config["current_session"],
                                },
                                namespace="/cast",
                            )
                    except OSError:
                        socketio.emit("disconnect", namespace="/cast")
                        sys.exit(0)


@jwt.unauthorized_loader
def unauthorized_response(callback):
    return redirect("/")


@jwt.invalid_token_loader
def invalid_token(callback):
    return redirect("/")


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.route("/cast")
@jwt_required
def index():
    log = Logging(app.config["current_session"])
    log.make_log_folder()
    return render_template("index.html")


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    elif request.method == "POST":
        data = request.json
        if data["password"] == app.config["passwd"]:
            access_token = create_access_token(identity=os.getenv("JOB_ID"))
            resp = jsonify({"login": True})
            set_access_cookies(resp, access_token)
            return resp
        else:
            return json.dumps(request.get_json()), 401


@socketio.on("new-session", namespace="/cast")
def new_session(data=None):
    """To register session on WebSocket server
    Similar to 'connect()', used for adding a new tab session
    """
    session_id = ""
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
            f"new-session: starting background task with command `{cmd}` to continously read "
            "and forward pty output to client"
        )

        socketio.start_background_task(
            target=read_and_forward_pty_output, session_id=session_id
        )

        print("new-session: task started")


@socketio.on("connect", namespace="/cast")
def connect(data=None):
    session_id = (
        request.values.get("session_id")
        if not request.values.get("session_id") is None
        else ""
    )
    if session_id == "" and data is not None:
        session_id = data["session_id"]
        print(f"connect: {session_id}\n")

    # Create new session only when id not in records
    if session_id in app.config["sessions"]:
        return

    (child_pid) = pty.fork()

    # child: start system command
    if child_pid == 0:
        subprocess.run(app.config["cmd"])
    else:
        new_session(data={"session_id": session_id})
        print("connect: task started")


@socketio.on("client-input", namespace="/cast")
def client_input(data):
    log = update_session_logger(data)
    if data["session_id"] in app.config["sessions"]:
        file_desc = app.config["sessions"][data["session_id"]]["fd"]
        write_input(file_desc, data, log)


# This is the route handler for DOWNLOADING the log file. Maybe a bit buggy. Please report if found
@app.route("/download/<string:file_path>")
def download(file_path):
    try:
        return send_from_directory(
            app.config["log_file"], filename=file_path, as_attachment=True
        )
    except BadRequest:
        return 404


def create_parser():
    parser = argparse.ArgumentParser(
        description=(
            "An adorable instance of your terminal in your browser."
            "https://github.com/pod-cast/cast-sh"
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-p", "--port", default=5000, help="port to run server on")
    parser.add_argument("--debug", action="store_true", help="debug the server")
    parser.add_argument("--version", action="store_true", help="print version and exit")
    parser.add_argument("--password", default="admin", help="cast password")
    parser.add_argument(
        "--command", default="bash", help="Command to run in the terminal"
    )
    parser.add_argument(
        "--cmd-args",
        default="",
        help="arguments to pass to command (i.e. --cmd-args='arg1 arg2 --flag')",
    )
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    if args.version:
        print(__version__)
        sys.exit(0)

    env_pass = os.getenv("PASSWORD")
    if env_pass is not None:
        app.config["passwd"] = env_pass
    else:
        app.config["passwd"] = args.password

    app.config["cmd"] = [args.command] + shlex.split(args.cmd_args)
    print(f"serving on http://0.0.0.0:{args.port}")
    socketio.run(app, host="0.0.0.0", debug=args.debug, port=args.port)


if __name__ == "__main__":
    main()
