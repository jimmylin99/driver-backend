import requests
from datetime import date, datetime
'''
* let body = ["UserID":uuid,
*             "LaunchTimestamp":LAUNCH_TIMESTAMP,
*             "Data":uploadBuffer 
*            ] as Dictionary<String, String>
* Format of each line in Data in Swift
* uploadBuffer += (Date().GetTime+",\(velocity),\(accCal[1]),\(gyroCal[2]),\(latitude),\(longitude),\n")
'''

records_num = 0
url = 'http://59.78.28.3:5000/register'

short_data = datetime.utcnow().isoformat("T") + "Z" + \
             ',1.0,1.0,0.1,120,30,\n'
long_data = ''
for i in range(records_num):
    long_data += short_data

json_body = {
    "UserID": 1,
    "LaunchTimestamp": datetime.utcnow().isoformat("T"),
    "Data": long_data
}

r = requests.post(url=url, json=json_body)
print(r.headers)
print(r.status_code)
print(r.text)
