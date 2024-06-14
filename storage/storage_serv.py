from flask import Flask, request, jsonify
from config import Config
from flask_cors import CORS
import database
import utils

app = Flask(__name__)
app.config.from_object(Config)

def unauth_error(resp_json):
    resp_json["status"] = "error"
    resp_json["error_message"] = "Unauthorized"
    status_code = 401
    return resp_json, status_code

@app.route('/get_all_logs', methods=['POST'])
def get_all_logs():
    data = request.json
    resp_json = {"status": "ok", "error_message": ""}
    status_code = 200
    if not utils.check_token(data["token"]):
        resp_json, status_code = unauth_error(resp_json)
    else:
        resp_json["data"] = database.get_all_logs()
    return jsonify(resp_json), status_code


@app.route('/get_logs_by_date', methods=['POST'])
def get_logs_by_date():
    data = request.json
    resp_json = {"status": "ok", "error_message": ""}
    status_code = 200
    if not utils.check_token(data["token"]):
        resp_json, status_code = unauth_error(resp_json)
    else:
        start_date = data["start_date"]
        end_date = data["end_date"]
        resp_json["data"] = database.get_logs_by_dates(start_date, end_date)
    return jsonify(resp_json), status_code

@app.route('/get_log_by_id', methods=['POST'])
def get_log_by_id():
    data = request.json
    resp_json = {"status": "ok", "error_message": ""}
    status_code = 200
    if not utils.check_token(data["token"]):
        resp_json, status_code = unauth_error(resp_json)
    else:
        id = data["id"]
        resp_json["data"] = database.get_log_by_id(id)
    return jsonify(resp_json), status_code

@app.route('/save_log', methods=['POST'])
def save_log():
    data = request.json
    resp_json = {"status": "ok", "error_message": ""}
    status_code = 200
    if not utils.check_token(data["token"]):
        resp_json, status_code = unauth_error(resp_json)
    else:
        type = data["type"]
        video_id = data["video_id"]
        database.save_log(type, video_id)
    return jsonify(resp_json), status_code

@app.route('/get_all_fragments', methods=['POST'])
def get_all_fragments():
    data = request.json
    resp_json = {"status": "ok", "error_message": ""}
    status_code = 200
    if not utils.check_token(data["token"]):
        resp_json, status_code = unauth_error(resp_json)
    else:
        resp_json["data"] = database.get_all_fragments()
        return jsonify(resp_json), status_code

@app.route('/get_fragment_by_id', methods=['POST'])
def get_fragment_by_id():
    data = request.json
    resp_json = {"status": "ok", "error_message": ""}
    status_code = 200
    if not utils.check_token(data["token"]):
        resp_json, status_code = unauth_error(resp_json)
    else:
        id = data["id"]
        resp_json["data"] = database.get_fragment_by_id(id)
    return jsonify(resp_json), status_code

@app.route('/save_fragment', methods=['POST'])
def save_fragment():
    data = request.json
    resp_json = {"status": "ok", "error_message": ""}
    status_code = 200
    if not utils.check_token(data["token"]):
        resp_json, status_code = unauth_error(resp_json)
    else:
        id = database.save_fragment(data["file_base64"])
        resp_json["id"] = id
    return jsonify(resp_json), status_code

@app.route('/get_user', methods=['POST'])
def get_user():
    data = request.json
    resp_json = {"status": "ok", "error_message": ""}
    status_code = 200
    if not utils.check_token(data["token"]):
        resp_json, status_code = unauth_error(resp_json)
    else:
        username = data["username"]
        resp_json["data"] = database.get_user(username)
    return jsonify(resp_json), status_code

@app.route('/save_user', methods=['POST'])
def save_user():
    data = request.json
    resp_json = {"status": "ok", "error_message": ""}
    status_code = 200
    if not utils.check_token(data["token"]):
        resp_json, status_code = unauth_error(resp_json)
    else:
        username = data["username"]
        password_hash = data["password_hash"]
        email = data["email"]
        if database.get_user(username):
            resp_json["status"] = "error"
            resp_json["error_message"] = "A user with this username is already registered"
        user = database.save_user(username, password_hash, email)
    return jsonify(resp_json), status_code


if __name__ == '__main__':
    app.run(debug=True, port=Config.STORAGE_PORT)
