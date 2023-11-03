from flask import Flask, render_template, request, send_file
from pytube import YouTube
import ssl
from io import BytesIO

app = Flask(__name__, template_folder="/Users/langmaneryougududeshen/PycharmProjects/YouTubeDownload/templates")

# 导入SSL证书
ssl._create_default_https_context = ssl._create_unverified_context

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    youtube_url = request.form.get('youtube_url')

    try:
        # 创建YouTube对象
        yt = YouTube(youtube_url)

        # 获取所有的视频流，并按分辨率排序（从高到低）
        video_streams = yt.streams.filter(file_extension='mp4', progressive=True).order_by('resolution').desc().all()

        # 选择分辨率最高的视频流
        highest_resolution_stream = video_streams[0]

        # 下载视频到 BytesIO 对象
        buffer = BytesIO()
        highest_resolution_stream.stream_to_buffer(buffer)

        # 返回文件内容
        buffer.seek(0)  # 重置缓冲区位置到开头
        return send_file(buffer, as_attachment=True, download_name=f"{yt.title}.mp4")

    except Exception as e:
        return f"发生错误: {e}"

if __name__ == '__main__':
    app.run(debug=True)
