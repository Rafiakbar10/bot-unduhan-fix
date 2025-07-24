from flask import Flask, request
import requests
import yt_dlp
import os

app = Flask(__name__)

TOKEN = '8378572934:AAEmSHtsH_fk-AUm78vANNbjszp1X4kR9d0'
URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

@app.route('/api', methods=['POST'])
def webhook():
    data = request.get_json()

    if 'message' in data and 'text' in data['message']:
        chat_id = data['message']['chat']['id']
        text = data['message']['text']

        if text.startswith('http'):
            try:
                ydl_opts = {
                    'format': 'best',
                    'outtmpl': 'downloaded.%(ext)s',
                    'noplaylist': True,
                    'quiet': True
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(text, download=True)
                    file_name = ydl.prepare_filename(info)

                with open(file_name, 'rb') as f:
                    files = {'video': f}
                    requests.post(f'https://api.telegram.org/bot{TOKEN}/sendVideo', data={'chat_id': chat_id}, files=files)

                os.remove(file_name)
            except Exception as e:
                requests.post(URL, data={'chat_id': chat_id, 'text': f"❌ Gagal: {str(e)}"})
        else:
            requests.post(URL, data={'chat_id': chat_id, 'text': 'Kirim link video TikTok/YouTube/IG untuk mengunduh'})

    return 'ok'