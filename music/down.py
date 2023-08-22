from pytube import YouTube
import os
from pydub import AudioSegment
import subprocess
from moviepy.editor import VideoFileClip

def download_video(url):
    yt = YouTube(url)
    output_file = yt.streams.get_lowest_resolution().download(filename = 'video.mp4')
    return output_file

youtube_url = "https://www.youtube.com/watch?v=y7JPgbLfpfA"

# 영상 다운로드
output_video = download_video(youtube_url)

# output_audio = "audio.mp3"

# videoclip = VideoFileClip(output_video)
# audioclip = videoclip.audio
# audioclip.write_audiofile(output_audio)

# audioclip.close()
# videoclip.close()

# os.remove(output_audio)
# os.remove(output_video)

# mp4를 mp3로 변환
# convert_to_mp3(video_file, output_file)

# 다운로드한 mp4 파일 삭제
# os.remove(video_file)
