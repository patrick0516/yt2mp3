import os
from flask import Flask, render_template, request, jsonify, send_file
import yt_dlp
import uuid
from threading import Thread

app = Flask(__name__)
DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
downloads = {}

def download_progress_hook(d):
    download_id = d.get('download_id')
    if not download_id or download_id not in downloads:
        return
    if d['status'] == 'downloading':
        downloads[download_id]['progress'] = d.get('_percent_str', '0.0%')
        downloads[download_id]['status'] = 'downloading'
        downloads[download_id]['detail'] = '正在下載...'
    elif d['status'] == 'finished':
        downloads[download_id]['progress'] = '100%'
        downloads[download_id]['status'] = 'converting'
        downloads[download_id]['detail'] = '正在轉換為 MP3...'
        if 'filename' in d and d['filename']:
            mp3_filename = os.path.splitext(d['filename'])[0] + '.mp3'
            downloads[download_id]['filename'] = os.path.basename(mp3_filename)
    elif d['status'] == 'error':
        downloads[download_id]['status'] = 'error'
        downloads[download_id]['detail'] = '下載失敗'
        downloads[download_id]['error'] = str(d.get('error', '未知錯誤'))

def download_video(url, quality, download_id):
    def progress_hook(d):
        d['download_id'] = download_id
        download_progress_hook(d)
    downloads[download_id] = {
        'progress': '0.0%',
        'status': 'downloading',
        'error': None,
        'filename': None
    }
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': quality,
        }],
        'progress_hooks': [progress_hook],
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        mp3_filename = os.path.splitext(filename)[0] + '.mp3'
        downloads[download_id]['filename'] = os.path.basename(mp3_filename)
        downloads[download_id]['progress'] = '100%'
        downloads[download_id]['status'] = 'completed'
        downloads[download_id]['detail'] = '下載與轉換完成！'
        downloads[download_id]['title'] = info.get('title', '')
        downloads[download_id]['filesize'] = info.get('filesize_approx', 0) or info.get('filesize', 0) or 0
        downloads[download_id]['ext'] = info.get('ext', 'mp3')
        downloads[download_id]['quality'] = quality
        # 自動清理 downloads 資料夾，只保留最新 10 個檔案
        files = [os.path.join(DOWNLOAD_FOLDER, f) for f in os.listdir(DOWNLOAD_FOLDER) if os.path.isfile(os.path.join(DOWNLOAD_FOLDER, f))]
        files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        for f in files[10:]:
            try:
                os.remove(f)
            except Exception:
                pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    quality = request.form.get('quality', '192')
    if not url:
        return jsonify({'error': '請提供 YouTube 網址'}), 400
    download_id = str(uuid.uuid4())
    thread = Thread(target=download_video, args=(url, quality, download_id))
    thread.daemon = True
    thread.start()
    return jsonify({'download_id': download_id})

@app.route('/progress/<download_id>')
def progress(download_id):
    if download_id not in downloads:
        return jsonify({'error': '找不到下載任務'}), 404
    return jsonify(downloads[download_id])

@app.route('/get_file/<filename>')
def get_file(filename):
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        return '找不到檔案', 404
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True) 