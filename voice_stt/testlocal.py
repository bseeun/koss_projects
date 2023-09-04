from google.cloud import speech
import io
import os

# export GOOGLE_APPLICATION_CREDENTIALS="Downloads/"

def run_stt():
    client = speech.SpeechClient()

    file_name = os.path.join(os.path.dirname(__file__), ".", "korean.mp3")

    with io.open(file_name, "rb") as audio_file:
        content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        audio_channel_count=1,
        language_code="ko-KR"
    )

    response = client.recognize(config=config, audio=audio)
    print(response.results)

    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))
    
if __name__ == "__main__":
    run_stt()