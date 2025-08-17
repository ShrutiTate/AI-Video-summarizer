
# 🎯 AI Video Learning Companion

An AI-powered web app that transforms educational videos into interactive learning materials. Users can input a YouTube URL or upload a transcript file, and the app will generate:

- Summaries of the content  
- Flashcards for active recall  
- Keywords for topic understanding  
- Sentiment analysis  
- PDF report download  

Built with **Streamlit**, **Google Gemini API**, and **Python**.

---

## 🚀 Features

- **YouTube Transcript Fetching**: Automatically fetches video transcripts.  
- **File Upload Support**: Upload `.txt` or `.pdf` transcripts for analysis.  
- **Summary Generation**: Generates concise summaries of the transcript.  
- **Interactive Flashcards**: Flip cards for Q&A learning.  
- **Keyword Extraction**: Highlights key topics from the transcript.  
- **Sentiment Analysis**: Provides an overall tone of the transcript.  
- **PDF Report**: Download a full report with summary, flashcards, keywords, and sentiment.  

---

## 🛠 Tech Stack

- **Frontend & Web App**: [Streamlit](https://streamlit.io/)  
- **AI & NLP**: [Google Gemini API](https://developers.generativeai.google/), Custom Python NLP functions  
- **PDF Generation**: PyMuPDF (fitz)  
- **Video Transcript**: YouTube transcript fetching  

---

## ⚡ Installation

1. Clone the repository:

```bash
git clone https://github.com/<your-username>/ai-video-learning-companion.git
cd ai-video-learning-companion
````

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set your **Gemini API key** in a `.env` file:

```
GEMINI_API_KEY=your_api_key_here
```

5. Run the app:

```bash
streamlit run app.py
```

---

## 📝 Usage

1. Select **input method** from the sidebar (`YouTube URL` or `Upload File`).
2. Enter the video URL or upload a transcript file.
3. View transcript, summary, and interactive flashcards.
4. Extract keywords and check sentiment.
5. Download the complete learning PDF report.

## 🔒 Security

* Keep your **Gemini API key** private.
* Add `.env` to `.gitignore` to prevent exposing secrets on GitHub.


## 💡 Future Improvements

* Support multiple languages.
* Integrate video playback with live transcript highlights.
* Add spaced repetition scheduling for flashcards.

---

## 📄 License

This project is licensed under the MIT License.

```

I can also create a **ready-to-paste `requirements.txt`** for this project so anyone can install dependencies quickly.  

Do you want me to do that?
```
