from flask import render_template
import json

from flask.json import jsonify

from carserver import app, client

@app.route('/replay')
def replay():
    return render_template('index.html')


@app.route('/points/chendy/0_th_recent', methods=['GET'])
def data_post():
    from carserver.utils.getlnglat import get_track_longitude_latitude
    from carserver.utils.transCoordinate import LngLatTransfer
    transCoord = LngLatTransfer()
    status, longitude_list, latitude_list, \
    time_list, unique_tag_info = get_track_longitude_latitude(
        client, 0
    )
    # package lng & lat into an array `points`
    points = []
    if status == 'OK':
        if len(longitude_list) == len(latitude_list) and \
            len(time_list) == len(longitude_list) and \
            len(longitude_list) > 0:
                for i in range(len(longitude_list)):
                    lng = longitude_list[i]
                    lat = latitude_list[i]
                    lat, lng = transCoord.WGS84_to_GCJ02(lng, lat)
                    points.append([lng, lat])
        else:
            print('one of the length of longitude, latitude and time '
                  'is not identical')
    else:
        print(status)
    
    # return jsonify(  # content-type is "application/json"
    #     {'message': [
    #         {'status': status},
    #         {'lo': longitude_list},
    #         {'la': latitude_list}

    #     ]},
    #     200
    # )
    # return json.dumps({  # content-type is "text/html; charset=utf-8"
    #     'points': points
    # })
    
    return jsonify({
        'points': points,
        'time': time_list,
        'tag-info': unique_tag_info
    })
