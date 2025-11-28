from Agents.Llm import LLM
from Agents.CodeAgent import CodeAgent
import json

tools = [
    {
        "type": "function",
        "function": {
            "name": "call_for_code_agent",
            "strict": True,
            "description": "Write, debug, and execute Python code using the CodeAgent. Returns both the code and its output.",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "The task description for writing or debugging Python code."
                    },
                    "current_code": {
                        "type": "string",
                        "description": "The previously generated code that requires debugging or improvement. Empty string if none."
                    }
                },
                "required": ["prompt", "current_code"],
                "additionalProperties": False
            }
        }
    }
]

def call_for_code_agent(prompt: str, rag_context: str, current_code: str):
    code_agent_prompt = f"""
    You are CodeAgent, a Python-code specialist model.

    Here is the relevant context from the books:
    {rag_context}

    Here is the current code (if any):
    {current_code}

    Your task:
    {prompt}

    Remember to follow all the rules provided in your system prompt.
    """

    code, output = CodeAgent.WriteAndExec(
        code_agent_prompt
    )

    return f"Code :{code}\n\nOutput :{output}"



class TaAgent:
    system_prompt = """
        You are an experienced and kind teacher in the field of computer engineering. Your task is to answer users’ questions using:
        - rag_context
        - The user’s interaction history (user_history)
        - The current user query (user_query)

        Always provide answers in a polite, friendly, and understandable manner.

        Inputs:
        1. **user_query** – The user’s current question (highest priority).
        2. **user_history** – A Python dictionary containing the user’s previous interactions (may be empty). Its structure is:

        {
            t_n: {
                "subject": "<one of: "Basic_Programming", "Advanced_Programming", "DataStructures_And_Algorithms", "Computer_Architecture", "Computer_Aided_Design", "Artificial_Intelligence", "Signal&Systems", "DiscreteMath", "Statistics", "Ordinary Partial Equations", "Operating Systems", "Data Bases", "Software Design and Analyze", "Digital Logic circuits", "Formal_Languages_And_Automata_Theory">",
                "chapter": "<a logical title based on the user input and RAG>",
                "description": "<summary of previous content>"
            }
        }

        Response rules (very important — please follow precisely):

        1. Always provide answers in **Persian**, unless the user explicitly requests English.
        2. First, consult the background data (RAG), then user_history.
        - If the question is clear, only use user_query.
        - If the question is ambiguous, use user_history.
        3. Dont write Python codes by your Own use the call_for_code_agent tool.
        4. If more details are needed, politely ask the user.
        5. Avoid unexplained technical terms; explain concepts simply and clearly.
        6. Provide examples wherever possible.
        7. **Your output should be simple Markdown text** (no JSON).
        8. For code, use a Markdown block:

        ```python
        # example
        ```
    9.For mathematical formulas:

        Inline math: \(a . b\)

        Block math: \[a . b\]

    Goal: Provide an educational, understandable response without tables or separators.
    """



    Agent = LLM(system_prompt, model="gpt-oss-120b")

    @classmethod
    def ANSWER_QUERY(cls, query, rag_data, user_obj):
        full_query = f"""
        سوال کاربر:
        {query}

        rag_context
        {rag_data}

        تاریخچه چت‌های قبلی کاربر:
        {user_obj.history}

        اطلاعات خلاصه‌شده از چت‌های قبلی:
        {user_obj.prev_conv_summery}

        /no_think
        """

        message, tool_calls =  cls.Agent(full_query, reasoning_effort="low", tools=tools, max_token=2048)
        # print(tool_calls)
        if tool_calls:
            print(f"REQ FROM [{user_obj.id}] The TA called for CodeAgent help...")
            tool_call = tool_calls[0]
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            # Local execution of the tool
            if name == "call_for_code_agent":
                result = call_for_code_agent(args["prompt"], rag_data, args["current_code"])
                print(f"REQ FROM [{user_obj.id}] The TA has CodeAgent results...")

            else:
                result = "Tool not implemented."
            messages = [
                {"role": "system", "content": cls.system_prompt},
                {"role": "user", "content": full_query},
                {
                    "role": "assistant",
                    "content": message,
                    "tool_calls": [
                        {
                            "id": tool_call.id,
                            "type": "function",
                            "function": {
                                "name": name,
                                "arguments": tool_call.function.arguments
                            }
                        }
                    ]
                },
                {"role": "tool", "tool_call_id": tool_call.id, "content": result}
            ]

            message, _ = cls.Agent(
                query="با توجه به خروجی ابزار، پاسخ کامل و نهایی را ارائه دهید.",
                Messages=messages,
                reasoning_effort="low",
                max_token=2048
            )

        return message