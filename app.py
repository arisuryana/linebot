from flask import Flask, request, jsonify
import os
import json
import dialogflow_v2

app = Flask(__name__)
PORT = int(os.environ.get("PORT", 5000))

# def results():
#     req = request.get_json()
#     intentName = req.get('intent').get('displayName')
#     action = req.get('queryResult').get('queryText')
#     # coba = req.get('originalDetectIntentRequest').get('payload').get('https://api.line.me/v2/profile')
#
#     return {'fulfillmentText': action}


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    intent_name = data.get("queryResult").get("intent").get("displayName")
    print(data)
    return jsonify(request.get_json())


if __name__ == '__main__':
    app.run(port=PORT, host='0.0.0.0')
