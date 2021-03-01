from flask import json, request
from flask.json import jsonify
from carserver import app, client
from carserver.utils.updateData import update_data

@app.route('/label/rapid-acc', methods=['POST'])
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
    print('rapid-acc received')
    try:
        data = json.loads(request.get_data(as_text=True))
        status = data.get("status", "")
        tag_info = data.get("tag_info", "")
        time = data.get("time", "")
        updated_fields = data.get("updated_fields", "")

        if "" in [status, tag_info, time, updated_fields]:
            print("json body from rapid-acc has empty value for at least one required field")
            raise Exception

        rapid_acc = updated_fields.get("rapid-acc", "")
        if "" == rapid_acc:
            print("did not detect field: rapid-acc within updated fields")
            raise Exception

        try:
            # positioning each column requires complete tag info and time info
            update_data(client, "data", tag_info, time, updated_fields, keep=True)

        except Exception as E:
            print('error occured within update_data')
            raise Exception from E

        return jsonify({
            "message": "received"
        }), 200

    except:
        print('rapid-acc error occured')

        return jsonify({
            "message": "error"
        }), 400
