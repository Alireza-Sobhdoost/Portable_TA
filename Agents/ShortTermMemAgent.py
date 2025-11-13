from Agents.Llm import LLM

class ShortTermMemAgent :
    system_prompt = """
        You are a history updater assistant. Your inputs are:

        1. user_history – a Python dictionary containing previous user interactions (can be null), structured like:
        {
            t_n: {
                "subject": "<One of: Basic_Programming, Advanced_Programming, DataStructures_And_Algorithms, Computer_Architecture, Computer_Aided_Design, Artificial_Intelligence, Signal&Systems, DiscreteMath, DigitalLogicDesign, Formal_Languages_And_Automata_Theory>",
                "chapter": "<Reasoned title based on user input and RAG context>",
                "description": "<Summary of what the user asks for in this section, based on RAG data and the subject>"
            }
        }

        2. current_user_prompt – the user’s latest input.
        3. rag_data – relevant RAG (retrieval-augmented generation) context for the prompt.
        4. agent_answer – the agent's response to the prompt.

        Your task is to create a summary containing two important parts:

        1. User Section:
        - What the user just said (briefly).
        - What problem or question the user had (more concise).

        2. Agent Section:
        - How the agent approached solving the problem.
        - Key answers, suggestions, or clarifying questions from the agent.

        Return the summary as a Python dictionary in the following format:

        {
            "user_summary": "<Brief description of user's input and problem>",
            "agent_summary": "<Explanation of agent's approach, answer, or solution>"
        }
        Do not return any explanations or extra text. Just the Json object.
        """
    Agent = LLM(system_prompt, model="qwen-3-235b-a22b-instruct-2507")

    @classmethod
    def GIVE_SHORT_TERM_MEM(cls, user_obj, current_user_prompt, rag_data, agent_answer) :
        query = f"""
        Here is the user's previous history:
        {user_obj.history[f"S{user_obj.session_number}"]}

        The user's current prompt is:
        {current_user_prompt}

        The relevant RAG context is:
        {rag_data}

        The agent's last answer is:
        {agent_answer}

        Generate a concise summary of the recent interaction to update the short-term memory.
        """

        user_obj.prev_conv_summery = cls.Agent(query)
