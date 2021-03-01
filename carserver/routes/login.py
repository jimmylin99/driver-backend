from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta

from carserver import app, client

@app.route('/register', methods=['GET', 'POST'])
def signup_user():  
    
    auth = request.authorization   

    if not auth or not auth.username or not auth.password:  
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})    

    username = auth.username
    results = client.query("SELECT * from usertable where username='{}';".format(username))
    points = results.get_points()
    size = sum(1 for point in points)
    if size > 0:
        return jsonify({'message': 'user name is registered'}), 400

    password_hash = generate_password_hash(auth.password, method='sha256')

    json_body = [
        {
            "measurement": "usertable",
            "time": datetime.utcnow().isoformat("T") + "Z",
            "tags": {
                "username": username
            },
            "fields": {
                "password_hash": password_hash
            }
        }
    ]
    client.write_points(json_body)

    return jsonify({'message': 'registered successfully'}), 200


@app.route('/login', methods=['GET', 'POST'])  
def login_user(): 

    auth = request.authorization   

    if not auth or not auth.username or not auth.password:  
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})    

    username = auth.username
    results = client.query("SELECT * from usertable where username='{}';".format(username))
    points = results.get_points(tags={'username': username})
    size = 0
    for _point in points:
        size += 1
        if size == 1:
            point = _point
    if size == 0:
        return jsonify({'message': 'user not found'}), 400

    password_hash = point['password_hash']
        
    if check_password_hash(password_hash, auth.password):  
        token = jwt.encode({'username': username, 'exp' : datetime.utcnow() + timedelta(days=9999)}, 
                           app.config['SECRET_KEY'],
                           algorithm="HS256")  
        return jsonify({'token' : token}), 200

    return make_response('could not verify',  401, {'WWW-Authentication': 'Basic realm: "login required"'})
