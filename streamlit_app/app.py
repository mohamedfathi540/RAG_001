"""
RAG System Testing Frontend
A Streamlit-based interface for testing the RAG (Retrieval-Augmented Generation) API
"""

import streamlit as st
import requests
import json
from datetime import datetime

# Configuration
API_BASE_URL = "http://localhost:8000/api/v1"

# Page configuration
st.set_page_config(
    page_title="RAG System Tester",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        color: white;
        margin: 0;
        font-weight: 700;
        font-size: 2.2rem;
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.85);
        margin: 0.5rem 0 0 0;
        font-size: 1rem;
    }
    
    /* Card styling */
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 1rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
    }
    
    .metric-card h3 {
        color: #667eea;
        margin: 0 0 0.5rem 0;
        font-weight: 600;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-card .value {
        color: white;
        font-size: 1.8rem;
        font-weight: 700;
    }
    
    /* Status indicators */
    .status-online {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(46, 213, 115, 0.15);
        color: #2ed573;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-weight: 500;
        font-size: 0.85rem;
        border: 1px solid rgba(46, 213, 115, 0.3);
    }
    
    .status-offline {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(255, 71, 87, 0.15);
        color: #ff4757;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-weight: 500;
        font-size: 0.85rem;
        border: 1px solid rgba(255, 71, 87, 0.3);
    }
    
    /* Response box styling */
    .response-box {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    .response-box h4 {
        color: #667eea;
        margin: 0 0 1rem 0;
    }
    
    .response-box pre {
        background: rgba(0, 0, 0, 0.3);
        padding: 1rem;
        border-radius: 8px;
        overflow-x: auto;
    }
    
    /* Answer box styling */
    .answer-box {
        background: linear-gradient(135deg, #1a2a1a 0%, #1a2e1a 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #2ed573;
        margin: 1rem 0;
    }
    
    .answer-box p {
        color: white;
        line-height: 1.8;
        font-size: 1.1rem;
    }
    
    /* Source card styling */
    .source-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .source-card .score {
        color: #ffa502;
        font-weight: 600;
    }
    
    /* Button styling overrides */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* File uploader styling */
    .stFileUploader {
        border: 2px dashed rgba(102, 126, 234, 0.5);
        border-radius: 12px;
        padding: 1rem;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    section[data-testid="stSidebar"] .stMarkdown h2 {
        color: white;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        color: white;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
    }
    
    /* Text input styling */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        color: white;
    }
    
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions
def check_api_health():
    """Check if the API is reachable"""
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=5)
        if response.status_code == 200:
            return True, response.json()
        return False, None
    except Exception as e:
        return False, str(e)

def upload_file(project_id: int, file):
    """Upload a file to the API"""
    try:
        files = {"file": (file.name, file.getvalue(), file.type)}
        response = requests.post(
            f"{API_BASE_URL}/data/upload/{project_id}",
            files=files,
            timeout=60
        )
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500

def process_files(project_id: int, chunk_size: int, overlap_size: int, do_reset: int, file_id: str = None):
    """Process uploaded files into chunks"""
    try:
        payload = {
            "chunk_size": chunk_size,
            "overlap_size": overlap_size,
            "Do_reset": do_reset
        }
        if file_id:
            payload["file_id"] = file_id
            
        response = requests.post(
            f"{API_BASE_URL}/data/process/{project_id}",
            json=payload,
            timeout=300
        )
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500

def push_to_index(project_id: int, do_reset: bool = False):
    """Push chunks to vector database"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/nlp/index/push/{project_id}",
            json={"do_reset": do_reset},
            timeout=600
        )
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500

def get_index_info(project_id: int):
    """Get vector index information"""
    try:
        response = requests.get(
            f"{API_BASE_URL}/nlp/index/info/{project_id}",
            timeout=30
        )
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500

def search_index(project_id: int, query: str, limit: int = 5):
    """Search the vector index"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/nlp/index/search/{project_id}",
            json={"text": query, "limit": limit},
            timeout=60
        )
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500

def get_answer(project_id: int, query: str, limit: int = 5):
    """Get AI-generated answer using RAG"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/nlp/index/answer/{project_id}",
            json={"text": query, "limit": limit},
            timeout=120
        )
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500

# Initialize session state
if 'project_id' not in st.session_state:
    st.session_state.project_id = 1
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Sidebar
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    
    # API endpoint configuration
    st.markdown("### 🌐 API Settings")
    api_url = st.text_input("API Base URL", value=API_BASE_URL, key="api_url")
    if api_url != API_BASE_URL:
        API_BASE_URL = api_url
    
    # Project selection
    st.markdown("### 📁 Project")
    st.session_state.project_id = st.number_input(
        "Project ID", 
        min_value=1, 
        value=st.session_state.project_id,
        help="Select the project to work with"
    )
    
    # API Health Check
    st.markdown("### 🏥 API Health")
    if st.button("Check API Status", key="health_check"):
        is_healthy, info = check_api_health()
        if is_healthy:
            st.markdown(f"""
            <div class="status-online">
                ● Online
            </div>
            """, unsafe_allow_html=True)
            st.json(info)
        else:
            st.markdown(f"""
            <div class="status-offline">
                ● Offline
            </div>
            """, unsafe_allow_html=True)
            st.error(f"Error: {info}")
    
    # Quick links
    st.markdown("### 🔗 Quick Links")
    st.markdown(f"""
    - 📊 [Grafana](http://localhost:3000)
    - 📈 [Prometheus](http://localhost:9090)
    - 🔍 [Qdrant](http://localhost:6333/dashboard)
    - 📚 [API Docs](http://localhost:8000/docs)
    """)

# Main content
st.markdown("""
<div class="main-header">
    <h1>🔍 RAG System Tester</h1>
    <p>Test and interact with your Retrieval-Augmented Generation API</p>
</div>
""", unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "📤 Upload & Process", "🔎 Search", "📊 Index Info"])

# Tab 1: Chat (RAG Q&A)
with tab1:
    st.markdown("### 💬 Ask Questions")
    st.markdown("Get AI-generated answers based on your indexed documents.")
    
    # Chat interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        user_question = st.text_area(
            "Your Question",
            placeholder="Ask anything about your documents...",
            height=100,
            key="chat_question"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        context_limit = st.slider("Context Chunks", 1, 10, 5, key="chat_limit")
        ask_button = st.button("🚀 Get Answer", key="ask_btn", use_container_width=True)
    
    if ask_button and user_question:
        with st.spinner("🔄 Generating answer..."):
            result, status_code = get_answer(st.session_state.project_id, user_question, context_limit)
            
            if status_code == 200 and "Answer" in result:
                # Display answer
                st.markdown(f"""
                <div class="answer-box">
                    <h4>🤖 AI Answer</h4>
                    <p>{result['Answer']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Show additional details in expander
                with st.expander("📝 View Full Prompt & Details"):
                    st.markdown("**Full Prompt:**")
                    st.code(result.get('FullPrompt', 'N/A'), language='text')
                    
                    if result.get('ChatHistory'):
                        st.markdown("**Chat History:**")
                        st.json(result['ChatHistory'])
                
                # Add to chat history
                st.session_state.chat_history.append({
                    "question": user_question,
                    "answer": result['Answer'],
                    "timestamp": datetime.now().isoformat()
                })
            else:
                st.error(f"❌ Error: {result.get('Signal', result.get('error', 'Unknown error'))}")
    
    # Display chat history
    if st.session_state.chat_history:
        st.markdown("---")
        st.markdown("### 📜 Chat History")
        for i, chat in enumerate(reversed(st.session_state.chat_history[-5:])):
            with st.expander(f"Q: {chat['question'][:50]}...", expanded=(i==0)):
                st.markdown(f"**Question:** {chat['question']}")
                st.markdown(f"**Answer:** {chat['answer']}")
                st.caption(f"Asked at: {chat['timestamp']}")

# Tab 2: Upload & Process
with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📤 Upload Documents")
        st.markdown("Upload files to your project for processing.")
        
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['pdf', 'txt', 'docx', 'md'],
            help="Supported formats: PDF, TXT, DOCX, MD"
        )
        
        if uploaded_file:
            st.info(f"📄 Selected: **{uploaded_file.name}** ({uploaded_file.size / 1024:.1f} KB)")
            
            if st.button("⬆️ Upload File", key="upload_btn"):
                with st.spinner("📤 Uploading..."):
                    result, status_code = upload_file(st.session_state.project_id, uploaded_file)
                    
                    if status_code == 200:
                        st.success(f"✅ {result.get('signal', 'File uploaded successfully')}")
                        if 'file_id' in result:
                            st.code(f"File ID: {result['file_id']}")
                    else:
                        st.error(f"❌ {result.get('signal', result.get('error', 'Upload failed'))}")
    
    with col2:
        st.markdown("### ⚙️ Process Documents")
        st.markdown("Process uploaded documents into chunks for indexing.")
        
        chunk_size = st.number_input("Chunk Size", min_value=100, max_value=5000, value=500)
        overlap_size = st.number_input("Overlap Size", min_value=0, max_value=500, value=50)
        do_reset = st.checkbox("Reset existing chunks", value=False)
        specific_file_id = st.text_input("Specific File ID (optional)", placeholder="Leave empty to process all files")
        
        if st.button("🔄 Process Files", key="process_btn"):
            with st.spinner("⚙️ Processing files..."):
                result, status_code = process_files(
                    st.session_state.project_id,
                    chunk_size,
                    overlap_size,
                    1 if do_reset else 0,
                    specific_file_id if specific_file_id else None
                )
                
                if status_code == 200:
                    st.success(f"✅ {result.get('signal', 'Processing complete')}")
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("Files Processed", result.get('processed_files', 0))
                    with col_b:
                        st.metric("Chunks Created", result.get('Inserted_chunks', 0))
                else:
                    error_msg = result.get('error', result.get('signal', 'Processing failed'))
                    st.error(f"❌ {error_msg}")
    
    st.markdown("---")
    st.markdown("### 🗄️ Index to Vector Database")
    st.markdown("Push processed chunks to the vector database for semantic search.")
    
    col3, col4 = st.columns([3, 1])
    with col3:
        reset_index = st.checkbox("Reset existing index", value=False, key="reset_idx")
    with col4:
        if st.button("🚀 Push to Index", key="push_idx_btn"):
            with st.spinner("🗄️ Indexing..."):
                result, status_code = push_to_index(st.session_state.project_id, reset_index)
                
                if status_code == 200:
                    st.success(f"✅ {result.get('Signal', 'Indexing complete')}")
                    st.metric("Items Indexed", result.get('InsertedItemsCount', 0))
                else:
                    st.error(f"❌ {result.get('Signal', result.get('error', 'Indexing failed'))}")

# Tab 3: Search
with tab3:
    st.markdown("### 🔎 Semantic Search")
    st.markdown("Search through your indexed documents using natural language.")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input(
            "Search Query",
            placeholder="Enter your search query...",
            key="search_query"
        )
    
    with col2:
        search_limit = st.slider("Results Limit", 1, 20, 5, key="search_limit")
    
    if st.button("🔍 Search", key="search_btn"):
        if search_query:
            with st.spinner("🔍 Searching..."):
                result, status_code = search_index(st.session_state.project_id, search_query, search_limit)
                
                if status_code == 200 and "Results" in result:
                    st.success(f"✅ Found {len(result['Results'])} results")
                    
                    for i, item in enumerate(result['Results'], 1):
                        with st.expander(f"Result #{i} (Score: {item.get('score', 'N/A'):.4f})", expanded=(i==1)):
                            st.markdown(f"**Text:**")
                            st.markdown(f"> {item.get('text', 'N/A')}")
                            
                            if item.get('metadata'):
                                st.markdown("**Metadata:**")
                                st.json(item.get('metadata'))
                else:
                    st.warning(f"⚠️ {result.get('Signal', 'No results found')}")
        else:
            st.warning("⚠️ Please enter a search query")

# Tab 4: Index Info
with tab4:
    st.markdown("### 📊 Vector Index Information")
    st.markdown("View details about your project's vector index.")
    
    if st.button("🔄 Refresh Index Info", key="refresh_info"):
        with st.spinner("📊 Loading index info..."):
            result, status_code = get_index_info(st.session_state.project_id)
            
            if status_code == 200:
                st.success("✅ Index information retrieved")
                
                info = result.get('CollectionInfo', {})
                
                # Display metrics
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("""
                    <div class="metric-card">
                        <h3>Collection Status</h3>
                        <div class="value">Active</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    vectors_count = info.get('vectors_count', info.get('points_count', 'N/A'))
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>Total Vectors</h3>
                        <div class="value">{vectors_count}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>Project ID</h3>
                        <div class="value">{st.session_state.project_id}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Full JSON
                with st.expander("📋 View Full Response"):
                    st.json(result)
            else:
                st.error(f"❌ {result.get('Signal', result.get('error', 'Failed to get index info'))}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: rgba(255,255,255,0.5); padding: 1rem;">
    <p>RAG System Tester • Built with Streamlit • Project: mohamedfathi540/RAG_001</p>
</div>
""", unsafe_allow_html=True)
