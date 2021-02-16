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

url = 'http://localhost:5000'


def add_points(pointList: list):
    long_data = ''
    def short_data(longitude=120, latitude=30):
        return datetime.utcnow().isoformat("T") + "Z" + \
                f',1.0,1.0,0.1,{latitude},{longitude},\n'

    for pair in pointList:
        long_data += short_data(pair[0], pair[1])

    json_body = {
        "UserID": 1,
        "LaunchTimestamp": datetime.utcnow().isoformat(" "),
        "Data": long_data
    }

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


pointList = [
    [121.40372811691469, 31.014449868194994],
    # [121.4083607289058, 31.01249866290206],
]
pointList.append([pointList[0][0] + 1e-12, pointList[0][1] + 1e-12])
add_points(pointList)
