# import yaml
# import random

# def load_questions():
#     with open('data/question_bank.yaml', 'r') as f:
#         return yaml.safe_load(f)

# QUESTION_BANK = load_questions()

# def generate_question(domain):
#     if domain in QUESTION_BANK:
#         return random.choice(QUESTION_BANK[domain])
#     return "Tell me about yourself."

# # def generate_questions_from_resume(domain, resume_text):
# #     from groq import Groq
# #     import os
# #     client = Groq(api_key=os.getenv("GROQ_API_KEY"))
# #     prompt = (
# #     f"Carefully read the following resume content:\n{resume_text}\n\n"
# #     f"Based on the candidate's resume above, generate exactly 5 distinct, technically detailed interview questions for the '{domain}' domain. "
# #     "Write ONLY the questions, without any explanation or heading. Number each question from 1 to 5."
# # )

# #     response = client.chat.completions.create(
# #         model="openai/gpt-oss-20b",
# #         messages=[{"role": "user", "content": prompt}]
# #     )
# #     # You may need to parse/combine LLM response into a list
# #     questions = response.choices[0].message.content.split('\n')
# #     return [q for q in questions if q.strip()]



# def generate_questions_from_resume(domain, resume_text):
#     from groq import Groq
#     import os

#     client = Groq(api_key=os.getenv("GROQ_API_KEY"))
#     prompt = (
#         f"Resume:\n{resume_text}\n\n"
#         f"Based on this résumé, generate exactly 5 distinct, technical interview questions for the '{domain}' domain "
#         "that would test the depth of knowledge and skills shown in the résumé. "
#         "Number each question from 1 to 5. Do not return any headings, explanations, or introductory sentences—only the questions."
#     )
#     response = client.chat.completions.create(
#         model="llama-3.1-8b-instant",
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0.3
#     )
#     raw_output = response.choices[0].message.content
#     # Parse ONLY numbered questions, skip any heading lines
#     questions = []
#     for line in raw_output.split('\n'):
#         line = line.strip()
#         # Accept lines starting with a digit and a period, like "1. What is ...?"
#         if line and line[0].isdigit() and '.' in line[:3]:
#             question_text = line.split('.', 1)[1].strip()
#             if len(question_text) > 10:
#                 questions.append(question_text)
#     # If not parsed, fallback to all lines longer than 10 chars
#     if not questions:
#         questions = [line for line in raw_output.split('\n') if len(line.strip()) > 20 and 'question' not in line.lower()]
#     return questions





import yaml
import random

def load_questions():
    with open('data/question_bank.yaml', 'r') as f:
        return yaml.safe_load(f)

QUESTION_BANK = load_questions()

def generate_question(domain, return_all=False):
    if domain in QUESTION_BANK:
        return QUESTION_BANK[domain] if return_all else random.choice(QUESTION_BANK[domain])
    return ["Tell me about yourself."] if return_all else "Tell me about yourself."

def generate_questions_from_resume(domain, resume_text):
    from groq import Groq
    import os
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    prompt = (
        f"Resume:\n{resume_text}\n\n"
        f"Based on this résumé, generate exactly 5 distinct, technical interview questions for the '{domain}' domain. "
        "Number each question from 1 to 5. Only output the questions."
    )
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    raw = response.choices[0].message.content
    questions = []
    for line in raw.split('\n'):
        line = line.strip()
        if line and line[0].isdigit() and '.' in line[:3]:
            q = line.split('.', 1)[1].strip()
            if len(q) > 10:
                questions.append(q)
    if not questions:
        questions = [line.strip() for line in raw.split('\n') if len(line.strip()) > 20]
    return questions
