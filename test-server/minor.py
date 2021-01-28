from influxdb import InfluxDBClient


def get_track_longitude_latitude(client, ith_recent):
    """
    @return: 
        str: status code, 
        list: longitude_list,
        list: latitude_list
    """
    results = client.query("SHOW tag values from data with key=launch")
    # print(results.raw)
    try:
        lists = results.raw.get('series', '')[0].get('values', '')
        values = [list[1] for list in lists]
        values.sort(reverse=True)
    except:
        return 'unknown error', None, None

    try:
        launch_tag = values[ith_recent]
    except IndexError:
        return 'error', None, None
    query_statement = f"select * from data where launch='{launch_tag}' group by launch"
    print(query_statement, end='\n\n')
    results = client.query(query_statement)
    gen = results.get_points()
    list = []
    longitude_list = [] # E'121
    latitude_list = [] # N'30
    for kv in gen:
        _longitude = kv.get('longitude', '')
        _latitude = kv.get('latitude', '')
        if _longitude == '' or _latitude == '':
            return 'one or more of the points lack(s) longitude or latitude data', None, None
        if _longitude == 0 or _latitude == 0:
            continue
        list.append(kv)
        longitude_list.append(_longitude)
        latitude_list.append(_latitude)
    
    return 'OK', longitude_list, latitude_list

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
