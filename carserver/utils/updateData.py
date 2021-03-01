'''
    Update point (data) given its unique identifiers: tag & time,
    as well as its updated fields.
    By default (keep=True), all old fields will be kept, and new fields
    mentioned in argument `fields` will overlay them if any;
    if keep is set to false, then no old field will be kept, and the fields
    for this new point will be exactly the same as those provide in argument
    `fields`.

    @params: client -> InfluxDBClient
    @params: measurement -> string
    @params: tag_info -> dict
    @params: time -> string
    @params: fields -> dict
    @params: keep -> boolean

'''
from influxdb.client import InfluxDBClient


def update_data(client: InfluxDBClient, measurement: str, tag_info: dict, 
        time: str, fields: dict, keep=True):
    if keep == False:
        raise NotImplementedError

    sql_query = (
        f"SELECT *::field FROM {measurement} "
        f"WHERE time='{time}' "
    )
    for key, value in tag_info.items():
        sql_query = sql_query + f" and {key}='{value}'"
    
    print(f"sql_query = {sql_query}")

    results = client.query(sql_query)
    print(f"results: {results}")
    points = results.get_points()
    print(f"points: {points}")
    size = 0
    for _point in points:
        size += 1
        if size == 1:
            point = _point
    if size == 0:
        print("sql query returns empty result set")
        raise Exception
    print(f"point = {point}")

    ''' update point
        point sample:
        point = {
            'time': '2021-01-23T15:58:30.750000Z', 
            'acceleration': 0.005427043900637734, 
            'gyroscope': 0.009184479105195894, 
            'latitude': 31.143920631980222, 
            'longitude': 121.36646195555223, 
            'velocity': 0.0
        }
    '''
    
    updated_point = {
        "measurement": measurement,
        "time": time,
        "tags": tag_info,
    }
    updated_fields = {}

    # update fields for old point
    for key, value in point.items():
        if key == 'time':
            continue
        if key in fields.keys():
            updated_fields[key] = fields[key]
        else:
            updated_fields[key] = value
    # add fields who does not exist in old point
    for key, value in fields.items():
        if key not in point.keys():
            updated_fields[key] = value

    updated_point["fields"] = updated_fields
    body = [
        updated_point
    ]
    print(body)

    client.write_points(body)


if __name__ == "__main__":
    import sys
    sys.path.append('../..')
    from carserver import client
    tag_info = {
                "launch": "2021-01-23 15:30:17.44",
                "username": "chendy",
                "uuid": "EF2C2D30-66BF-4BD8-974D-CB42929DA610"
    }
    time = "2021-01-23T15:58:30.75Z"
    updated_fields = {
        "rapid-acc": 0,
        "rapid-brake": 1
    }
    
    update_data(client, "data", tag_info, time, updated_fields, keep=True)
