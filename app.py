from flask import Flask, render_template, request, url_for, redirect, send_file, session
from pytube import YouTube
import os
from Downloader import *
from PIL import Image


app = Flask(__name__)
app.config['SECRET_KEY'] = 'sujith'

@app.route('/',methods = ['GET','POST'])
def index():
    if request.method=="POST":
        session['link'] = request.form.get('url')
        v_obj = Downloader(session['link'])
        url = v_obj.yt
        thumb = url.thumbnail_url
        streams, mp4files, audiofiles = v_obj.get_resolutions()
        return render_template('video_view.html', mp4files = mp4files, title = url.title, thumb=thumb)
    return render_template('index.html')

@app.route('/video_view',methods = ['GET','POST'])
def video_view():
    if request.method=="POST":
        v_obj = Downloader(session['link'])
        streams, mp4files, audiofiles = v_obj.get_resolutions()
        itag = request.form.get('res')
        print(itag)
        for i in mp4files:
            if int(itag) == i.itag:
                s_video = i
                break
        title = s_video.default_filename
        s_audio = audiofiles[0]
        s_video.download(filename='video')
        s_audio.download(filename='audio')
        os.rename('audio.webm','audio.mp3')
        v_obj.mux()
        os.remove('video.mp4')
        os.remove('audio.mp3')
        os.rename('output.mp4',title)
        #return send_file(title,as_attachment=True)
    return redirect(url_for('index'))


    

if __name__=="__main__":
    app.debug=True
    app.run()