#! /bin/bash
#
# Diffusion youtube avec ffmpeg

# Configurer youtube avec une résolution 720p. La vidéo n'est pas scalée.
rm -rf input* &&
./youtube-dl $2 -o input &&
mv input* input.mp4 &&
ls -a &&
#./ffmpeg -re -stream_loop -1 -i "input.mp4" -vcodec libx264 -pix_fmt yuv420p -b:v 1000k -preset veryfast -maxrate 1000k -bufsize 2500k -vf "format=yuv420p" -g 60 -acodec libmp3lame -b:a 198k -ar 44100 -metadata title="" -metadata artist="" -metadata album_artist="" -metadata album="" -metadata date="" -metadata track="" -metadata genre="" -metadata publisher="" -metadata encoded_by="" -metadata copyright="" -metadata composer="" -metadata performer="" -metadata TIT1="" -metadata TIT3="" -metadata disc="" -metadata TKEY="" -metadata TBPM="" -metadata language="eng" -metadata encoder="" -f flv "rtmp://a.rtmp.youtube.com/live2/$1"
./ffmpeg -re -stream_loop -1 -y -i input.mp4 -i "filter/Filter_HD_Pixel2.png" -af "[0:a]atempo=1.15,volume=1.6,pan=stereo|c0<c0+0*c1|c1<c0+0*c1,aeval=val(0)|-val(1)" -filter_complex "[0:v]setpts=PTS/1.15,crop=iw/1.2:ih/1.2,boxblur=1:2,scale=1280:720 [v1]; [v1][1:v]overlay=0:0,setdar=16/9"  -vcodec libx264 -pix_fmt yuv420p -b:v 500k -preset veryfast -maxrate 500k -bufsize 2500k -r 30 -g 60 -b:v 1400k -profile:v main -level 3.1 -acodec libmp3lame -b:a 128k -ar 44100 -metadata title="" -metadata artist="" -metadata album_artist="" -metadata album="" -metadata date="" -metadata track="" -metadata genre="" -metadata publisher="" -metadata encoded_by="" -metadata copyright="" -metadata composer="" -metadata performer="" -metadata TIT1="" -metadata TIT3="" -metadata disc="" -metadata TKEY="" -metadata TBPM="" -metadata language="eng" -metadata encoder="" -threads 0 -f flv -s 1280x720 "$1"
#./ffmpeg -re -stream_loop -1 -i "input.mp4" $3 -f flv -s 1280x720 "rtmp://a.rtmp.youtube.com/live2/$1"
