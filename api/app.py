from flask import Flask, request, jsonify, render_template, redirect, make_response
from database import Config
# Import databases
from database import db_session
from models import User, Channel, Message
#Generate and check hash code or token

from flask_cors import CORS
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_restful import Api
import resources, models

#Token authentication
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity,create_refresh_token,jwt_refresh_token_required
)


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['JWT_SECRET_KEY'] = 'abeba'  # Change this!
jwt = JWTManager(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Database migration
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/flasks'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app= app,)

@app.route('/')
def index():
    return jsonify("Pong!")


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')    


@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('RESPONSE', json, callback=messageReceived)   

@app.route('/', methods=['POST'])
@socketio.on('event')
def message(json):
    #for key, value in json.items():
    #  print('Received:' + key, value)  
    
    from_user = json.get('from_user')
    to_user = json.get('to_user')
    message = json.get('message')
    channel = json.get('channel')
    timestamp = json.get('timestamp')

    new_message = Message(message=message, channel_id=channel)
    new_message.from_user = from_user
    new_message.to_user = to_user
    new_message.timestamp = timestamp
    db_session.add(new_message)
    db_session.commit()

    message = {
        "from_user": from_user,
        "to_user": to_user,
        "message": message,
        "channel": channel,
        "timestamp": timestamp,
    }
    print('RECEIVED:' + str(message))  
    socketio.emit('RESPONSE', message, callback=messageReceived) 
    return make_response(jsonify(message))
    
    
# Close connection when not in use
@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()    
 


api.add_resource(resources.SignUp, '/api/signup')
api.add_resource(resources.SignIn, '/api/signin')
api.add_resource(resources.UserList,'/api/userlist')
api.add_resource(resources.TokenRefresh,'/api/refresh')
api.add_resource(resources.InitiateChat,'/api/initiatechat')
api.add_resource(resources.Messages,'/api/getmessages')
api.add_resource(resources.SendMessage,'/api/sendmessage')

    # run Flask app
if __name__ == "__main__":
    app.run()

