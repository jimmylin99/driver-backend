from influxdb import InfluxDBClient


def get_track_longitude_latitude(client, ith_recent):
    """
    @return: 
        str: status code, 
        list: longitude_list,
        list: latitude_list,
        list: time_list,
        dict: unique_tag_info
    """
    # get launch tag keys
    results = client.query("SHOW tag values from data with key=launch")
    # print(results.raw)

    # sort launch tag keys
    try:
        lists = results.raw.get('series', '')[0].get('values', '')
        values = [list[1] for list in lists]
        values.sort(reverse=True)
    except:
        return 'unknown error', None, None

    # check if ith-recent is valid
    try:
        launch_tag = values[ith_recent]
    except IndexError:
        return 'index error', None, None

    # get all fields and tags satisfying given launch tag
    query_statement = f"select * from data where launch='{launch_tag}' group by launch"
    print(query_statement, end='\n\n')
    results = client.query(query_statement)
    gen = results.get_points()
    list = []
    longitude_list = [] # E'121
    latitude_list = [] # N'30
    time_list = []
    for kv in gen:
        _longitude = kv.get('longitude', '')
        _latitude = kv.get('latitude', '')
        _time = kv.get('time', '')
        if '' in [_longitude, _latitude, _time]:
            return 'one or more of the points lack(s) longitude or latitude or time data', None, None
        if 0 in [_longitude, _latitude]:
            continue
        list.append(kv)
        longitude_list.append(_longitude)
        latitude_list.append(_latitude)
        time_list.append(_time)

    unique_tag_info = {
        "tag1": "value1"
    } # TODO: get unique tag info
    
    return 'OK', longitude_list, latitude_list, time_list, unique_tag_info

if __name__ == '__main__':
    database_name = 'DriveS'
    client = InfluxDBClient('localhost', 8086, 'root', 'root', database_name)
    ith_recent = 0
    status, longitude_list, latitude_list = get_track_longitude_latitude(
        client, ith_recent
    )
    if status == 'OK':
        print(longitude_list, latitude_list)
    else:
        print(status)
