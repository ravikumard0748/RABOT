"""
Streamlit App for Multi-Agent RAG System
"""
import streamlit as st
from orchestrator import MultiAgentOrchestrator
import config


# Page Configuration
st.set_page_config(
    page_title="RABOT - Ask Me Anything",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
        .stTabs [data-baseweb="tab-list"] button {
            font-size: 16px;
            font-weight: 600;
        }
        h1 {
            text-align: center;
        }
        h3 {
            text-align: center;
        }
        h4 {
            text-align: center;
        }
        .query-response {
            background-color: #f0f2f6;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .success {
            color: #00a86b;
        }
        .error {
            color: #ff6b6b;
        }
    </style>
""", unsafe_allow_html=True)


# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

@st.cache_resource
def get_orchestrator():
    """Initialize orchestrator (cached)"""
    try:
        return MultiAgentOrchestrator()
    except Exception as e:
        st.error(f"Failed to initialize system: {str(e)}")
        st.stop()


# Initialize orchestrator
orchestrator = get_orchestrator()


# ============================================================================
# MAIN APP
# ============================================================================

st.title("🤖 RABOT")
st.markdown("### Ask Anything About Ravikumar")

st.divider()

# Create tabs
tab1 = st.tabs(
    ["💬 Ask"]
)[0]


# ============================================================================
# TAB 1: ASK QUESTION
# ============================================================================

with tab1:
    st.subheader("Ask Me Anything")
    
    # Centered question input
    col_left, col_center, col_right = st.columns([1, 3, 1])
    
    with col_center:
        question = st.text_area(
            "Your Question:",
            placeholder="E.g., Tell me about your background, What are your skills?",
            height=100,
            label_visibility="collapsed"
        )
        
        submit_button = st.button("🚀 Ask", use_container_width=True)
    
    if submit_button and question.strip():
        # Process query
        with st.spinner("Processing your question..."):
            result = orchestrator.process_query(question)
        
        # Display results
        st.divider()
        
        # Centered answer section
        col_left, col_center, col_right = st.columns([1, 3, 1])
        
        with col_center:
            st.subheader("💭 Response")
            
            if result['success']:
                st.success(result['retrieval']['answer'])
            else:
                st.info(result['retrieval']['answer'])
        
        # Store in session history
        if 'query_results' not in st.session_state:
            st.session_state.query_results = []
        st.session_state.query_results.append(result)
    
    elif submit_button:
        col_left, col_center, col_right = st.columns([1, 3, 1])
        with col_center:
            st.warning("Please enter a question!")
    
    # Example questions
    st.divider()
    
    col_left, col_center, col_right = st.columns([1, 3, 1])
    
    with col_center:
        st.subheader("💡 Example Questions")
        
        example_questions = [
            "Tell me about your professional background",
            "What are your technical skills?",
            "What is your educational background?",
            "Tell me about your achievements and certifications"
        ]
        
        cols = st.columns(2)
        for idx, question in enumerate(example_questions):
            with cols[idx % 2]:
                if st.button(f"📌 {question[:40]}...", use_container_width=True):
                    st.session_state.example_question = question


# ============================================================================
# FOOTER
# ============================================================================

st.divider()
st.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 12px;'>
    🤖 RABOT - Ask Anything About Ravikumar | Powered by Groq & LangChain
    </div>
    """,
    unsafe_allow_html=True
)
