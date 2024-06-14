from datetime import timedelta
from flask import Flask, render_template, session
from flask_jwt_extended import JWTManager
from routes import api_blueprint
from config import Config
from flask_cors import CORS
import flask_monitoringdashboard as dashboard

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)
jwt = JWTManager(app)

app.register_blueprint(api_blueprint)

dashboard.config.init_from(file='dashboard.cfg')
dashboard.bind(app)

@app.route('/')
def index():
    username = session.get('username')
    return render_template('index.html', username=username)

if __name__ == '__main__':
    app.run(debug=True)
