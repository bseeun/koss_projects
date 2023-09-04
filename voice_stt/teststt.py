from google.cloud import speech

# export GOOGLE_APPLICATION_CREDENTIALS="Downloads/"

def run_stt():
    client = speech.SpeechClient()

    gcs_uri = "gs://bucketvoicenew/korean.flac"

    # 일단 모델을 무조건 써야겠다
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=44100,
        audio_channel_count=2,
        language_code="ko-KR",
        model="latest_short"
    )

    audio = speech.RecognitionAudio(uri=gcs_uri)

    # 10MB 이하
    # response = client.recognize(config=config, audio=audio)

    # 10MB 이상
    res = client.long_running_recognize(config=config, audio=audio)
    
    response = res.result()
    # print(response.results)

    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))
    
if __name__ == "__main__":
    run_stt()
    
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/baeseeun/Downloads/key.json"