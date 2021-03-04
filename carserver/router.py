from carserver import app

@app.route('/', methods=['POST', 'GET'])
def index():
    return 'hello world'

"""
Database: DriveS_v2
Measurement: usertable
Tag: username
Field: password_hash, public_id

Measurement: data
Tag: uuid, launch, public_id
Field: velocity, acceleration, gyroscope, latitude, longitude

API:
Route: /register
Methods: ['GET', 'POST']
Token: not required
Header:
    Authorization: <type> <credentials>
* Explanation of header authorization:
    it contains the encoded username-password pair,
    Swift provides API for this commonly used header

Route: /login
Methods: ['GET', 'POST']
Token: not required
Header:
    Authorization: <type> <credentials>

Route: /upload
Methods: ['POST']
Token: required
Header: 
    x-access-tokens: <token>
Body:
    * Same as the original version, i.e.
    * Format of request in Swift
    * let body = ["UserID":uuid,
    *             "LaunchTimestamp":LAUNCH_TIMESTAMP,
    *             "Data":uploadBuffer 
    *            ] as Dictionary<String, String>
    * Format of each line in Data in Swift
    * uploadBuffer += (Date().GetTime+",\(velocity),\(accCal[1]),\(gyroCal[2]),\(latitude),\(longitude),\n")
"""

from carserver.routes import login
from carserver.routes import motiondata
from carserver.routes import replay
from carserver.routes import label
# from carserver.routes import label

# if  __name__ == '__main__': 
#     from werkzeug.middleware.proxy_fix import ProxyFix
#     app.wsgi_app = ProxyFix(app.wsgi_app)

#     # app.run(debug=True) 
#     app.run(host='0.0.0.0', port=5001, debug=True)
