"""
Multi-Agent Orchestrator for coordinating agents
"""
from typing import Dict, Any
from datetime import datetime
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

import config
from agents import validate_question, retrieve_and_answer


class MultiAgentOrchestrator:
    """Orchestrates multiple agents to handle HR queries about Ravikumar's data"""
    
    def __init__(self, name: str = None):
        self.name = name or config.SYSTEM_NAME
        self.query_history = []
        self.retriever = None
        self._load_vector_store()
    
    def _load_vector_store(self):
        """Load the pre-computed vector store"""
        print("🔄 Loading pre-computed vector store...")
        
        try:
            vector_store_path = config.VECTOR_STORE_PATH / "faiss_index"
            
            if not (vector_store_path / "index.faiss").exists():
                raise FileNotFoundError(
                    f"Vector store not found at {vector_store_path}. "
                    "Please run setup.py first to create the vector store."
                )
            
            # Initialize embeddings
            embeddings = HuggingFaceEmbeddings(
                model_name=config.EMBEDDINGS_MODEL
            )
            
            # Load FAISS vector store
            vector_store = FAISS.load_local(
                str(vector_store_path),
                embeddings,
                allow_dangerous_deserialization=True
            )
            
            # Create retriever
            self.retriever = vector_store.as_retriever(
                search_kwargs={"k": config.RETRIEVER_K}
            )
            
            print("✓ Vector store loaded successfully")
            
        except FileNotFoundError as e:
            print(f"❌ Error: {str(e)}")
            raise
        except Exception as e:
            print(f"❌ Failed to load vector store: {str(e)}")
            raise
    
    def process_query(self, question: str) -> Dict[str, Any]:
        """
        Process a query through the multi-agent system:
        1. Validate the question
        2. Retrieve relevant information
        3. Generate response
        """
        
        # Step 1: Validate the question
        validation_result = validate_question(question)
        
        # Step 2: Retrieve and answer (if validated)
        rag_result = retrieve_and_answer(question, self.retriever, validation_result)
        
        # Step 3: Generate final response
        final_response = {
            "query": question,
            "validation": validation_result,
            "retrieval": rag_result,
            "success": rag_result["success"],
            "timestamp": datetime.now().isoformat()
        }
        
        self.query_history.append(final_response)
        
        return final_response
    
    def get_history(self) -> list:
        """Get query history"""
        return self.query_history
    
    def get_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        total_queries = len(self.query_history)
        hr_appropriate_count = sum(
            1 for q in self.query_history 
            if q['validation']['is_hr_appropriate']
        )
        successful_count = sum(
            1 for q in self.query_history 
            if q['success']
        )
        
        return {
            "total_queries": total_queries,
            "hr_appropriate": hr_appropriate_count,
            "successful": successful_count,
            "system_name": self.name
        }
    
    def clear_history(self):
        """Clear query history"""
        self.query_history = []
