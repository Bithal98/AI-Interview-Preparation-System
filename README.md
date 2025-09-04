# AI-Interview-Preparation-System
AI-powered interview preparation system using LangChain, LLaMA 3, RAG, and Whisper. Generates domain-specific questions, evaluates candidate answers via speech-to-text, and provides personalized feedback with an interactive interface.
<img width="1919" height="927" alt="Screenshot 2025-09-04 153401" src="https://github.com/user-attachments/assets/56d27c47-178d-41f2-a4b1-d7ea5ea96ac5" />



AI Interview Preparation System
An interactive AI-powered interview preparation web app built with Streamlit. It supports text and voice inputs, allows users to upload resumes for personalized domain-specific questions, evaluates answers with AI-generated feedback, and keeps session history with PDF export.


It is aslo evaluted 
<img width="1909" height="908" alt="Screenshot 2025-09-04 153345" src="https://github.com/user-attachments/assets/e402ee3e-a196-4dea-82fa-f8adc519e4d1" />

Features
Select interview domain: DSA, DBMS, OOP, ML, HR, Cloud

Upload your resume (.pdf, .docx) for tailored interview questions

Generate multiple non-repetitive questions per domain

Answer questions by typing or recording/uploading voice (Whisper API-backed speech-to-text)

AI-powered answer evaluation with scores and detailed feedback

Session history tracking with the ability to export conversation to PDF

Clean, intuitive UI with sidebar instructions and multi-format input methods

Demo
Installation & Setup
Prerequisites
Python 3.8+

API keys for:

Groq API (for AI question generation and evaluation)

Hugging Face API (for Whisper speech-to-text)

Clone the repo
text
git clone https://github.com/yourusername/ai-interview-prep.git
cd ai-interview-prep
Create and activate a virtual environment
text
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
Install required packages
text
pip install -r requirements.txt
Setup API keys
Create a .env file in the root:

text
GROQ_API_KEY=your_groq_api_key_here
HF_API_TOKEN=your_huggingface_api_token_here
Update modules/whisper_stt.py with your Hugging Face token:

python
headers = {"Authorization": "Bearer YOUR_HF_ACCESS_TOKEN"}
Replace YOUR_HF_ACCESS_TOKEN with your actual token.

Usage
Start the app with:

text
streamlit run app.py
Open the URL provided (usually http://localhost:8501).

How to Use
Select the interview domain from the sidebar.

(Optional) Upload your resume to get personalized questions.

Click Generate Question.

Answer by typing or upload your voice answer (WAV/MP3).

Click Evaluate Answer to get AI feedback.

Export the entire session as PDF for offline review.

Review your session history at the bottom.

Folder Structure
text
ai-interview-prep/
│
├── app.py
├── requirements.txt
├── modules/
│   ├── question_generator.py
│   ├── evaluator.py
│   ├── feedback.py
│   ├── whisper_stt.py
│   └── ...
├── utils/
│   ├── pdf_export.py
│   ├── resume_extract.py
│   └── ...
├── dashboard/
│   └── history.py
├── data/
│   └── question_bank.yaml
├── static/
│   ├── logo.png
│   └── style.css
└── .env
Contributing
Pull requests and issues are welcome. For major changes, please open an issue first to discuss what you want to change.

License
MIT License

Acknowledgments
Streamlit

Groq AI

Hugging Face Whisper

Inspiration from open source AI projects and interview prep tools
