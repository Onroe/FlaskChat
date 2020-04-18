from flask_restful import Resource, reqparse
from flask import request, Flask, jsonify, render_template, redirect,  make_response
from werkzeug.security import generate_password_hash, check_password_hash
import os
from database import db_session
from models import User, Channel, Message
import datetime
import app
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)


class SignUp(Resource):
   def post(self):
       data = request.get_json()
       username = data.get("username")
       password = generate_password_hash(data.get("password"))
       
       if User.find_by_username(data['username']):
            return make_response( jsonify({'message': 'Account {} already exists'.format(data['username']), 'status':'failure'}))

       elif (data.get("password") != data.get("cpassword")):
            return make_response( jsonify({'message': 'Passwords dont match','status':'failure'}))

       else:      
            try:
               new_user = User(username=username, password=password)
               db_session.add(new_user)
               db_session.commit()
            except:
                return make_response(jsonify({
                "status": "error",
                "message": "Could not add user"
            }))

            return make_response( jsonify({
            "status": "success",
            "message": "User added successfully"
        }), 201)


class SignIn(Resource):
   def post(self):
      
       data = request.get_json()
       username = data.get("username")
       password = data.get("password")
       user = User.query.filter_by(username=username).first()

       if not user or not check_password_hash(user.password, password):
            return make_response(jsonify({
                "status": "failed",
                "message": "Incorrect username and password"
            }), 401)

        # Generate a token
       access_token = create_access_token(identity=username, expires_delta=datetime.timedelta(seconds=300))
       refresh_token = create_refresh_token(identity=username, expires_delta=datetime.timedelta(seconds=300))

       #tokenz = jwt.encode({'user' : username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=30)},app.app.config['JWT_SECRET_KEY'] = 'abeba')

       return make_response(jsonify({
            "status": "success",
            "message": "login successful",
            "id": user.id,
            "token": access_token,
            "ref_token": refresh_token,
            "username": user.username,
            "data": {
               
            }
        }), 200)          

class UserList(Resource):
    @jwt_required
    def get(self):
        users = User.query.all()
        return make_response(jsonify(
        [{"id": user.id, "userName": user.username} for user in users]
    ), 200)
        db_session.remove()


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity = current_user, fresh=False)
        return make_response(jsonify({'access_token': new_token}), 200 )


class InitiateChat(Resource):
    @jwt_required  
    def post(self):
        request_data = request.get_json()
        from_user = request_data.get('from_user', '')
        to_user = request_data.get('to_user', '')
    #to_user_channel = "private-notification_user_%s" % (to_user)
    #from_user_channel = "private-notification_user_%s" % (from_user)

    # check if there is a channel that already exists between this two user
        channel = Channel.query.filter(Channel.from_user.in_([from_user, to_user])) \
                           .filter(Channel.to_user.in_([from_user, to_user])) \
                           .first()
        if not channel:
        # Generate a channel...
           chat_channel = "private-chat_%s_%s" % (from_user, to_user)

           new_channel = Channel()
           new_channel.from_user = from_user
           new_channel.to_user = to_user
           new_channel.name = chat_channel
           db_session.add(new_channel)
           db_session.commit()
           db_session.remove()
        else:
        # Use the channel name stored on the database
           chat_channel = channel.id

        data = {
        "from_user": from_user,
        "to_user": to_user,
        #"from_user_notification_channel": from_user_channel,
        #"to_user_notification_channel": to_user_channel,
        "channel_name": chat_channel,
         }

    # Trigger an event to the other user
    #pusher.trigger(to_user_channel, 'new_chat', data)

        return make_response(jsonify(data))
        


class SendMessage(Resource):   
    #@socketio.on('event')
    def message(self, json):
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

    def messageReceived(methods=['GET', 'POST']):
      print('message was received!!!')    
    

class Messages(Resource):
    #@jwt_required  
    def post(self):
        data = request.get_json() 
        channel = data.get("channelid")
        #print(channel)
        messages = Message.query.filter(Message.channel_id == channel).all()
        db_session.remove()

        return make_response(jsonify([
        {
            "id": message.id,
            "message": message.message,
            "to_user": message.to_user,
            "channel_id": message.channel_id,
            "from_user": message.from_user,
            "timestamp":message.timestamp,
        }
        for message in messages
    ]))