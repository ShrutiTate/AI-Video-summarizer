# app.py 
import streamlit as st 
import os
import fitz  # PyMuPDF
import random
from utils.youtube import fetch_youtube_transcript
from utils.gemini import generate_summary, generate_flashcards
from utils.report import generate_pdf
from utils.sentiment import analyze_sentiment
from utils.keywords import extract_keywords
import streamlit.components.v1 as components
import google.generativeai as genai

# Streamlit config
st.set_page_config(page_title="🎯 AI Video Learning Companion", layout="wide")

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    topic_model = genai.GenerativeModel("gemini-1.5-flash")
else:
    topic_model = None

# Initialize session state
for key in ["transcript", "summary", "flashcards", "show_transcript", "detected_topic"]:
    if key not in st.session_state:
        st.session_state[key] = None if key != "show_transcript" else False

# Sidebar input method
st.sidebar.title("🎓 Select Input Method")
input_type = st.sidebar.radio("", ["YouTube URL", "Upload File"])

# Title
st.markdown("<h1 style='text-align:center; color:#4B8BBE;'>🎯 AI Video Learning Companion</h1>", unsafe_allow_html=True)
st.markdown("---")

# Input handling
if input_type == "YouTube URL":
    youtube_url = st.text_input("🎥 Enter YouTube Video URL:")
    if youtube_url:
        try:
            transcript = fetch_youtube_transcript(youtube_url)
            st.session_state.transcript = transcript
            st.session_state.summary = None
            st.session_state.flashcards = None
            st.session_state.detected_topic = None
            st.success("✅ Transcript fetched successfully!")
        except Exception as e:
            st.error(f"❌ Error fetching transcript: {e}")

elif input_type == "Upload File":
    uploaded_file = st.file_uploader("📄 Upload a transcript file (.txt or .pdf)")
    if uploaded_file:
        try:
            file_name = uploaded_file.name.lower()
            if file_name.endswith(".txt"):
                content = uploaded_file.read().decode("utf-8")
            elif file_name.endswith(".pdf"):
                with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
                    content = "\n".join([page.get_text() for page in doc])
            else:
                st.warning("⚠️ Please upload only a .txt or .pdf file.")
                content = ""

            if content:
                st.session_state.transcript = content
                st.session_state.summary = None
                st.session_state.flashcards = None
                st.session_state.detected_topic = None
                st.success("✅ File uploaded and transcript extracted.")
        except Exception as e:
            st.error(f"❌ Error reading file: {e}")

# Transcript viewer
if st.button("🎹 Show Transcript") and st.session_state.transcript:
    st.session_state.show_transcript = not st.session_state.show_transcript

if st.session_state.show_transcript:
    st.markdown("### 📜 Transcript")
    st.text_area("Transcript", st.session_state.transcript, height=300)


# Generate Summary & Flashcards
if st.session_state.transcript and not st.session_state.summary:
    with st.spinner("⏳ Analyzing transcript..."):
        st.session_state.summary = generate_summary(st.session_state.transcript)
        st.session_state.flashcards = generate_flashcards(st.session_state.transcript)

# Summary
summary = st.session_state.summary
if summary:
    st.subheader("🗞 Summary")
    if isinstance(summary, dict):
        st.markdown(summary.get("summary_text", "⚠️ No summary available."))
    else:
        st.error(summary)

# Flashcards
flashcards = st.session_state.flashcards
if flashcards:
    st.subheader("📚 Flashcards")
    for i, card in enumerate(flashcards.get("flashcards", [])):
        if isinstance(card, dict) and "question" in card and "answer" in card:
            html = f"""
            <style>
                .click-card {{width: 100%;max-width: 800px;margin: 0 auto 20px auto; min-height: 200px;}}
                .click-card {{ background-color: transparent; width: 100%; height: 200px; perspective: 1000px; margin-bottom: 20px; cursor: pointer; }}
                .click-card-inner {{ position: relative; width: 100%; height: 100%; transition: transform 0.6s; transform-style: preserve-3d; }}
                .click-card.flipped .click-card-inner {{ transform: rotateY(180deg); }}
                .click-card-front, .click-card-back {{
                    position: absolute; width: 100%; height: 100%;
                    -webkit-backface-visibility: hidden; backface-visibility: hidden;
                    border-radius: 12px; padding: 20px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
                    display: flex; flex-direction: column; justify-content: center; align-items: center;
                    font-family: 'Segoe UI', sans-serif;
                }}
                .click-card-front {{ background: linear-gradient(135deg, #EDE7F6, #D1C4E9); color: #444; }}
                .click-card-back {{background: linear-gradient(135deg, #F3E5F5, #CE93D8);
                color: #000;
                transform: rotateY(180deg);
                overflow-y: auto;
                word-wrap: break-word;
                text-align: justify;
                padding: 15px;
                font-size: 16px;
                line-height: 1.4;
                max-height: 180px;
                }}
            </style>
            <script>
                function toggleFlip_{i}() {{
                    var card = document.getElementById("card-{i}");
                    card.classList.toggle("flipped");
                }}
            </script>
            <div id="card-{i}" class="click-card" onclick="toggleFlip_{i}()">
                <div class="click-card-inner">
                    <div class="click-card-front">
                        <h4>📘 Q{i+1}</h4>
                        <p>{card['question']}</p>
                    </div>
                    <div class="click-card-back">
                        <h4>✅ Answer</h4>
                        <p>{card['answer']}</p>
                    </div>
                </div>
            </div>
            """
            components.html(html, height=220)
    # Keywords and Sentiment
    if st.session_state.transcript:
        if 'keywords' not in st.session_state:
            st.session_state.keywords = extract_keywords(st.session_state.transcript)
        if 'sentiment' not in st.session_state:
            st.session_state.sentiment = analyze_sentiment(st.session_state.transcript)

        if st.session_state.keywords:
            st.subheader("🔑 Keywords")
            st.write(", ".join(st.session_state.keywords))

        if st.session_state.sentiment:
            st.subheader("🧠 Sentiment Analysis")
            st.write(f"Overall tone: {st.session_state.sentiment}")

# PDF Report Download
if summary and flashcards:
    if st.button("📥 Download PDF Report"):
        with st.spinner("Generating report..."):
            sentiment = analyze_sentiment(st.session_state.transcript)
            keywords = extract_keywords(st.session_state.transcript)
            st.write("🧪 Summary text:", summary.get('summary_text'))
            st.write("🧪 Keywords:", keywords)
            st.write("🧪 Sentiment:", sentiment)
            st.write("🧪 Flashcards:", flashcards.get('flashcards'))

            pdf_bytes = generate_pdf(summary['summary_text'], keywords, sentiment, flashcards['flashcards'])
                
            st.download_button(
                label="⬇️ Click to download",
                data=pdf_bytes,
                file_name="learning_report.pdf",
                mime="application/pdf"
            )
