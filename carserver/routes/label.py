from flask import json, request
from flask.json import jsonify
from carserver import app, client
from carserver.utils.updateData import update_data

@app.route('/label/update', methods=['POST'])
def rapid_acc():
    '''
        json body sample:
            "status": "OK",
            "tag_info": {
                "launch": "2021-01-28 09:59:17.28",
                "username": "chendy",
                "uuid": "C2C6DE91-427B-4DD0-A09B-F3F218FD596D"
            },
            "time": "Some UTC time",
            "updated_fields": {
                "rapid-acc": 1
            }
    '''
    print('signal received for updating label(s)')
    try:
        data = json.loads(request.get_data(as_text=True))
        status = data.get("status", "")
        tag_info = data.get("tag_info", "")
        time = data.get("time", "")
        updated_fields = data.get("updated_fields", "")

        if "" in [status, tag_info, time, updated_fields]:
            print("json body from `update label` has empty value for at least one required field")
            raise Exception

        rapid_acc = updated_fields.get("rapid-acc", "")
        rapid_brake = updated_fields.get("rapid-brake", "")
        normal = updated_fields.get("normal", "")
        bad_point = updated_fields.get("bad-point", "")
        if rapid_acc == "" and rapid_brake == "" \
            and normal == "" and bad_point == "":
                print("did not detect any required field: rapid-acc, rapid-brake, normal or bad-point")
                raise Exception

        try:
            # positioning each column requires complete tag info and time info
            update_data(client, "data", tag_info, time, updated_fields, keep=True)
            print(f'fields {updated_fields} labeled for tag = {tag_info} '
                  f'& time = {time}'
            )

        except Exception as e:
            print('error occured within update_data: ')
            print(e)
            raise Exception from e

        return jsonify({
            "message": "received"
        }), 200

    except Exception as e:
        print(e)
        print('error occured for update label(s)')

        return jsonify({
            "message": "error"
        }), 400
