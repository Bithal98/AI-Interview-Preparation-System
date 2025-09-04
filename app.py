# import streamlit as st
# from modules.question_generator import generate_question, generate_questions_from_resume
# from modules.evaluator import evaluate_answer
# from modules.feedback import format_feedback
# from dashboard.history import show_history
# from utils.pdf_export import export_interview_session
# import modules.whisper_stt as whisper_stt
# from io import BytesIO
# from gtts import gTTS
# import tempfile
# from streamlit_webrtc import webrtc_streamer, WebRtcMode

# import av
# import io
# import wave

# # Map UI languages to gtts language codes
# LANG_CODE_MAP = {'English': 'en', 'Hindi': 'hi', 'Odia': 'or'}


# def speak_text(text, lang='en'):
#     tts = gTTS(text=text, lang=lang)
#     mp3_fp = BytesIO()
#     tts.write_to_fp(mp3_fp)
#     mp3_fp.seek(0)
#     st.audio(mp3_fp.read(), format='audio/mp3')


# def audio_frame_callback(frame):
#     audio = frame.to_ndarray(format="s16", layout="mono")
#     return av.AudioFrame.from_ndarray(audio, layout="mono")


# # App configuration
# st.set_page_config(page_title="AI Interview Preparation System", layout="wide")


# # App heading
# st.markdown("<h1 style='text-align: center;'>AI Interview Preparation System</h1>", unsafe_allow_html=True)


# # Sidebar instructions and logo
# st.sidebar.image("./static/logo.png", width=120)
# st.sidebar.markdown("""
# # Instructions
# - Select a domain
# - Optionally upload resume (.pdf/.docx)
# - Select interview round and language
# - Click Generate Question
# - Type, record, or upload your answer
# - Click Evaluate!
# """)


# # Sidebar controls
# DOMAIN_LIST = ["DSA", "DBMS", "OOP", "ML", "HR", "Cloud"]
# domain = st.sidebar.selectbox("Select Domain", DOMAIN_LIST, index=0)


# LANGUAGES = ["English", "Hindi", "Odia"]
# language = st.sidebar.selectbox("Select Language", LANGUAGES, index=0)


# ROUNDS = ["Technical", "HR"]
# round_type = st.sidebar.selectbox("Select Interview Round", ROUNDS, index=0)


# resume_file = st.sidebar.file_uploader("Upload your resume (.pdf or .docx)", type=["pdf", "docx"])
# if resume_file:
#     import utils.resume_extract as rext
#     resume_text = rext.extract_resume_text(resume_file)
#     st.sidebar.success("Resume uploaded!")
#     st.sidebar.write("Resume preview:", resume_text[:300])
# else:
#     resume_text = ""


# # Session state initialization
# if "asked_questions" not in st.session_state:
#     st.session_state["asked_questions"] = {}
# if "questions" not in st.session_state:
#     st.session_state["questions"] = []
# if "answer" not in st.session_state:
#     st.session_state["answer"] = ""


# # Question generation
# if st.button("Generate Question"):
#     if resume_text:
#         questions = generate_questions_from_resume(domain, resume_text, language=language, round_type=round_type) \
#             if 'language' in generate_questions_from_resume.__code__.co_varnames else generate_questions_from_resume(domain, resume_text)
#     else:
#         questions = generate_question(domain, return_all=True) if hasattr(generate_question, "return_all") else [generate_question(domain)]
#     asked = st.session_state["asked_questions"].get(domain, set())
#     available = [q for q in questions if q not in asked]
#     if not available:
#         st.session_state["asked_questions"][domain] = set()
#         available = questions
#     question = available[0] if len(available) == 1 else st.selectbox("Choose a question", available)
#     st.session_state["question"] = question
#     st.session_state["asked_questions"].setdefault(domain, set()).add(question)
#     st.session_state["questions"] = questions
#     st.session_state["answer"] = ""  # reset answer on new question


# # Main QA UI
# if "question" in st.session_state:
#     st.subheader("Question")
#     st.write(st.session_state["question"])


#     gtts_lang_code = LANG_CODE_MAP.get(language, 'en')
#     if st.button("🔊 Listen to Question"):
#         speak_text(st.session_state["question"], lang=gtts_lang_code)


#     # Answer text area with session restore
#     answer = st.text_area("Type your answer (or paste STT):", value=st.session_state["answer"], key="input_answer")


