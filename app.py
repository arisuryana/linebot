from flask import Flask, request, jsonify
import os
import pymysql.cursors
from datetime import date
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
    id_pesan = data.get("originalDetectIntentRequest").get("payload").get("data").get("message").get("id")
    pesan = data.get("originalDetectIntentRequest").get("payload").get("data").get("message").get("text")
    id_inbox = ""

    try:
        result = None
        with connection.cursor() as cursor:
            sql = "SELECT * FROM tb_profile WHERE tb_profile.userID = %s"
            cursor.execute(sql, (cekUserID))
            result = cursor.fetchone()

        with connection.cursor() as cursor:
            sql = "INSERT INTO tb_inbox (id_pesan, pesan, userID, tanggal) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (id_pesan, pesan, cekUserID, date.today().strftime("%Y-%m-%d")))
            id_inbox = cursor.lastrowid

        connection.commit()

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

        with connection.cursor() as cursor:
            sql = "INSERT INTO tb_outbox (id_inbox, response) VALUES (%s, %s)"
            cursor.execute(sql, (id_inbox, "Halo {}, Silahkan pilih menu di bawah".format(result['nama'])))
            sql = "UPDATE tb_inbox SET tb_inbox.status = '1' WHERE tb_inbox.id_inbox = %s"
            cursor.execute(sql, (id_inbox))

        connection.commit()

        return jsonify(response)

    except Exception:
        with connection.cursor() as cursor:
            sql = "INSERT INTO tb_inbox (id_pesan, pesan, userID, tanggal) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (id_pesan, pesan, cekUserID, date.today().strftime("%Y-%m-%d")))
            id_inbox = cursor.lastrowid

        connection.commit()

        response = {
            'fulfillmentText': "Akun anda belum terkait dengan Sistem Simak, mohon input nim Anda"
        }

        with connection.cursor() as cursor:
            sql = "INSERT INTO tb_outbox (id_inbox, response) VALUES (%s, %s)"
            cursor.execute(sql, (id_inbox, "Akun anda belum terkait dengan Sistem Simak, mohon input nim Anda"))
            sql = "UPDATE tb_inbox SET tb_inbox.status = '1' WHERE tb_inbox.id_inbox = %s"
            cursor.execute(sql, (id_inbox))

        connection.commit()

        return jsonify(response)


if __name__ == '__main__':
    app.run(port=PORT, host='0.0.0.0')
