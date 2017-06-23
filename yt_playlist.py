#!/usr/bin/env python3

import re
import sys
import time
import os
import requests
from pytube import YouTube

class progressBar:
    def __init__(self, barlength=25):
        self.barlength = barlength
        self.position = 0
        self.longest = 0

    def print_progress(self, cur, total, start):
        currentper = (cur / total)
        curbar = int(currentper * self.barlength)
        size = bytestostr(total)
        bar = '\r Size : '+size+'  ['
        for i in range(curbar) :
            bar = bar + '#'
        for i in range(self.barlength-curbar) :
            bar = bar + '.'
        bar = bar + '] '
        bar +=  str(int(currentper*100)) + ' % '
        if len(bar) > self.longest :
            self.longest = len(bar)
        for i in range(self.longest-len(bar)):
            bar = bar + ' '
        sys.stdout.write(bar)

    def print_end(self, *args):  # Clears Progress Bar
        sys.stdout.write('\r{0}\r'.format((' ' for _ in range(self.longest))))

def bytestostr(bts):
    bts = float(bts)
    if bts >= 1024 ** 4:    # Converts to Terabytes
        terabytes = bts / 1024 ** 4
        size = '%.2fTb' % terabytes
    elif bts >= 1024 ** 3:  # Converts to Gigabytes
        gigabytes = bts / 1024 ** 3
        size = '%.2fGb' % gigabytes
    elif bts >= 1024 ** 2:  # Converts to Megabytes
        megabytes = bts / 1024 ** 2
        size = '%.2fMb' % megabytes
    elif bts >= 1024:       # Converts to Kilobytes
        kilobytes = bts / 1024
        size = '%.2fKb' % kilobytes
    else:                   # No Conversion
        size = '%.2fb' % bts
    return size


def getPageSource(url):
    try:
        pageContent = requests.get(url)
        return pageContent.text
    except requests.exceptions.RequestException as e:
        print(e)
        exit(1)
        

def getPlaylistID(url):
    if 'list=' in url:
        indx = url.index('=') + 1
        iD = url[indx:]
        if '&' in url:
            amp = url.index('&')
            iD = url[indx:amp]
        return iD   
    else:
        print(url, "is not a youtube playlist.")
        exit(1)

def getFinalVideoUrl(vid_urls):
    final_url_list = []
    for vid_url in vid_urls:
        url_amp = len(vid_url)
        if '&' in vid_url:
            url_amp = vid_url.index('&')
        final_url_list.append('http://www.youtube.com/' + vid_url[:url_amp])
    return final_url_list

def getPlaylistVideoUrls(page_content, url):
    playlist_id = getPlaylistID(url)

    vid_url_pattern = re.compile(r'watch\?v=\S+?list=' + playlist_id)
    vid_url_matches = re.findall(vid_url_pattern , page_content)
    if vid_url_matches:
        final_vid_urls = getFinalVideoUrl(vid_url_matches)
        # set is used in order to avoid repeated elements in the list .
        final_vid_urls = list(set(final_vid_urls))
        print("\nFound",len(final_vid_urls),"videos in playlist.")
        printUrls(final_vid_urls)
        return final_vid_urls
    else:
        print('No videos found.')
        exit(1)

#function added to get audio files along with the video files from the playlist

def download_Video_Audio(path, vid_url, file_no):
    try:
        yt = YouTube(vid_url)
    except Exception as e:
        print("Error:", str(e), "- Skipping Video with url '"+vid_url+"'.")
        return
    # selecting the video with mp4 format and highest resolution .
    video = sorted(yt.filter("mp4"), key=lambda temp: int(temp.resolution[:-1]))[-1]
    print('downloading "', yt.filename+'" video in '+video.resolution)
    try:
        bar = progressBar()
        video.download(path, on_progress=bar.print_progress, on_finish=bar.print_end)
        print("successfully downloaded", yt.filename, "!")
    except OSError:
        print(yt.filename, "already exists in this directory! Skipping video...")

    try:
        current_mp4 = path + '/' + yt.filename + '.mp4'
        final_mp4 = path + '/' + str(file_no) + '.mp4'
        final_wav = path + '/' + str(file_no) + '.wav'
        os.makedirs(path+'/audio',exist_ok=True) 
        final_mp3 = path + '/audio/' + str(file_no) + '.mp3'
        os.rename(current_mp4,final_mp4)
        aud= 'ffmpeg -i '+final_mp4+' '+final_wav
        final_audio='lame '+final_wav+' '+final_mp3
        os.system(aud)
        os.system(final_audio)
        os.remove(final_wav)
        print("sucessfully converted",yt.filename, "into audio!\n")
        print('######################################################################################################################################\n')
    except Exception as e:
        print(e)
        print(yt.filename, "There is some problem with the file names...")
 

def printUrls(vid_urls):
    for url in vid_urls:
        print(url)
        time.sleep(0.04)
    print('')
        
if __name__ == '__main__':

    # when command line arguments are not according to our need .
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print('USAGE: python yt_playlist.py <playlistURL> OR python yt_playlist.py <playlistURL> <destPath>')
        exit(1)

    else:
        url = sys.argv[1]

        if len(sys.argv) != 3 :
            directory = os.getcwd()  
        else :
            directory = sys.argv[2] 
    
        # make directory if dir specified doesn't exist
        try:
            os.makedirs(directory, exist_ok=True) 
        except OSError as e:
            print(e.reason)
            exit(1)

        if not url.startswith("http"):
            url = 'https://' + url

        # get html code for the playlist page . 
        playlist_page_content = getPageSource(url)

        # Extract all the video url from the source code .
        vid_urls_in_playlist = getPlaylistVideoUrls(playlist_page_content, url)

        # downloads videos and audios
        for i,vid_url in enumerate(vid_urls_in_playlist):
            download_Video_Audio(directory, vid_url, i)
time.sleep(1)