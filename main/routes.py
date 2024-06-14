from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import get_db
import utils
from config import Config


api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/logs', methods=['GET', 'POST'])
@jwt_required()
def logs():
    if request.method == 'GET':
        logs = utils.get_all_logs()
        username = get_jwt_identity()
        return render_template('logs.html', logs=logs, username=username)

    if request.method == 'POST':
        data = request.json
        utils.turn_on_alarm_notification_conditional(data['type'])
        utils.save_log(data['type'], data['video_id'])
        return jsonify({"msg": "Log created"}), 200

@api_blueprint.route('/fragments', methods=['GET', 'POST'])
@jwt_required()
def fragments():
    if request.method == 'GET':
        fragments = utils.get_all_fragments()
        username = get_jwt_identity()
        return render_template('fragments.html', fragments=fragments, username=username)

    if request.method == 'POST':
        data = request.json
        id = utils.save_fragment(data['file_base64'])
        return jsonify({"msg": "Fragment uploaded", "video_id": id}), 200

@api_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        error_message = utils.login(data["username"], data["password"])
        print(error_message)
        if error_message:
            return jsonify({"msg": error_message}), 401
        access_token = create_access_token(identity=data["username"])
        session['username'] = data["username"]
        return jsonify(access_token=access_token), 200
    return render_template('login.html')

@api_blueprint.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect('/'), 302

@api_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        error_message = utils.save_user(data['username'], data['password'], data['password2'], data['email'], data["invitation_token"])
        if error_message:
            return render_template('register.html', error=error_message)
        return redirect(url_for('api.login'))
    return render_template('register.html')

@api_blueprint.route('/notify', methods=['GET', 'POST'])
@jwt_required()
def notify():
    if request.method == 'GET':
        return jsonify({"msg": "GET request received"}), 200
    if request.method == 'POST':
        return jsonify({"msg": "POST request received"}), 200


@api_blueprint.route('/alarm', methods=['GET'])
def alarm():
    return render_template('alarm.html', username="test")

@api_blueprint.route('/get_fragment_by_id/<video_id>', methods=['GET'])
def get_fragment_by_id(video_id):
    fragment_base64 = utils.get_fragment(video_id)
    return render_template('fragment.html', gif_base64=fragment_base64, username="test")
