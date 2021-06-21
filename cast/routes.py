import json
import os

from werkzeug.exceptions import BadRequest
from flask import (
    Blueprint,
    request,
    redirect,
    render_template,
    send_from_directory,
    jsonify,
)
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    set_access_cookies,
)

from .logger import Logging
from .app import jwt, app

http = Blueprint("", __name__)


@jwt.unauthorized_loader
def unauthorized_response(callback):
    return redirect("/")


@jwt.invalid_token_loader
def invalid_token(callback):
    return redirect("/")


@http.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@http.route("/cast")
@jwt_required()
def index():
    log = Logging(app.config["current_session"])
    log.make_log_folder()
    return render_template("index.html")


@http.route("/", methods=["GET", "POST"])
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


# This is the route handler for DOWNLOADING the log file. Maybe a bit buggy. Please report if found
@http.route("/download/<string:file_path>")
def download(file_path):
    try:
        return send_from_directory(
            app.config["log_file"], filename=file_path, as_attachment=True
        )
    except BadRequest:
        return 404
