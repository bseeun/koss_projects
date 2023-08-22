import openai

# OpenAI API 키 설정
openai.api_key = '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'

# 오디오 파일 경로
audio_file_path = 'song.mp3'

audio_file = open("song.mp3", "rb")
transcript = openai.Audio.transcribe("whisper-1", audio_file)
text = transcript['text']
print(text)