import nomic
import numpy as np
import os
from nomic import embed

class EmbedSys() :

    def __init__(self):
        self.__key =  os.getenv("NOMIC_API_KEY")
        nomic.login(self.__key)

    @property
    def getAPI(self) :
        return self.__key
    
    def __call__(self, text):

        output = embed.text(
            texts=[text],
            model='nomic-embed-text-v1.5',
            task_type='search_query',
        )

        return np.array(output['embeddings'][0])
