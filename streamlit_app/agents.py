"""
Validation and RAG Retrieval Agents
"""
from typing import Dict, Any
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
import json

import config


# Initialize LLM
llm = ChatGroq(
    model_name=config.LLM_MODEL,
    temperature=config.LLM_TEMPERATURE,
    max_tokens=config.LLM_MAX_TOKENS
)


# ============================================================================
# VALIDATION AGENT
# ============================================================================

validation_prompt = PromptTemplate(
    input_variables=["question"],
    template="""You are Ravikumar's chatbot. Your task is to check if the following question is a valid question about Ravikumar.

Question: {question}

Consider:
1. Is this a meaningful question?
2. Is it asking about Ravikumar or his profile?
3. Is it not abusive, offensive, or harmful?

Respond with a JSON object containing:
- is_valid: boolean (true if it's a valid question to ask about Ravikumar)
- confidence: float (0-1)
- reason: brief explanation
- category: "background", "skills", "experience", "education", "achievements", "career", "general", or "invalid"

Example valid questions:
- "Tell me about your background"
- "What are your skills?"
- "What have you accomplished?"
- "Who are you?"

Example invalid questions:
- "What's the weather?"
- "Tell me a joke"

Example response format:
{{"is_valid": true, "confidence": 0.95, "reason": "Valid question about Ravikumar", "category": "background"}}

Your validation response:"""
)


def validate_question(question: str) -> Dict[str, Any]:
    """Validate if a question is valid about Ravikumar"""
    
    # Generate validation
    validation_chain = validation_prompt | llm
    response = validation_chain.invoke({"question": question})
    
    # Parse response
    try:
        response_text = response.content
        # Extract JSON from response
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        if json_start != -1 and json_end > json_start:
            json_str = response_text[json_start:json_end]
            validation_result = json.loads(json_str)
        else:
            validation_result = {
                "is_valid": False,
                "confidence": 0.5,
                "reason": "Could not parse validation response",
                "category": "invalid"
            }
    except json.JSONDecodeError:
        validation_result = {
            "is_valid": False,
            "confidence": 0.5,
            "reason": "Error parsing validation response",
            "category": "invalid"
        }
    
    return validation_result


# ============================================================================
# RAG RETRIEVAL AGENT
# ============================================================================

rag_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""You are Ravikumar, answering a question about yourself. Using the provided personal data, answer the question accurately and professionally as if you are speaking about your own profile.

About me:
{context}

Question: {question}

Instructions:
1. Answer in first person (I, my, me) as Ravikumar
2. Base your answer ONLY on the provided context
3. Be professional, clear, and concise
4. If information is not available in my profile, say "I don't have that specific information available"
5. Speak naturally as if answering directly
6. Share relevant details from your experience, skills, and achievements

Your response as Ravikumar:"""
)


def retrieve_and_answer(
    question: str,
    retriever,
    validation_result: Dict[str, Any]
) -> Dict[str, Any]:
    """Retrieve information and generate answer as Ravikumar"""
    
    if not validation_result.get("is_valid", True):
        return {
            "success": False,
            "answer": "❓ Please ask me a valid question about Ravikumar. For example: 'Tell me about your background', 'What are your skills?', or 'What have you accomplished?'",
            "reason": validation_result.get("reason"),
            "context_retrieved": []
        }
    
    # Retrieve relevant documents
    retrieved_docs = retriever.invoke(question)
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])
    
    # Generate answer
    rag_chain = rag_prompt | llm
    response = rag_chain.invoke({
        "context": context,
        "question": question
    })
    
    return {
        "success": True,
        "answer": response.content,
        "reason": validation_result.get("reason"),
        "context_retrieved": [doc.page_content[:200] + "..." for doc in retrieved_docs]
    }
