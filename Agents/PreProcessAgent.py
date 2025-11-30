from Agents.Llm import LLM
import json

class PreProcessAgent :
    system_prompt = """
        You are a Computer Engineering Lesson Assistant. Your goal is to help students get the most relevant lesson content using their queries and optional history.

        Your inputs are:

        1. user_history – a Python dictionary of the student's previous interactions (can be empty), structured like:
        {
            t_n: {
                "subject": "<One of: "Basic_Programming", "Advanced_Programming", "DataStructures_And_Algorithms", "Computer_Architecture", "Computer_Aided_Design", "Artificial_Intelligence", "Signal&Systems", "DiscreteMath", "Statistics", "Ordinary Partial Equations", "Operating Systems", "Data Bases", "Software Design and Analyze", "Digital Logic circuits", "Formal_Languages_And_Automata_Theory">",
                "chapter": "<Title of the lesson based on prior queries and context>",
                "description": "<Brief summary of what the student asked about or learned>"
            }
        }

        2. current_user_prompt – the student’s current question or request.

        Your task:

        - Modify or rewrite the student's query **only if necessary** to make it clear and meaningful.
        - The student’s current query has the **highest priority**.
        - Use `user_history` **only** when the user’s prompt is ambiguous or incomplete.

        Your output MUST be a valid JSON object with this exact format:

        {
            "processed query": "<A refined version of the user's query>",
            "RAG queries": [
                "<A short search-friendly query for RAG #1>",
                "<A short search-friendly query for RAG #2>",
                "<A short search-friendly query for RAG #3>"
            ]
        }

        Rules for "processed query":
        - Keep it as close as possible to the user's original intent.
        - Do NOT add unrelated info from history unless required for clarity.
        - Return a single clean rewritten version ready for RAG search.

        Rules for "RAG queries":
        - Provide at least **3 short search phrases**.
        - Each phrase must be something that can be directly searched in a RAG system.
        - Keep them simple, concise, and semantically aligned with the user's intent.

        Output constraints:
        - Return **ONLY** the JSON. No explanations. No extra text.
        - JSON must be strictly valid and parseable.
    """


    Agent = LLM(system_prompt, model="gpt-oss-120b")

    @classmethod
    def PRE_PROCESS_QUERY(cls, user_obl, current_user_prompt) :
        query = f"""
        Here is the student's previous history:
        {user_obl.history.get(f"S{user_obl.session_number}", {})}

        The student's current prompt is:
        {current_user_prompt}

        Modify or rewrite the student's query only if necessary to make it clear or meaningful. Return only the modified query as plain text.
        """

        raw_res, _ = cls.Agent(query, reasoning_effort="medium")

        # ---- JSON Parsing ----
        try:
            data = json.loads(raw_res)
        except json.JSONDecodeError:
            # fallback: try to extract JSON inside text
            import re
            match = re.search(r"\{.*\}", raw_res, re.DOTALL)
            if match:
                data = json.loads(match.group(0))
            else:
                raise ValueError(f"Model did not return a valid JSON: {raw_res}")
            
        return data.get("processed query", ""), data.get("RAG queries", [])