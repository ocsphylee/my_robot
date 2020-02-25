from aip import AipSpeech

APP_ID = '18577557'
API_KEY = 'or49f6bzWcXzz7yU1wBSGGhb'
SECRET_KEY = '1XvlM7Nl95PYG0GGtBeK1BRRxwPLWj4a'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

def listen():
    with open('recording.wav', 'rb') as f:
        audio_data = f.read()

    result = client.asr(audio_data, 'wav', 16000, {
        'dev_pid': 1536,
    })

    result_text = result["result"][0]

    print("you said: " + result_text)

    return result_text

listen()