from cerebras.cloud.sdk import Cerebras
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import json

class LLM :
    def __init__(self):

        with open("./teaching/books.pkl", "rb") as f:
            knowledge_chunks = pickle.load(f)  # Should contain {"documents": [...], "embeddings": [...]}


        self.__API_key = "your api key here"  # Replace with your actual API key
        self.client = Cerebras(
        # This is the default and can be omitted
        api_key= self.__API_key
        )

        self.models = ["qwen-3-32b", "llama-4-scout-17b-16e-instruct"]

        self.KB = knowledge_chunks

        self.embed_model = SentenceTransformer(
        "nomic-ai/nomic-embed-text-v1",
        trust_remote_code=True
        )




    def get_rag_content(self, query=None, top_k= 10) :


        query_embedding = self.embed_model.encode(query, convert_to_tensor=True, batch_size=8)

        scored_chunks = []
        for chunk_text, chunk_embedding in zip(self.KB["documents"], self.KB["embeddings"]):
            score = cosine_similarity([query_embedding.tolist()], [chunk_embedding])[0][0]
            scored_chunks.append((chunk_text, score))

        scored_chunks.sort(key=lambda x: x[1], reverse=True)

        rag_context = "\n\n".join(text for text, _ in scored_chunks[:top_k])


        return rag_context

    def clean_contex(self, messages):
        if not messages:
            return ''

        new_texts = [f"{msg['role']} : {msg['content']}" for msg in messages]
        new_context = "\n\n".join(new_texts)

        summary_prompt = [
            {"role": "user", "content": f"""تو یک خلاصه‌نویس حرفه‌ای هستی.

    پیام‌های جدید: 
    {new_context}

    لطفاً خلاصه‌ای ترکیبی از کل این مکالمه بنویس. اگر کاربر سوال پرسیده، سوال و جواب را واضح نگه دار. خیلی کلی ننویس.
    """}
        ]

        response = self.client.chat.completions.create(
            messages=summary_prompt,
            model=self.models[0],
            stream=False,
            max_completion_tokens=256,
            temperature=0.2,
            top_p=1
        )

        brief_message = response.choices[0].message.content.strip()
        return brief_message


    def __call__(self, query, messages, summery):


        brief_message = self.clean_contex(messages)

        summery = summery + brief_message if len(summery) < 1024 else brief_message
        print(summery)
        
        rag_data = self.get_rag_content(f"{query, summery}")
        print("Data retrieved from the knowledge base.")

        # Prepare messages for the model

        sys_prompt = """
        شما یک معلم نظریه زبان ها و ماشین ها با تجربه و مهربان هستید. وظیفه شما پاسخ دادن به سؤالات کاربران با استفاده از اطلاعات زمینه‌ای ارائه‌شده (RAG) و سؤالات آن‌ها است. لطفاً همیشه پاسخ‌ها را با لحن مؤدبانه، دوستانه و قابل فهم ارائه دهید.

        قوانین پاسخ‌دهی:
        1. پاسخ‌ها را همیشه به زبان فارسی ارائه دهید، مگر اینکه کاربر صراحتاً درخواست پاسخ به انگلیسی داشته باشد.
        2. لطفاً قبل از پاسخ دادن، ابتدا داده‌های زمینه‌ای (RAG) و خلاصه‌ی چت‌های پیشین را بررسی کن و سپس به پرسش پاسخ بده.
        3. در صورت نیاز به اطلاعات بیشتر برای پاسخ دقیق‌تر، با احترام از کاربر درخواست جزئیات بیشتر کنید.
        4. از استفاده از اصطلاحات تخصصی بدون توضیح خودداری کنید؛ مفاهیم پیچیده را به زبان ساده توضیح دهید.
        5. در صورت وجود مثال‌های مرتبط، آن‌ها را برای درک بهتر موضوع ارائه دهید.
        6. پاسخ‌ها را همیشه در قالب JSON بازگردان. این JSON باید فقط یک کلید با نام "answer" داشته باشد و مقدار آن یک رشته (string) باشد، نه یک JSON دیگر.
        7. محتوای داخل کلید "answer" باید با استفاده از Markdown فرمت‌دهی شده باشد (برای نمایش بهتر در تلگرام).
        8. برای نمایش فرمول‌های ریاضی، از نمادهای `\(` و `\)` برای ریاضی درون‌خطی و از `\[` و `\]` برای فرمول‌های بلوکی استفاده کنید. از نمادهای `$...$` استفاده نکنید.
        """


        messages = [
                    {
                        "role": "system",
                        "content": sys_prompt
                    },

                ]
        
        messages.append({
            "role": "user",
            "content": f"""
        سوال کاربر:
        {query}

        اطلاعات مرتبط از کتاب‌ها:
        {rag_data}

        اطلاعات خلاصه‌شده از چت‌های قبلی:
        {summery}
        """
        })

        # Generate a response using the model
        completion_create_response = self.client.chat.completions.create(
            messages=messages,
            model=self.models[1],
            stream=False,
            max_completion_tokens=1024,
            temperature=0.2,
            top_p=1,
            response_format={"type": "json_object"}
        )


        # Append the assistant's response to the message history
        messages.append({
            "role": "assistant",
            "content": completion_create_response.choices[0].message.content
        })

        # Parse the JSON response
        try:
            content = completion_create_response.choices[0].message.content
            data = json.loads(content)
            print(data)

            if isinstance(data, list):
                first_item = data[1] if data else {}
                if isinstance(first_item, dict):
                    answer = ", ".join(f"{v}" for k, v in first_item.items())
                else:
                    answer = str(first_item)
            elif isinstance(data, dict):
                answer = ", ".join(f"{v}" for k, v in data.items())
            else:
                answer = str(data)

        except json.JSONDecodeError:
            answer = completion_create_response.choices[0].message.content

        # except :
            # data = json.loads(completion_create_response.choices[0].message.content[0])
            # answer = data.get("پاسخ", "")
        return answer, messages, summery

