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

records_num = 20
# url = 'http://server.acemap.cn:24050'
url = 'http://localhost'


def short_data(longitude=120, latitude=30):
    return datetime.utcnow().isoformat("T") + "Z" + \
             f',1.0,1.0,0.1,{latitude},{longitude},\n'


long_data = ''
for i in range(records_num):
    long_data += short_data(120+0.01*i, 30+0.01*i)

json_body = {
    "UserID": 1,
    "LaunchTimestamp": datetime.utcnow().isoformat(" "),
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
