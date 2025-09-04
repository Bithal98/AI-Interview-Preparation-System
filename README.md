AI Interview Preparation System 🎤🤖
An AI-powered interview preparation web app built with Streamlit, LangChain-style RAG, LLaMA 3, and Whisper.
It generates domain-specific interview questions, evaluates candidate answers (text/voice), and provides personalized AI feedback.
The system supports resume-based tailoring, session history tracking, and PDF export for offline review.
<img width="1919" height="927" alt="Screenshot 2025-09-04 153401" src="https://github.com/user-attachments/assets/56d27c47-178d-41f2-a4b1-d7ea5ea96ac5" />



AI Interview Preparation System
An interactive AI-powered interview preparation web app built with Streamlit. It supports text and voice inputs, allows users to upload resumes for personalized domain-specific questions, evaluates answers with AI-generated feedback, and keeps session history with PDF export.


It is aslo evaluted 
<img width="1909" height="908" alt="Screenshot 2025-09-04 153345" src="https://github.com/user-attachments/assets/e402ee3e-a196-4dea-82fa-f8adc519e4d1" />


🚀 Features

Select interview domains: DSA, DBMS, OOP, ML, HR, Cloud

Upload your resume (PDF/DOCX) for tailored questions

Generate multiple non-repetitive questions per domain

Answer via typing or voice recording (Whisper API-backed STT)

Get AI-powered evaluation with scores & detailed feedback

Track session history and export conversations as PDF

Clean, intuitive Streamlit UI with sidebar instructions

🛠️ Installation & Setup
Prerequisites

Python 3.8+

API keys for:

Groq API
 (AI question generation & evaluation)

Hugging Face API
 (Whisper STT)

Clone & Setup
git clone https://github.com/yourusername/ai-interview-prep.git
cd ai-interview-prep


Create and activate a virtual environment:

python -m venv venv


Windows: venv\Scripts\activate

macOS/Linux: source venv/bin/activate

Install requirements:

pip install -r requirements.txt

Configure API Keys

Create a .env file in the root directory:

GROQ_API_KEY=your_groq_api_key_here
HF_API_TOKEN=your_huggingface_api_token_here


Update modules/whisper_stt.py with your Hugging Face token:

headers = {"Authorization": "Bearer YOUR_HF_ACCESS_TOKEN"}

▶️ Usage

Run the app:

streamlit run app.py


Open the app in your browser: http://localhost:8501

How to Use

Select interview domain from the sidebar.

(Optional) Upload your resume for personalized questions.

Click Generate Question.

Answer by typing or upload a voice response (WAV/MP3).

Click Evaluate Answer for AI feedback & score.

Export entire session as PDF for offline review.

Review session history at the bottom.

📂 Folder Structure
ai-interview-prep/
│── app.py
│── requirements.txt
│── .env
│
├── modules/
│   ├── question_generator.py
│   ├── evaluator.py
│   ├── feedback.py
│   ├── whisper_stt.py
│   └── ...
│
├── utils/
│   ├── pdf_export.py
│   ├── resume_extract.py
│   └── ...
│
├── dashboard/
│   └── history.py
│
├── data/
│   └── question_bank.yaml
│
├── static/
│   ├── logo.png
│   └── style.css
