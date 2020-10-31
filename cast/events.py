import os
import pty
import subprocess
import shlex

from flask import current_app as app
from flask import request

from .logger import Logging
from .app import socketio, read_and_forward_pty_output


@socketio.on("client-input", namespace="/cast")
def client_input(data):
    # Update current session
    app.config["current_session"] = data["session_id"]
    print("input: {}".format(app.config["sessions"]))
    log = Logging(app.config["current_session"])

    if data["session_id"] in app.config["sessions"]:
        file_desc = app.config["sessions"][data["session_id"]]["fd"]

        if file_desc:
            if data["input"] == "":
                # When switching sessions, send a key to update terminal content
                os.write(file_desc, b"\x00")
            else:
                log.write_log(data["input"])
                os.write(file_desc, data["input"].encode())


@socketio.on("connect", namespace="/cast")
def connect(data=None):
    session_id = (
        request.values.get("session_id")
        if not request.values.get("session_id") is None
        else ""
    )
    if session_id == "" and data is not None:
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
            target=read_and_forward_pty_output, session_id=session_id
        )

        print("connect: task started")


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
            target=read_and_forward_pty_output, session_id=session_id
        )

        print("new-session: task started")
