# Youtube_Playlist_Downloader
- This script helps us to download all the videos in a youtube playlist in .mp4 format and in the highest resolution available for the video.
- This script also extract audio from these videos and save all audio files in a new folder named audio inside cwd .

### Build Requirements :
- Python 3+ and pip3 . 
- pytube module 
    ```
        $ pip3 install pytube
    ```
- ffmpeg  ( a fast tool for video to audio conversion )

    ```
        $ sudo add-apt-repository ppa:jonathonf/ffmpeg-3 
        $ sudo apt update 
        $ sudo apt install ffmpeg libav-tools x264 x265 
     ```
     
- lame  ( a tool that converts audio file to .mp3 format ) 
    ```
        $ sudo apt-get update
        $ sudo apt-get install lame
    ```
### Usage :
- Videos will be downloaded in current working directory . 

  ```
     python3 yt_playlist.py <playlistURL> 
  ```
- Videos will be downloaded in the given directory .
  ```
     python 3 yt_playlist.py <playlistURL> <destPath>
  ```
### Screenshots :
- We are downloading video from (https://www.youtube.com/playlist?list=PLxwCQIG_wMBLpxjPr_Kp5S47Aw8964p75) in the directory `~/Music/Temp`
<p align="center">
  <img src="http://i.imgur.com/08fcV2w.png"> <br>
  Fig 1 - Progress Bar in Terminal<br><br><br>
  <img src="http://i.imgur.com/LxvxOfR.png"> <br>
  Fig 2 - Downloaded Video Files<br><br><br>
  <img src="http://i.imgur.com/c5F4zWY.png"> <br>
  Fig 3 - Downloaded audio Files
</p>
