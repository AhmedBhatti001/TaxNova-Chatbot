import streamlit as st
import os
from datetime import datetime
from utils.llm_utils import get_llm_response

# Page configuration
st.set_page_config(
    page_title="TaxNova Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f4e79;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .chat-container {
        max-height: 600px;
        overflow-y: auto;
        padding: 1rem;
        border-radius: 10px;
        background-color: #f8f9fa;
    }
    .sidebar-content {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
    }
    .info-box {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2196f3;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.header("🏛️ TaxNova Assistant")
    
    st.markdown("### About")
    st.write("TaxNova is your AI-powered assistant for Pakistan Income Tax queries. Get instant answers to your tax-related questions!")
    
    st.markdown("### Features")
    st.write("✅ Income Tax Rates & Slabs")
    st.write("✅ Tax Deductions & Exemptions")
    st.write("✅ Filing Procedures")
    st.write("✅ Tax Calculations")
    st.write("✅ Withholding Tax Rules")
    
    st.markdown("### Quick Tips")
    st.info("💡 Be specific with your questions for better answers!")
    st.info("📊 Ask about current tax rates, deadlines, or procedures")
    st.info("⚖️ For complex cases, consult a tax professional")
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main content
st.markdown('<h1 class="main-header">🤖 TaxNova</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI Chatbot for Pakistan Tax Queries</p>', unsafe_allow_html=True)

# Information box
st.markdown("""
<div class="info-box">
    <strong>Welcome to TaxNova!</strong><br>
    I'm here to help you with Pakistan Income Tax queries. Ask me about tax rates, deductions, filing procedures, and more!
</div>
""", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add welcome message
    welcome_msg = """Hello! I'm TaxNova, your AI assistant for Pakistan Income Tax queries. 

I can help you with:
• Current tax rates and slabs
• Tax deductions and exemptions  
• Filing procedures and deadlines
• Tax calculations
• Withholding tax rules
• And much more!

What would you like to know about Pakistan's tax system?"""
    
    st.session_state.messages.append({
        "role": "assistant", 
        "content": welcome_msg,
        "timestamp": datetime.now().strftime("%H:%M")
    })

# Display chat messages
st.markdown("### 💬 Chat")
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "timestamp" in message:
                st.caption(f"⏰ {message['timestamp']}")

# Chat input
if prompt := st.chat_input("Ask me about Pakistan Income Tax..."):
    # Add user message to chat history
    timestamp = datetime.now().strftime("%H:%M")
    st.session_state.messages.append({
        "role": "user", 
        "content": prompt,
        "timestamp": timestamp
    })
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
        st.caption(f"⏰ {timestamp}")
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = get_llm_response(prompt)
            except Exception as e:
                response = f"I apologize, but I encountered an error: {str(e)}. Please try again or check your API configuration."
        
        st.markdown(response)
        response_timestamp = datetime.now().strftime("%H:%M")
        st.caption(f"⏰ {response_timestamp}")
    
    # Add assistant response to chat history
    st.session_state.messages.append({
        "role": "assistant", 
        "content": response,
        "timestamp": response_timestamp
    })

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    <p>⚠️ <strong>Disclaimer:</strong> This chatbot provides general information about Pakistan's tax system. 
    For specific tax advice, please consult with a qualified tax professional or visit the FBR website.</p>
    <p>🏛️ <strong>Official Source:</strong> <a href="https://fbr.gov.pk" target="_blank">Federal Board of Revenue (FBR)</a></p>
</div>
""", unsafe_allow_html=True)


