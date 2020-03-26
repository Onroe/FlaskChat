from flask import Flask, request, jsonify, render_template, redirect
import os
import pusher
# Import databases
from database import db_session
from models import User, Channel, Message
#Generate and check hash code or token
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from flask_socketio import SocketIO


#Token authentication

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
import os
import pusher

app = Flask(__name__)
#CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['JWT_SECRET_KEY'] = 'something-super-secret'  # Change this!
jwt = JWTManager(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return jsonify("Pong!")

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')    

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('RESPONSE', json, callback=messageReceived)   
 
    
# User registration
@app.route('/api/register/', methods=["POST"])
def register():
        data = request.get_json()
        username = data.get("username")
        password = generate_password_hash(data.get("password"))

        try:
            new_user = User(username=username, password=password)
            db_session.add(new_user)
            db_session.commit()
        except:
            return jsonify({
                "status": "error",
                "message": "Could not add user"
            })

        return jsonify({
            "status": "success",
            "message": "User added successfully"
        }), 201

# User Login
@app.route('/api/login/', methods=["POST","GET"])
def login():
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            return jsonify({
                "status": "failed",
                "message": "Failed getting user"
            }), 401

        # Generate a token
        access_token = create_access_token(identity=username)

        return jsonify({
            "status": "success",
            "message": "login successful",
            "data": {
                "id": user.id,
                "token": access_token,
                "username": user.username
            }
        }), 200            

    # run Flask app
if __name__ == "__main__":
    app.run()

# Close session after database operation
@app.teardown_appcontext
def shutdown_session(exception=None):
        db_session.remove()    