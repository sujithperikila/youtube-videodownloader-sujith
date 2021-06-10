from pytube import YouTube
import re
import time
import os
file_size=0

def progress_Check(stream = None, chunk = None, file_handle = None, remaining = None):
    #Gets the percentage of the file that has been downloaded.
    percent = (100*(file_size-remaining))/file_size
    print("{:00.0f}% downloaded".format(percent))

link='https://www.youtube.com/watch?v=Lk2oDvoonUc&t=1s'
yt = YouTube(link)

o_mp4files = yt.streams.filter(file_extension = 'mp4').order_by('resolution')[::-1]
mp4files = [i for i in o_mp4files if 'avc1' not in str(i)]
mp4files_avc1 = [i for i in o_mp4files if 'avc1' in str(i)]
audiofiles = yt.streams.filter(only_audio=True).order_by('abr')[::-1]
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
print("Available Video Resolutions: ")
print(resolution)
print('Available Audio Bit Rates: ')
print(audios)
res_pref = input("Select the Video Resolution You Want to Download : ")
aud_pref = input("Select the Audio Bitrate You Want to Download : ")
for i in mp4files:
    if res_pref in str(i):
        s_video = i
        break
for i in audiofiles:
    if aud_pref in str(i):
        s_audio = i
        break
print("Selected Streams are : ")
print(s_video)
print(s_audio)
print("Downloading Streams: ")
vts = time.time()
s_video.download()
#os.rename(s_video,'only_video')
vte = time.time()
print("Video Download took "+str(vte-vts)+" seconds")
ats = time.time()
s_audio.download()
#os.rename(s_audio,'only_audio')
ate = time.time()
print("Audio Download took "+str(ate-ats)+" seconds")