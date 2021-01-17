from flask import Flask, request 
from influxdb import InfluxDBClient
import json



app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def index():
    return 'hello world'
 
@app.route('/register', methods=['GET','POST'])
def register():
    '''
    * Format of request in Swift
    * let body = ["UserID":uuid,
    *             "LaunchTimestamp":LAUNCH_TIMESTAMP,
    *             "Data":uploadBuffer 
    *            ] as Dictionary<String, String>
    * Format of each line in Data in Swift
    * uploadBuffer += (Date().GetTime+",\(velocity),\(accCal[1]),\(gyroCal[2]),\(latitude),\(longitude),\n")
    '''
    # parse request
    data = json.loads(request.get_data(as_text=True))
    UserID = data['UserID']
    LaunchTimestamp = data['LaunchTimestamp']
    Data = data['Data']
    # print(UserID)
    # print(LaunchTimestamp)
    # print(Data)

    # save into files
    filename = UserID + '+' + LaunchTimestamp
    file = open(filename + '.csv', 'a')
    file.write(Data)

    # save into database
    client = InfluxDBClient('localhost', 8086, 'root', 'root', 'DriveS')
    client.create_database('DriveS')
    Data = Data.splitlines()
    for line in Data:
        line = line.split(',')
        # print(line)
        body = [
            {
                "measurement": "data",
                "time": line[0],
                "tags":{
                    "uuid": UserID,
                    "launch": LaunchTimestamp
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

    return 'Package Received'
 
if __name__ == '__main__':
    from werkzeug.contrib.fixers import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)
    
    app.run(host = '0.0.0.0',port = 5000)

