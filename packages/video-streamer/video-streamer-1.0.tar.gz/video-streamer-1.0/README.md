# Video Streamer
Video streamer is a client-server application for streaming videos. It uses rtsp with gstreamer and libvlc for video processing and playing. It is written in Python3 using PySide2 Qt5 bindings.

## Applications
### Video Streamer
This application is a video client playing videos from remote server. It works on Windows, Linux and MacOS. It supports listing available videos through directory explorer and playing those videos.
#### System Dependencies
**libvlc** - for playing video
### Video Streamer Server
This application is a server for video streaming. It is a linux-only console application capable of handling multiple clients.
#### System Dependencies
**dbus** - for internal communication (used on most Linux distributions by default)
**mediainfo** - for querying video file information
**gstreamer** - hosting rtsp video server and doing all video processing
### Video Streamer Setter
This is a linux-only console application capable of setting additional video metadata for video files communicating with server via dbus. It can be used only on server machine - no remote acces.
### System Dependencies
dbus - same purpose as in Video Streamer Server
## Video and audio support
There are two containers supported - MP4 and MKV. Video codec and audio codec have to be H264 and AAC.
## Installation
This application can be installed with `pip` tool from PyPi using command:
```
pip3 install video-streamer
```
Alternatively you can install it manually with:
```
git clone https://github.com/artudi54/video-streamer
cd video-streamer
python3 setup.py install
```
## Running
Installation adds scripts to binary folders, they are available with names: `video_streamer.py`, `video_streamer_server.py` of `video_streamer_setter.py`.
## About
Project was created by Artur Pietrzyk and Tomasz Kolbusz as a part of Python university course.