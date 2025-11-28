from cerebras.cloud.sdk import Cerebras
import os
from dotenv import load_dotenv

load_dotenv()



MODELS = ["qwen-3-32b", "gpt-oss-120b", "qwen-3-235b-a22b-instruct-2507"]
Course_List = ["Basic_Programming", "Advanced_Programming", "DataStructures_And_Algorithms", "Computer_Architecture", "Computer_Aided_Design", "Artificial_Intelligence", "Signal&Systems", "DiscreteMath", "Statistics", "Ordinary Partial Equations", "Operating Systems", "Data Bases", "Software Design and Analyze", "Digital Logic circuits", "Formal_Languages_And_Automata_Theory"]

class LLM :
    def __init__(self, system_prompt, model="qwen-3-32b", ApiKey=None) :

        self.client = Cerebras(
        # This is the default and can be omitted
        api_key= os.getenv("CEREBRAS_API_KEY") if ApiKey is not None else ApiKey
        )

        self.system_prompt = system_prompt
        self.model = model



    def __call__(self, query, reasoning_effort="low", tools=None, Messages=None, max_token=1024) :

        # Generate a response using the model
        if self.model =="gpt-oss-120b" :

            completion_create_response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": query}
                ] if Messages is None else Messages,
                model=self.model,
                stream=False,
                tools=tools,
                max_completion_tokens=max_token,
                temperature=0.2,
                top_p=1,
                reasoning_effort=reasoning_effort
            )

        else :
            
            completion_create_response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": query}
                ] if Messages is None else Messages,
                model=self.model,
                stream=False,
                tools=tools,
                max_completion_tokens=1024,
                temperature=0.2,
                top_p=1,
                response_format={"type": "json_object"},
            )

        return completion_create_response.choices[0].message.content, completion_create_response.choices[0].message.tool_calls
    