from flask import Blueprint,Response,request,json
from src import db
from src.services.user_service import check_unique_credentials,find_user
import datetime
import os
import jwt
import bcrypt
import traceback
auth = Blueprint('auth',__name__)

User = db['users']


@auth.route('/signin',methods=['POST'])
def handle_signin():
    try: 
        data = request.json
        user = {}
        if ("email" in data or "username" in data) and ("password" in data):
            if "email" in data:
                email = data['email']
                user = find_user({'email':email})
            else:
                print(data['username'])
                username = data['username']
                user = find_user({'username':username})
            password = data['password']
            # if user records exists we will check user password
            if user:
                # check user password
                if bcrypt.checkpw(password.encode('utf-8'),user["password"]):
                    # user password matched, we will generate token
                    payload = {
                        '_id': str(user['_id']),
                        'username': user['username'],
                        }
                    token = jwt.encode(payload,os.getenv('JWT_SECRET_KEY'),algorithm='HS256')
                    return Response(
                            response=json.dumps({'status': "success",
                                                "message": "User Sign In Successful",
                                                "token": token}),
                            status=200,
                            mimetype='application/json'
                        )
                
                else:
                    return Response(
                        response=json.dumps({'status': "failed", "message": "User Password Mistmatched"}),
                        status=401,
                        mimetype='application/json'
                    ) 
            # if there is no user record
            else:
                return Response(
                    response=json.dumps({'status': "failed", "message": "User Record doesn't exist, kindly register"}),
                    status=404,
                    mimetype='application/json'
                ) 
        else:
            # if request parameters are not correct 
            return Response(
                response=json.dumps({'status': "failed", "message": "User Parameters Email and Password are required"}),
                status=400,
                mimetype='application/json'
            )
        
    except Exception as e:
        print(traceback.format_exc())
        return Response(
                response=json.dumps({'status': "failed", 
                                     "message": "Error Occured",
                                     "error": str(e)}),
                status=500,
                mimetype='application/json'
            )
    
@auth.route('/signup',methods=['POST'])
def handle_signup():
    try: 
        data = request.json
        if 'email' in data  and 'password' in data and 'username' in data:
            print('password' in data)
            email = data['email']
            password = data['password']
            username = data['username']
            user_in_db = check_unique_credentials(username,email)
            if user_in_db:
                return json.jsonify({'status':'failed','message':'user already exists'})
            
            password = password.encode('utf-8')
            salt = bcrypt.gensalt() 
            hashed_password = bcrypt.hashpw(password,salt)
            new_user = {
                'email':email,
                'username':username,
                'password':hashed_password
            }
            user = User.insert_one(new_user)
            print(user.inserted_id)
            payload = {
                        '_id': str(user.inserted_id),
                        'username': username,
                        }
            token = jwt.encode(payload,os.getenv('JWT_SECRET_KEY'),algorithm='HS256')
            return json.jsonify({'status': "success","message": "User Sign In Successful","token": token})
        else:
            return json.jsonify({'status': "failed", "message": "User Parameters Email and Password are required"})
                
        
    except Exception as e:
        print(traceback.format_exc())
        return json.jsonify({'status': "failed", "message": "Error Occured", "error": str(e)})
                