#     # Button to listen to user's typed or transcribed answer
#     if answer:
#         if st.button("🔊 Listen to Your Answer"):
#             speak_text(answer, lang=gtts_lang_code)


#     # Live mic recording section
#     st.subheader("Or record your answer using your microphone:")
#     ctx = webrtc_streamer(
#         key="voice-answer",
#         mode=WebRtcMode.SENDRECV,  # This is correct
#         audio_frame_callback=audio_frame_callback,
#         media_stream_constraints={"audio": True, "video": False},
#     )


#     # Capture audio and transcribe via Whisper when recording stops
#     if ctx.audio_receiver:
#         audio_frames = []
#         try:
#             while True:
#                 frame = ctx.audio_receiver.get_frame(timeout=1)
#                 if frame is None:
#                     break
#                 audio_frames.append(frame)
#         except Exception:
#             pass

#         if audio_frames:
#             wav_buffer = BytesIO()
#             with wave.open(wav_buffer, 'wb') as wf:
#                 wf.setnchannels(1)
#                 wf.setsampwidth(2)  # 16-bit audio
#                 wf.setframerate(48000)
#                 for frame in audio_frames:
#                     wf.writeframes(frame.to_ndarray().tobytes())
#             wav_buffer.seek(0)

#             transcript = whisper_stt.transcribe_whisper_api(wav_buffer)
#             if transcript:
#                 st.success("Transcribed Answer (auto-filled below):")
#                 st.text_area("Type your answer (or paste STT):", value=transcript, key="answer_area")
#                 st.session_state["answer"] = transcript
#             else:
#                 st.warning("Transcription failed or empty result.")


#     # Update answer from session state (preserves transcription)
#     answer = st.session_state.get("answer", answer)


#     if st.button("Evaluate Answer") and answer.strip():
#         with st.spinner("Evaluating your answer..."):
#             feedback = evaluate_answer(st.session_state["question"], answer, language=language, round_type=round_type)
#             feedback = format_feedback(feedback)
#             st.session_state.setdefault("history", []).append({
#                 "question": st.session_state["question"],
#                 "answer": answer,
#                 "feedback": feedback,
#             })
#             st.subheader("Feedback & Score")
#             st.write(feedback)


#             if st.button("Export as PDF"):
#                 export_interview_session(st.session_state["history"])
#                 st.success("Exported to PDF!")


# # Show session history below everything
# st.markdown("---")
# st.subheader("Session History")
# show_history()




import streamlit as st
from modules.question_generator import generate_question, generate_questions_from_resume
from modules.evaluator import evaluate_answer
from modules.feedback import format_feedback
from dashboard.history import show_history
from utils.pdf_export import export_interview_session
import modules.whisper_stt as whisper_stt
from io import BytesIO
from gtts import gTTS
import tempfile
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import av
import io
import wave

# Map UI languages to gtts language codes
LANG_CODE_MAP = {'English': 'en', 'Hindi': 'hi', 'Odia': 'or'}

