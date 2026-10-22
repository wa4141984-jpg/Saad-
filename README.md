# Saad-# AI Study Assistant

A beginner-friendly chatbot for students, built with Python and Streamlit. Ask questions, paste notes,
or upload files (PDF, DOCX, TXT, MD, CSV, PNG, JPG), then choose a mode: **Explain**, **Quiz me**,
**Summarize** or **Flashcards**. Answers stream in live. It uses the Anthropic (Claude) API.

## Files
| File | Purpose |
|---|---|
| `app.py` | The Streamlit interface |
| `ai_client.py` | API key loading, prompts, API calls, error messages |
| `file_utils.py` | File validation and text extraction |
| `requirements.txt` | Python dependencies |
| `.env.example` | Template for your key (copy to `.env`) |
| `.streamlit/secrets.toml.example` | Template for Streamlit secrets |

## 1. Get an API key
1. Create an account at https://console.anthropic.com.
2. Add billing or credits (the API is pay-as-you-go).
3. Open **API Keys** → **Create Key**, and copy it. You see it only once.

## 2. Install
Requires Python 3.9+.
```bash
cd ai-study-assistant
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 3. Configure the key
```bash
cp .env.example .env            # Windows: copy .env.example .env
```
Open `.env` and replace `your-api-key-here` with your key. `.env` is in `.gitignore`, so it won't be uploaded to GitHub.
Alternatively, copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and fill it in.

## 4. Run
```bash
streamlit run app.py
```
Open http://localhost:8501.

## 5. Deploy (Streamlit Community Cloud, free)
1. Push this folder to a GitHub repository (confirm `.env` is NOT included).
2. Go to https://share.streamlit.io → **New app**, select the repo and `app.py`.
3. Open **Advanced settings → Secrets** and paste:
   ```toml
   ANTHROPIC_API_KEY = "your-real-key"
   ```
4. Click **Deploy**. Other hosts (Render, Railway, Hugging Face Spaces) work too: set `ANTHROPIC_API_KEY`
   as an environment variable and use the start command
   `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`.

## Limitations
- **Not a source of truth.** AI can be wrong; check important facts against your textbook.
- **Limits:** 3 files, 5 MB each; about 40,000 characters of file text are used; messages max 4,000 characters; the last 20 messages are remembered.
- **Scanned PDFs** have no text and are rejected. Upload a clear photo (PNG/JPG) of the page instead.
- **Images** apply only to the next question you send (they are not remembered afterwards).
- **No login and no saved history:** the chat disappears when you refresh. Use **Download chat** to keep it.
- **Cost:** every message uses your API credits. The app has no per-user usage cap, so don't share a public deployment widely without adding one.
- **Model:** defaults to `claude-sonnet-5-5`; change it with `ANTHROPIC_MODEL` if your account uses another.

## Troubleshooting
- *"No API key found"* → check `.env` is in the same folder as `app.py`, then restart.
- *"API key was rejected"* → recreate the key and make sure there are no spaces or quotes around it in `.env`.
- *"Model not found"* → set `ANTHROPIC_MODEL` to a model listed in your Anthropic console.
