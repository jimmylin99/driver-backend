from flask import render_template, make_response
import json

from flask.json import jsonify

from carserver import app, client

@app.route('/replay')
def replay():
    return render_template('index.html')


@app.route('/algo-test')
def algo_test():
    return render_template('algo_test.html')


@app.route('/points/<string:username>/<int:trackid>', methods=['GET'])
def data_post(username, trackid):
    from carserver.utils.getlnglat import get_track_longitude_latitude
    from carserver.utils.transCoordinate import LngLatTransfer
    transCoord = LngLatTransfer()
    status, longitude_list, latitude_list, \
        acc_list, gyr_list, speed_list, \
        time_list, unique_tag_info = get_track_longitude_latitude(
            client, username, trackid
    )
    from carserver.algo.detectionWrapper import getFastTurnIndicator
    algoIsFastTurn = getFastTurnIndicator(acc_list, gyr_list, speed_list)
    # algoIsFastTurn = [0] * len(acc_list)
    # for i in range(len(acc_list)//3, len(acc_list)//3*2):
    #     algoIsFastTurn[i] = 1
    points = []
    # package lng & lat into an array `points`
    # also package fastTurn indicator
    if status == 'OK':
        if len(longitude_list) == len(latitude_list) and \
            len(time_list) == len(longitude_list) and \
            len(longitude_list) > 0:
                for i in range(len(longitude_list)):
                    lng = longitude_list[i]
                    lat = latitude_list[i]
                    lat, lng = transCoord.WGS84_to_GCJ02(lng, lat)
                    points.append([lng, lat])
                    
                
                return make_response(
                    jsonify({
                        'points': points,
                        'time': time_list,
                        'tag-info': unique_tag_info,
                        'algo': {
                            'fast-turn': algoIsFastTurn
                        }
                    }),
                    200
                )
        else:
            print('one of the length of longitude, latitude and time '
                  'is not identical')
            return make_response('one of the length of longitude, latitude and time '
                  'is not identical', 400)
    else:
        print(status)
        return make_response({'message': status}, 400)
    
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
