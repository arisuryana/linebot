from flask import Flask, request, jsonify
import os
import pymysql.cursors
import json
import dialogflow_v2

app = Flask(__name__)
PORT = int(os.environ.get("PORT", 5000))

connection = pymysql.connect(host='db4free.net',
                             user='arisuryana',
                             password='arisuryana',
                             db='db_simak',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    intent_name = data.get("queryResult").get("intent").get("displayName")
    print(data)

    if intent_name == 'Awal':
        return Awal(data)

    return jsonify(request.get_json())


def Awal(data):
    cekUserID = data.get("originalDetectIntentRequest").get("payload").get("data").get("source").get("userId")

    try:
        result = None
        with connection.cursor() as cursor:
            sql = "SELECT * FROM tb_profile WHERE tb_profile.userID = %s"
            cursor.execute(sql, (cekUserID))
            result = cursor.fetchone()

        response = {
            'fulfillmentMessages': [
                {
                    "card": {
                        "title": "Menu",
                        "subtitle": "Halo {}, Silahkan pilih menu di bawah".format(result['nama']),
                        "buttons": [
                            {
                                "text": "Cek Profil",
                                "postback": "cek profil"
                            },
                            {
                                "text": "Info Akademik",
                                "postback": "info akademik"
                            }
                        ]
                    }
                }
            ]
        }

        return jsonify(response)
    except Exception:
        response = {
            'fulfillmentText': "Akun anda belum terkait dengan Sistem Simak, mohon input nim Anda"
        }

        return jsonify(response)


if __name__ == '__main__':
    app.run(port=PORT, host='0.0.0.0')
