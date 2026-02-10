# PaperBuddy
Your AI companion that breaks down research papers so you can understand them faster and with clarity

## Overview
PaperBuddy is a Streamlit web application that helps users read and understand research papers using an OpenAI model. It uses a step-by-step teaching approach to guide learners through complex academic concepts.

## Features
- 📄 **PDF Upload**: Upload any research paper in PDF format
- 💬 **Interactive Chat**: Ask questions and have a conversation about the paper
- 🎓 **Step-by-Step Learning**: The AI tutor guides you through concepts incrementally
- 🔄 **Clear Chat**: Reset the conversation to start fresh
- 🤖 **Powered by OpenAI**: Uses GPT-5-mini for intelligent responses

## Installation

1. Clone the repository:
```bash
git clone https://github.com/nerdjerry/PaperBuddy.git
cd PaperBuddy
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

## Usage

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser to the URL shown (typically http://localhost:8501)

3. Upload a PDF research paper

4. Start asking questions!

## How It Works

1. **PDF Processing**: When you upload a PDF, PaperBuddy converts it to clean markdown using `pymupdf4llm`
2. **AI Tutor Setup**: The paper content is fed to an OpenAI model with a specialized system prompt
3. **Interactive Learning**: The AI follows a teaching methodology:
   - Assesses your background knowledge
   - Builds intuition with examples
   - Connects concepts to math
   - Lets you guide the conversation

## Teaching Principles

The AI tutor follows these guidelines:
- Takes one small step at a time
- Asks what you already know before explaining
- Keeps responses short (2-4 paragraphs max)
- Uses concrete examples and analogies
- Teaches math through code experiments when possible
- Always ends with a question to check understanding

## Requirements

- Python 3.8+
- OpenAI API key
- Dependencies listed in `requirements.txt`

## Screenshots
<img width="663" height="572" alt="Screenshot 2026-02-10 at 12 00 00 PM" src="https://github.com/user-attachments/assets/2ae6db1e-7ad5-40d4-ad93-c98a3446308a" />
<img width="671" height="586" alt="Screenshot 2026-02-10 at 11 56 34 AM" src="https://github.com/user-attachments/assets/726fbcdd-1550-4dc3-b239-27bd79c8fc59" />

## Contributing

Feel free to open issues or submit pull requests!

## License

MIT

