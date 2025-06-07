import requests
import nomic
import numpy as np

from nomic import embed

class EmbedSys() :

    def __init__(self):
        self.__key = "your_api_key"  # Replace with your actual API key
        nomic.login(self.__key)



    @property
    def getAPI(self) :
        return self.__key
    
    def __call__(self, text):

        output = embed.text(
            texts=[text],  # متغیر query باید به‌صورت رشته (string) باشد
            model='nomic-embed-text-v1.5',
            task_type='search_query',
        )

        return np.array(output['embeddings'][0])
