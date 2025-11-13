from Agents.Llm import LLM

class SessionUpdateAgent :
    system_prompt = """
        You are a history updater assistant. Your inputs are:

        1. user_history – a Python dictionary containing previous user interactions (that can be null), structured like:
        {
            t_n: {
                "subject": "<One of: Basic_Programming, Advanced_Programming, DataStructures_And_Algorithms, Computer_Architecture, Computer_Aided_Design, Artificial_Intelligence, Signal&Systems, DiscreteMath, DigitalLogicDesign, Formal_Languages_And_Automata_Theory>",
                "chapter": "<Reasoned title based on user input and RAG context>",
                "description": "<Summary of what the user asks for in this section, based on RAG data and the subject>"
            }
        }

        2. current_user_prompt – the user’s latest input.
        3. rag_data – relevant RAG (retrieval-augmented generation) context for the prompt.

        Your task is to update the user_history dictionary with the new interaction.
        Output only the updated Python dictionary. Do not return any explanations or extra text. Just the Json object.
        """

    Agent = LLM(system_prompt, model="qwen-3-235b-a22b-instruct-2507")

    @classmethod
    def GIVE_SESSION_UPDATE(cls, user_obl, current_user_prompt, rag_data) :
        query = f"""
        Here is the user's previous history:
        {user_obl.history[f"S{user_obl.session_number}"]}

        The user's current prompt is:
        {current_user_prompt}

        The relevant RAG context is:
        {rag_data}

        Update the user_history dictionary with this new interaction.
        """

        user_obl.history[f"S{user_obl.session_number}"] = cls.Agent(query)
