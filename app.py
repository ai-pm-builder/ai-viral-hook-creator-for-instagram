"""
Streamlit app for generating viral Instagram hooks for food content.
Integrates with Langflow API to generate hook recommendations.
"""

import streamlit as st
from langflow_client import LangflowClient
from config import Config
import time


# Page configuration
st.set_page_config(
    page_title="Viral Hook Generator",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #FF6B6B 0%, #4ECDC4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .hook-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
    }
    .hook-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    .hook-number {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .hook-text {
        font-size: 1.1rem;
        line-height: 1.6;
    }
    .stTextInput > div > div > input {
        border-radius: 10px;
    }
    .stTextArea > div > div > textarea {
        border-radius: 10px;
    }
    .stButton > button {
        border-radius: 10px;
        background: linear-gradient(90deg, #FF6B6B 0%, #4ECDC4 100%);
        color: white;
        font-weight: bold;
        padding: 0.5rem 2rem;
        border: none;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .success-message {
        padding: 1rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        color: #155724;
        margin: 1rem 0;
    }
    .error-message {
        padding: 1rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        color: #721c24;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if "hooks" not in st.session_state:
        st.session_state.hooks = []
    if "last_description" not in st.session_state:
        st.session_state.last_description = ""


def display_header():
    """Display app header."""
    st.markdown('<h1 class="main-header">🍔 Viral Hook Generator</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitle">Generate viral Instagram hooks for your food content using AI</p>',
        unsafe_allow_html=True
    )


def display_input_section():
    """Display input section for video description."""
    st.markdown("### 📝 Describe Your Video")
    st.markdown("Enter a brief description of the food video you want to create:")
    
    video_description = st.text_area(
        "Video Description",
        height=150,
        placeholder="e.g., A quick tutorial on making the perfect chocolate chip cookies with a secret ingredient that makes them extra chewy...",
        key="video_description"
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        generate_button = st.button("✨ Generate Hooks", type="primary", use_container_width=True)
    
    return video_description, generate_button


def display_hooks(hooks: list):
    """Display generated hooks in formatted cards."""
    if not hooks:
        return
    
    st.markdown("### 🎯 Generated Viral Hooks")
    st.markdown("---")
    
    for idx, hook in enumerate(hooks, 1):
        hook_html = f"""
        <div class="hook-card">
            <div class="hook-number">Hook #{idx}</div>
            <div class="hook-text">{hook}</div>
        </div>
        """
        st.markdown(hook_html, unsafe_allow_html=True)
        
        # Copy button for each hook
        col1, col2 = st.columns([5, 1])
        with col2:
            if st.button("📋 Copy", key=f"copy_{idx}"):
                st.write(f"Copied: {hook[:50]}...")
                st.code(hook, language=None)


def generate_hooks(video_description: str):
    """Generate hooks using Langflow API."""
    try:
        # Validate configuration
        Config.validate()
        
        # Initialize client
        client = LangflowClient()
        
        # Show loading state
        with st.spinner("🤖 Generating viral hooks... This may take a moment."):
            # Call Langflow API
            response = client.generate_hooks(video_description)
            
            # Parse response
            hooks = client.parse_hooks_response(response)
            
            # Store in session state
            st.session_state.hooks = hooks
            st.session_state.last_description = video_description
            
            return hooks, None
            
    except Exception as e:
        error_message = str(e)
        return None, error_message


def main():
    """Main application function."""
    initialize_session_state()
    display_header()
    
    # Input section
    video_description, generate_button = display_input_section()
    
    # Generate hooks on button click
    if generate_button:
        if not video_description or len(video_description.strip()) < 10:
            st.error("⚠️ Please enter a more detailed description (at least 10 characters).")
        else:
            hooks, error = generate_hooks(video_description.strip())
            
            if error:
                st.markdown(f'<div class="error-message">❌ Error: {error}</div>', unsafe_allow_html=True)
                st.info("💡 Make sure your Langflow API is running and the URL is correct in your .env file.")
            elif hooks:
                st.success("✅ Hooks generated successfully!")
                display_hooks(hooks)
    
    # Display previous hooks if available
    elif st.session_state.hooks:
        st.info("💡 Enter a new description above to generate more hooks, or view your previous results below:")
        display_hooks(st.session_state.hooks)
    
    # Sidebar with instructions
    with st.sidebar:
        st.markdown("## 📖 How to Use")
        st.markdown("""
        1. **Describe your video**: Enter a brief description of the food video you want to create
        2. **Click Generate**: The AI will analyze your description and create viral hooks
        3. **Copy & Use**: Copy the hooks you like and use them for your Instagram content
        
        ### 🔧 Setup
        Make sure you have:
        - Langflow API running
        - `.env` file configured with `LANGFLOW_API_URL`
        - Optional: `LANGFLOW_API_KEY` if authentication is required
        """)
        
        st.markdown("---")
        st.markdown("### ⚙️ Configuration")
        st.code(f"API URL: {Config.LANGFLOW_API_URL}", language=None)
        if Config.LANGFLOW_API_KEY:
            st.code(f"API Key: {'*' * len(Config.LANGFLOW_API_KEY)}", language=None)
        else:
            st.info("No API key configured")


if __name__ == "__main__":
    main()
