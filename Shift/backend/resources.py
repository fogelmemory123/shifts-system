from flask_restful import Resource, reqparse
from models import db, User, Shift
from flask import jsonify,request,make_response
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

user_parser = reqparse.RequestParser()
user_parser.add_argument('username', required=True, help='Username cannot be blank')
user_parser.add_argument('password', required=True, help='Password cannot be blank')


class Logout(Resource):
    @jwt_required()
    def post(self):
        response = make_response(jsonify({'status': 'success', 'message': 'Logged out successfully'}), 200)

        return response


class UserRegistration(Resource):
    def post(self):
        data = user_parser.parse_args()
        if User.query.filter_by(username=data['username']).first():
            return {'message': 'User already exists'}, 400
        user = User(username=data['username'])
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(username=data['username']).first()
        access_token = create_access_token(identity=user.id)
        access_id = user.id
        return {'access_token': access_token,'access_id':access_id}, 200







class UserLogin(Resource):
    def post(self):
        data = user_parser.parse_args()
        user = User.query.filter_by(username=data['username']).first()

        if not user:
            return {'message': 'Invalid username'}, 401

        if not user.check_password(data['password']):
            return {'message': 'Invalid password'}, 401

        # Set a very long expiration time, e.g., 100 years
        access_token = create_access_token(identity=user.id)
        access_id = user.id

        return {
            'access_token': access_token,
            'access_id': access_id,
            'expires_in': None  # Indicate that the token does not expire
        }, 200





class AddShifts(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {'status': 'fail', 'message': 'User not found'}, 404

        data = request.get_json()
        date = data['date']
        shiftType = data['shiftType']
        location = data['location']

        # Check if a shift already exists for this date, shift type, and user
        existing_shift = Shift.query.filter_by(date=date, shiftType=shiftType, user_id=user.id).first()

        if existing_shift:
            # Update the existing shift
            existing_shift.location = location
            db.session.commit()
            return {'status': 'success', 'message': 'Shift updated', 'data': {'id': existing_shift.id, 'username': user.username, 'date': date, 'shiftType': shiftType, 'location': location}}
        else:
            # Create a new shift
            new_shift = Shift(date=date, shiftType=shiftType, location=location, user_id=user.id)
            db.session.add(new_shift)
            db.session.commit()
            return {'status': 'success', 'message': 'Shift created', 'data': {'id': new_shift.id, 'username': user.username, 'date': date, 'shiftType': shiftType, 'location': location}}




class GetShifts(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {'status': 'fail', 'message': 'User not found'}, 404

        shifts = Shift.query.filter_by(user_id=user.id).all()
        shift_data = [{'date': shift.date, 'shiftType': shift.shiftType, 'location': shift.location} for shift in shifts]
        return {'status': 'success', 'data': shift_data}


class GetAllShifts(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {'status': 'fail', 'message': 'User not found'}, 404

        shifts = Shift.query.all()
        shift_data = [
            {
                'date': shift.date,
                'shiftType': shift.shiftType,
                'location': shift.location,
                'username': shift.user.username  # Assuming relationship is set up
            }
            for shift in shifts
        ]
        return {'status': 'success', 'data': shift_data}

class GetUserName(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        return {'username':user.username}
