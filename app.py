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
    elif intent_name == 'Awalcustom':
        return AwalCustom(data)
    elif intent_name == 'cekProfil':
        return cekProfil(data)
    elif intent_name == 'infoAkademik':
        return infoAkademik(data)
    elif intent_name == 'ubahDataAlamat':
        return ubahDataAlamat(data)
    elif intent_name == 'ubahDataAlamatValue':
        return ubahDataAlamatValue(data)
    elif intent_name == 'cekIpk':
        return cekIpk(data)

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

        # with connection.cursor() as cursor:
        #     sql = "INSERT INTO tb_inbox (id_pesan, pesan, userID, tanggal) VALUES (%s, %s, %s, %s)"
        #     cursor.execute(sql, (id_pesan, pesan, cekUserID, date.today().strftime("%Y-%m-%d")))
        #     id_inbox = cursor.lastrowid
        #
        # connection.commit()
        #
        # with connection.cursor() as cursor:
        #     sql = "INSERT INTO tb_outbox (id_inbox, response) VALUES (%s, %s)"
        #     cursor.execute(sql, (id_inbox, "Halo {}, Silahkan pilih menu di bawah".format(result['nama'])))
        #     sql = "UPDATE tb_inbox SET tb_inbox.status = '1' WHERE tb_inbox.id_inbox = %s"
        #     cursor.execute(sql, (id_inbox))
        #
        # connection.commit()

        return jsonify(response)

    except Exception:
        # with connection.cursor() as cursor:
        #     sql = "INSERT INTO tb_inbox (id_pesan, pesan, userID, tanggal) VALUES (%s, %s, %s, %s)"
        #     cursor.execute(sql, (id_pesan, pesan, cekUserID, date.today().strftime("%Y-%m-%d")))
        #     id_inbox = cursor.lastrowid
        #
        # connection.commit()

        response = {
            'fulfillmentText': "Akun anda belum terkait dengan Sistem Simak, mohon input nim Anda"
        }

        # with connection.cursor() as cursor:
        #     sql = "INSERT INTO tb_outbox (id_inbox, response) VALUES (%s, %s)"
        #     cursor.execute(sql, (id_inbox, "Akun anda belum terkait dengan Sistem Simak, mohon input nim Anda"))
        #     sql = "UPDATE tb_inbox SET tb_inbox.status = '1' WHERE tb_inbox.id_inbox = %s"
        #     cursor.execute(sql, (id_inbox))
        #
        # connection.commit()

        return jsonify(response)

def AwalCustom(data):
    cekUserID = data.get("originalDetectIntentRequest").get("payload").get("data").get("source").get("userId")
    id_pesan = data.get("originalDetectIntentRequest").get("payload").get("data").get("message").get("id")
    pesan = data.get("originalDetectIntentRequest").get("payload").get("data").get("message").get("text")
    nim = data.get("queryResult").get("parameters").get("number")

    try:
        result = None
        with connection.cursor() as cursor:
            sql = "SELECT * FROM tb_profile WHERE tb_profile.nim = %s"
            cursor.execute(sql, (nim))
            result = cursor.fetchone()

        response = {
            'fulfillmentText': "Akun anda berhasil terintegrasi dengan Akun Simak !"
        }

        with connection.cursor() as cursor:
            sql = "UPDATE tb_profile SET tb_profile.userID = %s WHERE tb_profile.nim = %s"
            cursor.execute(sql, (cekUserID, nim))
        connection.commit()

        return jsonify(response)

    except Exception:
        response = {
            'fulfillmentText': "Mohon maaf, anda tidak memiliki Akun Simak"
        }

        return jsonify(response)

def cekProfil(data):
    cekUserID = data.get("originalDetectIntentRequest").get("payload").get("data").get("source").get("userId")
    pesan = data.get("originalDetectIntentRequest").get("payload").get("data").get("message").get("text")

    try:
        hasil = None
        with connection.cursor() as cursor:
            sql = "SELECT * FROM tb_profile WHERE tb_profile.userID = %s"
            cursor.execute(sql, (cekUserID))
            hasil = cursor.fetchone()

        response = {
            'fulfillmentText': "NIM : {}\nNama : {}\nAlamat : {}\nJurusan : {}".format(hasil['nim'], hasil['nama'], hasil['alamat'], hasil['jurusan'])
        }

        return jsonify(response)

    except Exception:
        response = {
            'fulfillmentText': "Profil anda tidak tersedia !"
        }

        return jsonify(response)

