from pytube import YouTube
import ffmpeg
import re
import time
import os
import subprocess
from subprocess import run

class Downloader():
    def __init__(self,link):
        self.link = link
        self.yt = YouTube(self.link)
        self.title = self.yt.title

    def get_resolutions(self):
        all_streams = self.yt.streams.filter().order_by('resolution')[::-1]
        o_mp4files = self.yt.streams.filter(file_extension = 'mp4').order_by('resolution')[::-1]
        mp4files = [i for i in o_mp4files if 'avc1' not in str(i)]
        mp4files_avc1 = [i for i in o_mp4files if 'avc1' in str(i)]
        audiofiles = self.yt.streams.filter(only_audio=True).order_by('abr')[::-1]
        resolution=[]
        audios=[]
        for i in mp4files:
            if re.search(r"res=\"(\d{3,4}p)\"",str(i)):
                res = re.findall(r"res=\"(\d{3,4}p)\"",str(i))[0]
                resolution.append(res)
        for i in audiofiles:
            if re.search(r"abr=\"(\d{2,4}kbps)\"",str(i)):
                res = re.findall(r"abr=\"(\d{2,4}kbps)\"",str(i))[0]
                audios.append(res)
        return resolution, mp4files, audiofiles

    def get_by_tag(self,tag,mp4files):
        video = mp4files.get_by_itag(tag)
        return video

    def run(self):
        resolution , mp4files, audiofiles= self.get_resolutions()
        print(type(mp4files[0]))
        print("Available Video Resolutions:")
        print(resolution)
        v_found = False
        a_found = False

        res_pref = input("Select the Video Resolution You Want to Download : ")

        for i in mp4files:
            if res_pref in str(i):
                s_video = i
                v_found = True
                break

        if v_found:
            print("Selected Video Stream is : ")
            print(s_video)
        else:
            print("Selected Video Stream is Not Available\n")
    
        s_audio = audiofiles[0]
        if s_audio:
            a_found = True

        if not v_found or not a_found:
            return 'Failed Download Attempt'

        print("Downloading Streams: ")
        vts = time.time()
        s_video.download(filename='video')
        #os.rename(s_video,'only_video')
        vte = time.time()
        print("Video Download took "+str(vte-vts)+" seconds\n")
        ats = time.time()
        s_audio.download(filename='audio')
        #os.rename(s_audio,'only_audio')
        ate = time.time()
        print("Audio Download took "+str(ate-ats)+" seconds\n")
        return self.title, 'Downloaded Sucessfully !'

    def mux(self):
        cmd = 'ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 output.mp4 -loglevel quiet'
        subprocess.call(cmd, shell=True)
    
    def mix(self,path,op):
        cmd = 'ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 output.mp4 -loglevel quiet'
        subprocess.call(cmd, shell=True) 


        # video_stream = ffmpeg.input('video.mp4')
        # audio_stream = ffmpeg.input('audio.mp3')
        # ffmpeg.concat(video_stream, audio_stream, v=1, a=1).output('finished_video.mp4').run()


if __name__=="__main__":
    #link = input('Enter URL of Youtube Video you want to Download : ')
    # https://www.youtube.com/watch?v=Lk2oDvoonUc
    try:
        path = 'C:/Users/perikila/Desktop/Youtube Downloader Python Project By Sujith'
        link=input("Enter the Url of the Youtube Video : ")
        d=Downloader(link)
        title, msg = d.run()
        os.rename('audio.webm','audio.mp3')
        op = path+str(title)+'.mp4'
        d.mix(path,op)
        os.remove('video.mp4')
        os.remove('audio.mp3')
        os.rename('output.mp4',str(title)+'.mp4')
        print(msg)
    except Exception as e:
        print(str(e))
