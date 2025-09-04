import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def evaluate_answer(question, answer, language="English", round_type="Technical"):
    """
    Evaluates a candidate's answer using an LLM, providing a score (out of 10) and detailed feedback.
    Supports multilingual feedback and round (HR/Technical) adaptation.
    """
    client = Groq(api_key=GROQ_API_KEY)
    prompt = (
        f"You are an expert {round_type} interviewer.\n"
        f"Evaluate this answer to the following {round_type.lower()} interview question. "
        f"Give a score out of 10 and constructive feedback in {language}.\n"
        f"Question: {question}\nAnswer: {answer}\n"
        "Format: 'Score: X/10\nFeedback: ...'"
    )
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return response.choices[0].message.content


