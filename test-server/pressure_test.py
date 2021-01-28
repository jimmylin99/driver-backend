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

records_num = 1
url = 'http://server.acemap.cn:24050'
# url = 'http://localhost:5001'


def short_data():
    return datetime.utcnow().isoformat("T") + "Z" + \
             ',1.0,1.0,0.1,120,30,\n'


long_data = ''
for i in range(records_num):
    long_data += short_data()

json_body = {
    "UserID": 1,
    "LaunchTimestamp": datetime.utcnow().isoformat("T") + "Z",
    "Data": long_data
}
# register
# r = requests.post(url=url+'/register', auth=('mike2', '123'))
# login
# r = requests.post(url=url+'/login', auth=('mike2', '123'))
#upload
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Im1pa2UyIiwiZXhwIjoxNjQyOTE5NjA4fQ.J-yczjSd2ZiVjQnRV6jXxw6DeBLpd5RiVeywsuz1aAs"
from time import perf_counter
T1 = perf_counter()
r = requests.post(url=url+'/upload', json=json_body,
                  headers={'x-access-tokens': access_token})
T2 = perf_counter()
print(f'time elapsed: {(T2 - T1):3f} s')
print(r.headers)
print(r.status_code)
print(r.text)