def speak_text(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    st.audio(mp3_fp.read(), format='audio/mp3')

def audio_frame_callback(frame):
    audio = frame.to_ndarray(format="s16", layout="mono")
    return av.AudioFrame.from_ndarray(audio, layout="mono")

# App configuration
st.set_page_config(page_title="AI Interview Preparation System", layout="wide")

# App heading
st.markdown("<h1 style='text-align: center;'>AI Interview Preparation System</h1>", unsafe_allow_html=True)

# Sidebar instructions and logo
st.sidebar.image("./static/logo.png", width=120)
st.sidebar.markdown("""
# Instructions
- Select a domain
- Optionally upload resume (.pdf/.docx)
- Select interview round and language
- Click Generate Question
- Type, record, or upload your answer
- Click Evaluate!
""")

# Sidebar controls
DOMAIN_LIST = ["DSA", "DBMS", "OOP", "ML", "HR", "Cloud"]
domain = st.sidebar.selectbox("Select Domain", DOMAIN_LIST, index=0)

LANGUAGES = ["English", "Hindi", "Odia"]
language = st.sidebar.selectbox("Select Language", LANGUAGES, index=0)

ROUNDS = ["Technical", "HR"]
round_type = st.sidebar.selectbox("Select Interview Round", ROUNDS, index=0)

resume_file = st.sidebar.file_uploader("Upload your resume (.pdf or .docx)", type=["pdf", "docx"])
if resume_file:
    import utils.resume_extract as rext
    resume_text = rext.extract_resume_text(resume_file)
    st.sidebar.success("Resume uploaded!")
    st.sidebar.write("Resume preview:", resume_text[:300])
else:
    resume_text = ""

# Session state initialization
if "asked_questions" not in st.session_state:
    st.session_state["asked_questions"] = {}
if "questions" not in st.session_state:
    st.session_state["questions"] = []
if "answer_stt" not in st.session_state:
    st.session_state["answer_stt"] = ""

# Question generation
if st.button("Generate Question"):
    if resume_text:
        questions = generate_questions_from_resume(domain, resume_text, language=language, round_type=round_type) \
            if 'language' in generate_questions_from_resume.__code__.co_varnames else generate_questions_from_resume(domain, resume_text)
    else:
        questions = generate_question(domain, return_all=True) if hasattr(generate_question, "return_all") else [generate_question(domain)]
    asked = st.session_state["asked_questions"].get(domain, set())
    available = [q for q in questions if q not in asked]
    if not available:
        st.session_state["asked_questions"][domain] = set()
        available = questions
    question = available[0] if len(available) == 1 else st.selectbox("Choose a question", available)
    st.session_state["question"] = question
    st.session_state["asked_questions"].setdefault(domain, set()).add(question)
    st.session_state["questions"] = questions
    st.session_state["answer_stt"] = ""  # reset STT answer on new question

if "question" in st.session_state:
    st.subheader("Question")
    st.write(st.session_state["question"])

    gtts_lang_code = LANG_CODE_MAP.get(language, 'en')
    if st.button("🔊 Listen to Question"):
        speak_text(st.session_state["question"], lang=gtts_lang_code)

    # Get typed answer, default from STT if present
    typed_answer = st.text_area(
        "Type your answer (or paste STT):",
        value=st.session_state.get("answer_stt", ""),
        key="typed_answer"
    )

    # TTS for user's answer
    if typed_answer:
        if st.button("🔊 Listen to Your Answer"):
            speak_text(typed_answer, lang=gtts_lang_code)

    # Microphone recorder via streamlit-webrtc
    st.subheader("Or record your answer using your microphone:")
    ctx = webrtc_streamer(
        key="voice-answer",
        mode=WebRtcMode.SENDRECV,
        audio_frame_callback=audio_frame_callback,
        media_stream_constraints={"audio": True, "video": False},
    )

    if ctx.audio_receiver:
        audio_frames = []
        try:
            while True:
                frame = ctx.audio_receiver.get_frame(timeout=1)
                if frame is None:
                    break
                audio_frames.append(frame)
        except Exception:
            pass

        if audio_frames:
            wav_buffer = BytesIO()
            with wave.open(wav_buffer, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)  # 16-bit samples
                wf.setframerate(48000)
                for frame in audio_frames:
                    wf.writeframes(frame.to_ndarray().tobytes())
            wav_buffer.seek(0)

            transcript = whisper_stt.transcribe_whisper_api(wav_buffer)
            if transcript:
                st.session_state["answer_stt"] = transcript
                st.success("Transcribed Answer (auto-filled below):")
                # Force refresh typed_answer box with latest transcript
                typed_answer = st.text_area(
                    "Type your answer (or paste STT):",
                    value=transcript,
                    key="typed_answer",
                    on_change=None
                )
            else:
                st.warning("Transcription failed or empty result.")

    # Evaluate using latest answer in typed_answer box
    if st.button("Evaluate Answer"):
        currently_typed = st.session_state.get("typed_answer", "").strip()
        if not currently_typed:
            st.warning("Please provide your answer before evaluation.")
        else:
            with st.spinner("Evaluating your answer..."):
                feedback = evaluate_answer(st.session_state["question"], currently_typed, language=language, round_type=round_type)
                feedback = format_feedback(feedback)
                st.session_state.setdefault("history", []).append({
                    "question": st.session_state["question"],
                    "answer": currently_typed,
                    "feedback": feedback,
                })
                st.subheader("Feedback & Score")
                st.write(feedback)

            if st.button("Export as PDF"):
                export_interview_session(st.session_state["history"])
                st.success("Exported to PDF!")

st.markdown("---")
st.subheader("Session History")
show_history()
