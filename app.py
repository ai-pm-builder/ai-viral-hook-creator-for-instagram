"""
Streamlit app for generating viral Instagram hooks for food content.
Integrates with Langflow API to generate hook recommendations.
"""

import streamlit as st
from instagram_hook_chain import run_full_chain
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
    if "results" not in st.session_state:
        st.session_state.results = {}
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


def display_hooks(results: dict):
    """Display generated hooks and production card in formatted layout."""
    if not results:
        return
    
    # Display the final winning hook/production card
    if "production_card" in results:
        st.markdown("### 🏆 Winning Hook Production Card")
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); padding: 20px; border-radius: 15px; color: white; margin-bottom: 25px;">
            <div style="font-size: 1.2rem; white-space: pre-wrap;">{results['production_card']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("📋 View Winning Hook Analysis"):
            st.markdown(results["winner_analysis"])

    # Display all generated hooks
    st.markdown("### 🎯 All Candidate Hooks")
    st.markdown("---")
    
    # Extract hooks from generated_hooks string
    import re
    hooks_text = results.get("generated_hooks", "")
    hooks = re.findall(r"HOOK \d+: (.*?)(?=HOOK \d+:|$)", hooks_text, re.DOTALL)
    
    if not hooks:
        hooks = [hooks_text]

    for idx, hook in enumerate(hooks, 1):
        hook_html = f"""
        <div class="hook-card">
            <div class="hook-number">Hook #{idx}</div>
            <div class="hook-text">{hook.strip()}</div>
        </div>
        """
        st.markdown(hook_html, unsafe_allow_html=True)
    
    # Display Simulation if available
    if "priya_simulation" in results:
        with st.expander("🔬 View Persona Simulation (Priya)"):
            st.markdown(results["priya_simulation"])


def generate_hooks(video_description: str):
    """Generate hooks using LangChain workflow."""
    try:
        # Validate configuration
        Config.validate()
        
        # Show loading state
        with st.spinner("🤖 Running AI Content Stratgist Chain... This may take a moment."):
            # Call LangChain workflow
            results = run_full_chain(video_description)
            
            # Store in session state
            st.session_state.results = results
            st.session_state.last_description = video_description
            
            return results, None
            
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
            results, error = generate_hooks(video_description.strip())
            
            if error:
                st.markdown(f'<div class="error-message">❌ Error: {error}</div>', unsafe_allow_html=True)
                st.info("💡 Make sure your GEMINI_API_KEY is correct in your .env file.")
            elif results:
                st.success("✅ Workflow complete!")
                display_hooks(results)
    
    # Display previous result if available
    elif st.session_state.results:
        st.info("💡 Enter a new description above to generate more hooks, or view your previous results below:")
        display_hooks(st.session_state.results)
    
    # Sidebar with instructions
    with st.sidebar:
        st.markdown("## 📖 How to Use")
        st.markdown("""
        1. **Describe your video**: Enter a brief description of the food video you want to create
        2. **Click Generate**: The AI will run a 4-step workflow:
            - Generate candidate hooks
            - Simulate person reaction (Priya)
            - Rank hooks based on evidence
            - Create final production card
        3. **Copy & Use**: Use the production card for your shoot!
        
        ### 🔧 Setup
        Make sure you have:
        - `.env` file configured with `GEMINI_API_KEY`
        """)
        
        st.markdown("---")
        st.markdown("### ⚙️ Configuration")
        if Config.GEMINI_API_KEY:
            st.code(f"Gemini API Key: {'*' * 8}{Config.GEMINI_API_KEY[-4:]}", language=None)
        else:
            st.warning("⚠️ No Gemini API key configured")


if __name__ == "__main__":
    main()
