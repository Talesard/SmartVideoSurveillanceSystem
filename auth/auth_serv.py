from flask import Flask, request, jsonify
from config import Config
import utils

app = Flask(__name__)
app.config.from_object(Config)

def unauth_error(resp_json):
    resp_json["status"] = "error"
    resp_json["error_message"] = "Unauthorized"
    status_code = 401
    return resp_json, status_code

@app.route('/get_user', methods=['POST'])
def get_user():
    data = request.json
    resp_json = {"status": "ok", "error_message": ""}
    status_code = 200
    if not utils.check_token(data["token"]):
        resp_json, status_code = unauth_error(resp_json)
    else:
        user = utils.get_user(data["username"])
        resp_json["data"] = user
    return jsonify(resp_json), status_code

@app.route('/save_user', methods=['POST'])
def save_user():
    data = request.json
    resp_json = {"status": "ok", "error_message": ""}
    status_code = 200
    if not utils.check_token(data["token"]):
        resp_json, status_code = unauth_error(resp_json)
    else:
        error_message = utils.save_user(data["username"], data["password"], data["password2"], data["email"], data["invitation_token"])
        if (error_message):
            resp_json["status"] = "err"
            resp_json["error_message"] = error_message
            status_code = 400
    return jsonify(resp_json), status_code

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    print(data)
    resp_json = {"status": "ok", "error_message": ""}
    status_code = 200
    if not utils.check_token(data["token"]):
        resp_json, status_code = unauth_error(resp_json)
    else:
        error_message = utils.login(data["username"], data["password"])
        if error_message:
            resp_json["status"] = "err"
            resp_json["error_message"] = error_message
            status_code = 400
    return jsonify(resp_json), status_code

if __name__ == '__main__':
    app.run(debug=True, port=Config.AUTH_PORT)