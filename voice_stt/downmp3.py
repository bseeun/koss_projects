from pytube import YouTube
yt = YouTube('https://www.youtube.com/watch?v=oETf7R3JCg4')
output_video = yt.streams.get_lowest_resolution().download(filename='korean.mp3') # 이름이 video.mp4이고 가장 낮은 화질의 영상 다운