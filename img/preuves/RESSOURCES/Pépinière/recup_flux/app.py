from flask import Flask, render_template

app = Flask(__name__)

CAMERAS = [
    {
        "id": "IP8166",
        "name": "Vivotek IP8166",
        "hls_url": "/streams/IP8166/index.m3u8"
    },
    {
        "id": "FE8391V",
        "name": "Vivotek FE8391V",
        "hls_url": "/streams/FE8391V/index.m3u8"
    }
]

@app.route("/")
def index():
    return render_template("index.html", cameras=CAMERAS)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
