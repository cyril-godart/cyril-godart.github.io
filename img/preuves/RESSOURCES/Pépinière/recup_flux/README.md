# Vivotek Video Aggregator (Flask)

Ce projet affiche les flux vidéo de deux caméras IP Vivotek via une interface web Flask.

## Prérequis

- Les flux RTSP des caméras doivent être convertis en HLS (par exemple avec ffmpeg ou rtsp-simple-server).
- Python 3.10+ et Flask.

## Lancement local

```bash
pip install flask
python app.py
```

Accédez à [http://localhost:5000](http://localhost:5000)

## Lancement avec Docker

```bash
docker build -t vivotek-flask .
docker run -p 5000:5000 vivotek-flask
```

## Proxy RTSP/HLS

Utilisez un proxy comme [rtsp-simple-server](https://github.com/aler9/rtsp-simple-server) ou ffmpeg pour exposer les flux HLS sur `/streams/IP8166/index.m3u8` et `/streams/FE8391V/index.m3u8`.

Exemple de configuration pour rtsp-simple-server :

```
paths:
  IP8166:
    source: rtsp://user:pass@192.168.1.100:554/live.sdp
  FE8391V:
    source: rtsp://user:pass@192.168.1.101:554/live.sdp
```

## Personnalisation

Modifiez la liste des caméras dans `app.py` si besoin.
