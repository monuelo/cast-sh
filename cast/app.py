#!/usr/bin/env python3
import os
import sys
import select
import shlex
import random
import string
import argparse

from flask import Flask
import flask_socketio
from flask_jwt_extended import JWTManager

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


from .routes import *
from .events import *

app.register_blueprint(http, url_prefix=r"")


def create_parser():
    parser = argparse.ArgumentParser(
        description=(
            "An adorable instance of your terminal in your browser."
            "https://github.com/pipeflow/cast-sh"
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
    print("serving on http://0.0.0.0:{}".format(args.port))
    socketio.run(app, host="0.0.0.0", debug=args.debug, port=args.port)


if __name__ == "__main__":
    main()
