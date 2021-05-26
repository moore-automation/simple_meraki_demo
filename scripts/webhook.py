from flask import Flask, request, jsonify
from ciscosparkapi import CiscoSparkAPI, SparkApiError
import json
import os
#import slack

#bearer_token = os.environ.get("bearer_token")
#room_id = os.environ.get("room_id")
bearer_token = "ZWE0MGU1NmItZjdmMS00OWU4LWJmZjQtZDIwYTQyNTA3NGIyZDc3Mjc0ZjktNWE5_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f"
room_id = "Y2lzY29zcGFyazovL3VzL1JPT00vMTM2MWIyNDAtYjdiNy0xMWViLTlhZmUtOTExZDFhYmUwZDZh"


if bearer_token is None or room_id is None:
    print("\nWebex Teams Authorization and roomId must be set via environment variables using below commands or statically within the script")
    print("export bearer_token=<authorization bearer token>")
    print("export room_id=<webex teams room-id>")
    exit()

app = Flask(__name__)


@app.route('/', methods=['POST'])
def alarms():
    try:
        data = json.loads(request.data)
        print(data)
        message = '''Team, alarm event : **''' + data['eventname'] + '** ------ **' + data['message'] + \
            '''** is recieved from Meraki Dashboard and here are the complete details <br><br>''' + \
            str(data)
        api = CiscoSparkAPI(access_token=bearer_token)
        res = api.messages.create(roomId=room_id, markdown=message)
        print(res)
    except Exception as exc:
        return jsonify(str(exc)), 500

    return jsonify("Message sent to Webex Teams"), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
