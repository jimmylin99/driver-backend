from influxdb import InfluxDBClient
import traceback

def get_track_longitude_latitude(client, username, ith_recent):
    """
    IMPORTANT: tag should be unique among all returned points!
    this is the key assumption
    @return: 
        str: status code, 
        list: longitude_list,
        list: latitude_list,
        list: time_list,
        dict: unique_tag_info
    """
    # check for existence of username in tracks
    results = client.query("show tag values from data with key=username")
    lists = results.raw.get('series', '')[0].get('values', '')
    found_username = False
    for pair in lists:
        if pair[1] == username:
            found_username = True
            break
    if not found_username:
        return 'No tracks recorded for given username', None, None, None, None

    # get launch tag keys
    results = client.query("show tag values from data with key=launch")
    # print(results.raw)

    # sort launch tag keys
    try:
        lists = results.raw.get('series', '')[0].get('values', '')
        values = [list[1] for list in lists]
        values.sort(reverse=True)
    except Exception as e:
        print(e)
        traceback.print_exc()
        return 'unknown error', None, None, None, None

    # find the tags for ith-recent
    # and check if ith-recent is valid
    found_valid = False
    index_for_values = 0
    cnt = 0
    while index_for_values < len(values):
        _launch = values[index_for_values]
        query_statement = f"select * from data where launch='{_launch}' limit 1"
        results = client.query(query_statement)
        gen = results.get_points()
        for kv in gen:
            _username = kv.get('username', '')
            break

        if _username == username:
            cnt += 1
            if cnt == ith_recent + 1: 
                found_valid = True
                break

        index_for_values += 1
    
    if found_valid == False:
        if index_for_values >= len(values):
            return 'Index Out of Range for track id', None, None, None, None
        return 'Invalid', None, None, None, None
    
    launch_tag = values[index_for_values]

    # get all fields and tags satisfying given launch tag
    # MOD: no tailing `group by launch` so that launch tag is also listed in results
    # TODO: make sure this works (it should work)
    query_statement = f"select * from data where launch='{launch_tag}' group by *"
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

    # IMPORTANT: as mentioned at the beginning,
    # tag should be unique among all returned points!
    # this is the key assumption
    keys = results.keys()
    assert len(keys) > 0
    assert len(keys[0]) == 2
    unique_tag_info = keys[0][1]
    
    return 'OK', longitude_list, latitude_list, time_list, unique_tag_info

if __name__ == '__main__':
    database_name = 'DriveS'
    client = InfluxDBClient('localhost', 8086, 'root', 'root', database_name)
    status, longitude_list, latitude_list, \
        time_list, unique_tag_info = get_track_longitude_latitude(
            client, 'wangj1ngyan ', 2
    )
    if status == 'OK':
        # print(longitude_list, latitude_list)
        print('success')
        print(f'len = {len(longitude_list)}')
        print(f'tag info = {unique_tag_info}')
    else:
        print(status)
