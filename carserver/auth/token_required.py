from flask import request, jsonify
import jwt
from functools import wraps

from carserver import app
from carserver import client

def token_required(f):  
    @wraps(f)  
    def decorator(*args, **kwargs):

        token = None 

        if 'x-access-tokens' in request.headers:  
            token = request.headers['x-access-tokens'] 

        if not token:  
            return jsonify({'message': 'a valid token is missing'}), 400

        data = jwt.decode(token, 
                          key=app.config['SECRET_KEY'],
                          algorithms="HS256") 
        try:  
            username = data['username']
            results = client.query("SELECT * from usertable where username='{}';".format(username))
            points = results.get_points()
            size = sum(1 for point in points)
            if size == 0:
                return jsonify({'message': 'do not find user'}), 400
            if size > 1:
                return jsonify({'message': 'multiple user with same username found'}), 400
        except:  
            return jsonify({'message': 'token is invalid'})  

        return f(username, *args,  **kwargs)  

    return decorator 
