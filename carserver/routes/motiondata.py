from flask import request, jsonify
import json

from carserver import app, client
from carserver.auth.token_required import token_required

@app.route('/upload', methods=['POST'])
@token_required
def create_author(username):
    '''
    * Format of request in Swift
    * let body = ["UserID":uuid,
    *             "LaunchTimestamp":LAUNCH_TIMESTAMP,
    *             "Data":uploadBuffer 
    *            ] as Dictionary<String, String>
    * Format of each line in Data in Swift
    * uploadBuffer += (Date().GetTime+",\(velocity),\(accCal[1]),\(gyroCal[2]),\(latitude),\(longitude),\n")
    '''
    try:
        data = json.loads(request.get_data(as_text=True))
        uuid = data['UserID']
        LaunchTimestamp = data['LaunchTimestamp']
        Data = data['Data']

        Data = Data.splitlines()
        for line in Data:
            line = line.split(',')
            # print(line)
            body = [
                {
                    "measurement": "data",
                    "time": line[0],
                    "tags":{
                        "uuid": uuid,
                        "launch": LaunchTimestamp,
                        "username": username
                    },
                    "fields": {
                        "velocity":float(line[1]),
                        "acceleration":float(line[2]),
                        "gyroscope":float(line[3]),
                        "latitude":float(line[4]),
                        "longitude":float(line[5])
                    }
                }
            ]
            client.write_points(body)

        return jsonify({'message' : 'package received'}), 200

    except:

        return jsonify({'message' : 'error occured'}), 400
