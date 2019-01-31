#! /bin/bash
#
# Diffusion youtube avec ffmpeg

# Configurer youtube avec une résolution 720p. La vidéo n'est pas scalée.
rm -rf input* &&
./youtube-dl $2 -o input &&
mv input* input.mp4 &&
ls -a &&
#rtmp://a.rtmp.youtube.com/live2/./ffmpeg -re -stream_loop -1 -i "input.mp4" -vcodec libx264 -pix_fmt yuv420p -b:v 1000k -preset veryfast -maxrate 1000k -bufsize 2500k -vf "format=yuv420p" -g 60 -acodec libmp3lame -b:a 198k -ar 44100 -metadata title="" -metadata artist="" -metadata album_artist="" -metadata album="" -metadata date="" -metadata track="" -metadata genre="" -metadata publisher="" -metadata encoded_by="" -metadata copyright="" -metadata composer="" -metadata performer="" -metadata TIT1="" -metadata TIT3="" -metadata disc="" -metadata TKEY="" -metadata TBPM="" -metadata language="eng" -metadata encoder="" -f flv "rtmp://a.rtmp.youtube.com/live2/$1"
./ffmpeg -re -stream_loop -1 -i "input.mp4" -filter_complex setpts=PTS/1 -vcodec libx264 -pix_fmt yuv420p -b:v 1000k -acodec libmp3lame -b:a 128k -ar 44100 -threads 0 -preset superfast -maxrate 1000k -bufsize 2500k -f flv -s 1280x720 "$1"
