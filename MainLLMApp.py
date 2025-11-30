from Agents.PreProcessAgent import PreProcessAgent
from Agents.TaAgent import TaAgent
from Agents.SessionUpdateAgent import SessionUpdateAgent
from Agents.ShortTermMemAgent import ShortTermMemAgent

from Tools.RagTool import RagTool

import json

class MainLLMApp :

    def __init__(self):
        
        self.rag_tool = RagTool()

    def __call__(self, user_obj, current_user_prompt) :
        # Step 1: Pre-process the user query
        print(f"REQ FROM [{user_obj.id}] in MainLLMApp: Pre-processing the user query...")
        pre_processed_query, rag_queries = PreProcessAgent.PRE_PROCESS_QUERY(user_obj, current_user_prompt)

        print(rag_queries)

        # Step 2: Retrieve RAG context
        print(f"REQ FROM [{user_obj.id}] in MainLLMApp: Retrieving RAG context...")
        rag_context = self.rag_tool.get_rag_context(rag_queries)

        print(rag_context)


        # Step 4: Generate answer using TaAgent
        print(f"REQ FROM [{user_obj.id}] in MainLLMApp: Generating answer using TaAgent...")
        answer = TaAgent.ANSWER_QUERY(pre_processed_query, rag_context, user_obj)

        # Step 5: Update session history
        print(f"REQ FROM [{user_obj.id}] in MainLLMApp: Updating session history...")
        SessionUpdateAgent.GIVE_SESSION_UPDATE(user_obj, current_user_prompt, rag_context)
        # Step 6: Update short-term memory
        print(f"REQ FROM [{user_obj.id}] in MainLLMApp: Updating short-term memory...")
        ShortTermMemAgent.GIVE_SHORT_TERM_MEM(user_obj, current_user_prompt, rag_context, answer) 


        return answer