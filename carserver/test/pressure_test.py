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
url = 'https://datainput-safesjtu.acemap.cn'
# url = 'http://localhost:5000'


def short_data(longitude=120, latitude=30):
    return datetime.utcnow().isoformat("T") + "Z" + \
             f',1.0,1.0,0.1,{latitude},{longitude},\n'


long_data = ''
for i in range(records_num):
    long_data += short_data(121+0.01*i, 31+0.01*i)

json_body = {
    "UserID": 1,
    "LaunchTimestamp": datetime.utcnow().isoformat(" "),
    "Data": long_data
}
# register
# r = requests.post(url=url+'/register', auth=('mike3', '123'))

# login
# r = requests.post(url=url+'/login', auth=('mike3', '123'))

#upload
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Im1pa2UzIiwiZXhwIjoyNDgxNzc3Njk5fQ.badfXcWfxz-3QJd5hf3yjrwC4Sm5cCr39m9rbCzabD0"
from time import perf_counter
T1 = perf_counter()
r = requests.post(url=url+'/upload', json=json_body,
                  headers={'x-access-tokens': access_token})
T2 = perf_counter()
print(f'time elapsed: {(T2 - T1):3f} s')

#result
print(r.headers)
print(r.status_code)
print(r.text)
