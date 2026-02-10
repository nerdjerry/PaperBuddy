"""
Research Paper Tutor - A Streamlit app to help users understand research papers
using an OpenAI model via lisette (lightweight wrapper over litellm).
"""

import streamlit as st
import pymupdf4llm
from lisette import Chat
import tempfile
import os
from dotenv import load_dotenv
from config import SYSTEM_PROMPT_TEMPLATE, DEFAULT_MODEL, DEFAULT_TEMPERATURE

# Load environment variables from .env file
load_dotenv()


def create_system_prompt(paper_txt):
    """
    Create the system prompt for the AI tutor.
    
    Args:
        paper_txt: The extracted markdown text from the research paper
        
    Returns:
        A formatted system prompt string
    """
    return SYSTEM_PROMPT_TEMPLATE.format(paper_txt=paper_txt)

# Configure the Streamlit page
st.set_page_config(
    page_title="Research Paper Tutor",
    page_icon="📚",
    layout="centered"
)

# Display the main title
st.title("📚 Research Paper Tutor")

# Verify OpenAI API key is set
if not os.getenv("OPENAI_API_KEY"):
    st.error("⚠️ OPENAI_API_KEY not found in environment variables. Please set it in your .env file.")
    st.stop()

# Initialize session state variables to persist data across reruns
# session_state maintains values across Streamlit reruns
if "messages" not in st.session_state:
    # Store chat history as list of dicts with 'role' and 'content' keys
    st.session_state.messages = []

if "paper_txt" not in st.session_state:
    # Store the extracted markdown text from the uploaded PDF
    st.session_state.paper_txt = None

if "llm" not in st.session_state:
    # Store the Lisette LLM instance for conversation
    st.session_state.llm = None

# File uploader widget - accepts only PDF files
uploaded_file = st.file_uploader(
    "Upload a research paper (PDF)",
    type=["pdf"],
    help="Upload a single PDF research paper to analyze"
)

# Process the uploaded PDF
if uploaded_file is not None and st.session_state.paper_txt is None:
    # Show a spinner while processing the PDF
    with st.spinner("Processing PDF... This may take a moment."):
        try:
            # Create a temporary file to save the uploaded PDF
            # tempfile.NamedTemporaryFile creates a temp file that's automatically deleted
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                # Write the uploaded file content to the temporary file
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            
            # Convert PDF to markdown using pymupdf4llm
            # This extracts text and structure from the PDF in markdown format
            paper_txt = pymupdf4llm.to_markdown(tmp_file_path)
            
            # Store the extracted text in session state
            st.session_state.paper_txt = paper_txt
            
            # Clean up: remove the temporary file
            os.unlink(tmp_file_path)
            
            # Create the system prompt that defines the AI tutor's behavior
            system_prompt = create_system_prompt(paper_txt)
            
            # Initialize the LLM using lisette Chat
            # Chat is a lightweight wrapper over litellm for easy conversation management
            st.session_state.llm = Chat(
                model=DEFAULT_MODEL,  # Use model from config
                sp=system_prompt,  # Set the system prompt using 'sp' parameter
                temp=DEFAULT_TEMPERATURE,  # Temperature from config
            )
            
            # Show success message
            st.success("✅ PDF processed successfully! You can now ask questions about the paper.")
            
        except Exception as e:
            # Handle any errors during PDF processing
            st.error(f"❌ Error processing PDF: {str(e)}")
            st.error("Please make sure you uploaded a valid PDF file.")

# Show chat interface only if paper has been processed
if st.session_state.paper_txt is not None:
    
    # Add a clear chat button in the sidebar
    if st.sidebar.button("🗑️ Clear Chat", use_container_width=True):
        # Reset chat history
        st.session_state.messages = []
        # Reinitialize the LLM to start fresh conversation
        # This clears the conversation history in the LLM
        if st.session_state.llm:
            system_prompt = create_system_prompt(st.session_state.paper_txt)
            st.session_state.llm = Chat(
                model=DEFAULT_MODEL,
                sp=system_prompt,
                temp=DEFAULT_TEMPERATURE,
            )
        st.rerun()  # Rerun the app to reflect the cleared state
    
    # Display chat history
    # Iterate through all messages and display them in a conversational format
    for message in st.session_state.messages:
        # Use st.chat_message to create chat bubbles
        # 'role' can be 'user' or 'assistant'
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input widget - allows user to type messages
    if prompt := st.chat_input("Ask a question about the paper..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message immediately
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate assistant response
        with st.chat_message("assistant"):
            # Create a placeholder for streaming response
            message_placeholder = st.empty()
            
            try:
                # Send the user's message to the LLM and get response
                # Chat instance is callable - conversation history is automatically maintained
                response = st.session_state.llm(prompt)
                
                # Extract the message content from the response
                # response is a ModelResponse object, we need to get the actual text content
                response_text = response.choices[0].message.content
                
                # Display the full response
                message_placeholder.markdown(response_text)
                
                # Add assistant response to chat history
                st.session_state.messages.append(
                    {"role": "assistant", "content": response_text}
                )
                
            except Exception as e:
                # Handle errors during LLM call
                error_msg = f"❌ Error generating response: {str(e)}"
                message_placeholder.markdown(error_msg)
                st.session_state.messages.append(
                    {"role": "assistant", "content": error_msg}
                )

else:
    # Show instructions when no paper is uploaded
    st.info("👆 Please upload a PDF research paper to get started!")
    
    # Show some helpful information
    st.markdown("""
    ### How it works:
    1. Upload a research paper in PDF format
    2. The AI tutor will read and understand the paper
    3. Ask questions to understand the paper better
    4. The tutor will guide you step-by-step through the concepts
    
    ### Features:
    - 📄 Upload any research paper (PDF)
    - 💬 Chat-style interface for questions
    - 🎓 Step-by-step learning approach
    - 🔄 Clear chat to start over
    """)
