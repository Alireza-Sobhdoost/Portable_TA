import requests
# from openai import OpenAI
# TODO: FIX this file

class VoiceModel:
    def __init__(self):
        self.__apikey = "your_api_key"  # Replace with your actual API key
        self.client = OpenAI(api_key = self.__apikey , base_url="https://api.metisai.ir/openai/v1")

    @property
    def getAPI(self):
        return self.__apikey

    def __call__(self, audio_file):
        url = "https://api.metisai.ir/openai/v1/audio/transcriptions"
        headers = {
            "Authorization": self.getAPI
        }

        files = {
            "file": (audio_file, open(audio_file, "rb"), "audio/mpeg")
        }

        data = {
            "model": "whisper-1"
        }

        response = requests.post(url, headers=headers, files=files, data=data)

        print("Status Code:", response.status_code)
        # print("Response:\n", response.json()['text'])

        return response.json()['text']


