from Agents.PreProcessAgent import PreProcessAgent
from Agents.TaAgent import TaAgent
from Agents.SessionUpdateAgent import SessionUpdateAgent
from Agents.ShortTermMemAgent import ShortTermMemAgent

from Tools.RagTool import RagTool

class MainLLMApp :

    def __init__(self):
        
        self.rag_tool = RagTool()

    def __call__(self, user_obj, current_user_prompt) :
        # Step 1: Pre-process the user query
        print("MainLLMApp: Pre-processing the user query...")
        pre_processed_query = PreProcessAgent.PRE_PROCESS_QUERY(user_obj, current_user_prompt)

        # Step 2: Retrieve RAG context
        print("MainLLMApp: Retrieving RAG context...")
        rag_context = self.rag_tool.get_rag_context(pre_processed_query)


        # Step 4: Generate answer using TaAgent
        print("MainLLMApp: Generating answer using TaAgent...")
        answer = TaAgent.ANSWER_QUERY(pre_processed_query, rag_context, user_obj)

        # Step 5: Update session history
        print("MainLLMApp: Updating session history...")
        SessionUpdateAgent.GIVE_SESSION_UPDATE(user_obj, current_user_prompt, rag_context)
        # Step 6: Update short-term memory
        print("MainLLMApp: Updating short-term memory...")
        ShortTermMemAgent.GIVE_SHORT_TERM_MEM(user_obj, current_user_prompt, rag_context, answer) 


        return answer