def infoAkademik(data):
    pesan = data.get("originalDetectIntentRequest").get("payload").get("data").get("message").get("text")

    response = {
        'fulfillmentMessages': [
            {
                "card": {
                    "title": "Info Akademik",
                    "buttons": [
                        {
                            "text": "Lihat KHS",
                            "postback": "lihat khs"
                        },
                        {
                            "text": "Cek IPK",
                            "postback": "cek ipk"
                        }
                    ]
                }
            }
        ]
    }

    return jsonify(response)

def ubahDataAlamat(data):
    cekUserID = data.get("originalDetectIntentRequest").get("payload").get("data").get("source").get("userId")
    pesan = data.get("originalDetectIntentRequest").get("payload").get("data").get("message").get("text")

    try:
        hasil = None
        with connection.cursor() as cursor:
            sql = "SELECT * FROM tb_profile WHERE tb_profile.userID = %s"
            cursor.execute(sql, (cekUserID))
            hasil = cursor.fetchone()

        response = {
            'fulfillmentText': "Alamat lama anda di {}, input alamat baru dengan keyword awalan alamat baru".format(hasil['alamat'])
        }

        return jsonify(response)

    except Exception:
        response = {
            'fulfillmentText': "Data alamat tida ditemukan"
        }

        return jsonify(response)

def ubahDataAlamatValue(data):
    cekUserID = data.get("originalDetectIntentRequest").get("payload").get("data").get("source").get("userId")
    pesan = data.get("originalDetectIntentRequest").get("payload").get("data").get("message").get("text")
    alamat = data.get("queryResult").get("parameters").get("address")

    try:
        with connection.cursor() as cursor:
            sql = "UPDATE tb_profile SET tb_profile.alamat = %s WHERE tb_profile.userID = %s"
            cursor.execute(sql, (alamat, cekUserID))
        connection.commit()

        response = {
            'fulfillmentText': "Alamat anda berhasil diubah, silahkan cek profil"
        }

        return jsonify(response)

    except Exception:
        response = {
            'fulfillmentText': "Data tidak berhasil diubah !"
        }

        return jsonify(response)

def cekIpk(data):
    cekUserID = data.get("originalDetectIntentRequest").get("payload").get("data").get("source").get("userId")
    pesan = data.get("originalDetectIntentRequest").get("payload").get("data").get("message").get("text")
    id_profile = ""

    try:
        with connection.cursor() as cek:
            sql = "SELECT tb_profile.id_profile WHERE tb_profile.userID = %s"
            id_profile = cek.execute(sql, (cekUserID))

        ipk = None
        with connection.cursor() as cursor:
            sql = "SELECT ROUND(SUM(tb_mk.sks*tb_nilai.angka)/SUM(tb_mk.sks),2) AS ipk FROM tb_profile,tb_periode,tb_khs,tb_detail_khs,tb_mk,tb_nilai " \
                  "WHERE tb_profile.id_profile=tb_khs.profile_id " \
                  "AND tb_periode.id_periode=tb_khs.periode_id " \
                  "AND tb_khs.id_khs=tb_detail_khs.khs_id " \
                  "AND tb_mk.id_mk=tb_detail_khs.mk_id " \
                  "AND tb_nilai.id_nilai=tb_detail_khs.nilai_id " \
                  "AND tb_profile.id_profile = %s"
            cursor.execute(sql, (id_profile))
            ipk = cursor.fetchone()

        response ={
            'fulfillmentText': "Nilai IPK : {}".format(ipk['ipk'])
        }

        return jsonify(response)

    except Exception:

        response = {
            'fulfillmentText': "Nilai IPK anda tidak ditemukan !"
        }

        return jsonify(response)

if __name__ == '__main__':
    app.run(port=PORT, host='0.0.0.0')
