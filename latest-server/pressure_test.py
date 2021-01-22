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

records_num = 3000
url = 'http://server.acemap.cn:24050'


def short_data():
    return datetime.utcnow().isoformat("T") + "Z" + \
             ',1.0,1.0,0.1,120,30,\n'


long_data = ''
for i in range(records_num):
    long_data += short_data()

json_body = {
    "UserID": 1,
    "LaunchTimestamp": datetime.utcnow().isoformat("T"),
    "Data": long_data
}
# register
# r = requests.post(url=url+'/register', auth=('mike', '123'))
# login
# r = requests.post(url=url+'/login', auth=('mike', '123'))
#upload
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiI3MDIzNWMwNi1jNzYxLTQzYzctYTA2My02NjQwMjA1YmVjYTEiLCJleHAiOjE2NDI2NTEzMTV9.s5iYigksac-loZSokLoTy1GjaSWJwB_6Ctnv8ohqmdQ"
r = requests.post(url=url+'/upload', json=json_body,
                  headers={'x-access-tokens': access_token})
print(r.headers)
print(r.status_code)
print(r.text)
