from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from threading import Thread
from config import config
from flask_cors import CORS
import telebot


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

subscribers = []
alarm_active = False
secret_token = config["secret_token"]

def notify_tg(message):
    if not config["tg_enabled"]:
        return
    bot=telebot.TeleBot(config["tg_token"])
    for user_id in config["tg_user_ids"]:
         bot.send_message(user_id, message)
    bot.stop_bot()

@app.route('/start_alarm', methods=['POST'])
def start_alarm():
    data = request.json
    if data.get('secret_token') == secret_token:
        global alarm_active
        alarm_active = True
        notify_subscribers('start_alarm')
        notify_tg("Alarm!!! Check what happened ASAP!!!")
        return jsonify({'status': 'Alarm started'}), 200
    else:
        return jsonify({'error': 'Invalid token'}), 403

@app.route('/stop_alarm', methods=['POST'])
def stop_alarm():
    data = request.json
    if data.get('secret_token') == secret_token:
        global alarm_active
        alarm_active = False
        notify_subscribers('stop_alarm')
        notify_tg("The alarm is off.")
        return jsonify({'status': 'Alarm stopped'}), 200
    else:
        return jsonify({'error': 'Invalid token'}), 403

def notify_subscribers(message):
    global subscribers
    for subscriber in subscribers:
        emit(message, broadcast=True, namespace='/alarm', to=subscriber)

@socketio.on('connect', namespace='/alarm')
def connect():
    global subscribers
    subscribers.append(request.sid)
    print(f"Client connected: {request.sid}")

@socketio.on('disconnect', namespace='/alarm')
def disconnect():
    global subscribers
    subscribers.remove(request.sid)
    print(f"Client disconnected: {request.sid}")

def run_flask_app():
    socketio.run(app, host='0.0.0.0', port=5555)

if __name__ == '__main__':
    flask_thread = Thread(target=run_flask_app)
    flask_thread.start()