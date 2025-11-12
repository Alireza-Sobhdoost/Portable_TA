from cerebras.cloud.sdk import Cerebras
import os



MODELS = ["qwen-3-32b", "gpt-oss-120b", "qwen-3-235b-a22b-instruct-2507"]

class LLM :
    def __init__(self, system_prompt, model="qwen-3-32b") :


        self.__API_key = os.getenv("CEREBRAS_API_KEY")
        self.client = Cerebras(
        # This is the default and can be omitted
        api_key= self.__API_key
        )

        self.system_prompt = system_prompt



    def __call__(self, query, reasoning_effort="low"):

        # Generate a response using the model
        if self.model =="gpt-oss-120b" :

            completion_create_response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": query}
                ],
                model=self.model,
                stream=False,
                max_completion_tokens=1024,
                temperature=0.2,
                top_p=1,
                response_format={"type": "json_object"},
                reasoning_effort=reasoning_effort
            )

        else :
            
            completion_create_response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": query}
                ],
                model=self.model,
                stream=False,
                max_completion_tokens=1024,
                temperature=0.2,
                top_p=1,
                response_format={"type": "json_object"},
            )

        return completion_create_response.choices[0].message.content
    