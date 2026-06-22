from flask import Flask, render_template
import requests

app = Flask(__name__)

def get_token():
    url_login = "http://10.0.0.11:8080/api/internal/login"
    login_payload = {
        "email": "pepiniere@pepiniere",
        "password": "pepiniere"
    }
    response = requests.post(url_login, json=login_payload)
    if response.status_code == 200:
        return response.json()["jwt"]
    return None

def get_devices(token):
    headers = {
        "Grpc-Metadata-Authorization": f"Bearer {token}"
    }
    url_devices = "http://10.0.0.11:8080/api/devices?limit=10"
    response = requests.get(url_devices, headers=headers)
    return response.json().get("result", [])

def get_last_data(dev_eui, token):
    headers = {
        "Grpc-Metadata-Authorization": f"Bearer {token}"
    }
    url_data = f"http://10.0.0.11:8080/api/devices/{dev_eui}/frames?limit=1"
    response = requests.get(url_data, headers=headers)
    frames = response.json().get("result", [])
    if frames:
        frm_payload = frames[0].get("frmPayload")
        payload_bytes = bytes.fromhex(frm_payload)
        temp_raw = int.from_bytes(payload_bytes[0:2], byteorder='big')
        hum_raw = int.from_bytes(payload_bytes[2:4], byteorder='big')
        return temp_raw / 100, hum_raw / 10
    return None, None

@app.route('/')
def index():
    token = get_token()
    if not token:
        return "Erreur de connexion à l'API"
    devices = get_devices(token)
    if not devices:
        return "Aucun capteur trouvé"
    dev_eui = devices[0]["devEui"]
    temperature, humidity = get_last_data(dev_eui, token)
    return render_template('index.html', temperature=temperature, humidity=humidity)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
