# AI Study Assistant

A beginner-friendly study chatbot built with Python and Streamlit, using the Anthropic (Claude) API.
Ask questions, paste notes, or upload files (PDF, DOCX, TXT, MD, CSV, PNG, JPG), then pick a mode:
Explain, Quiz me, Summarize or Flashcards. Answers stream in live.

## Files (all in ONE folder)
| File | Purpose |
|---|---|
| `app.py` | The whole app (settings, file reading, AI calls, interface) |
| `requirements.txt` | Python dependencies. Must sit next to `app.py` |
| `.env.example` | Template for your key (copy to `.env`) |
| `.streamlit/secrets.toml.example` | Template for Streamlit secrets |
| `.gitignore` | Keeps `.env` and secrets out of Git |

## 1. Get an API key
1. Create an account at https://console.anthropic.com.
2. Add credits or billing (pay-as-you-go).
3. Open **API Keys** > **Create Key** and copy it. It is shown only once.

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
Open `.env` and replace `your-api-key-here` with your key. No spaces or quotes.
Alternative: copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and fill it in.

## 4. Run
```bash
streamlit run app.py
```
Open http://localhost:8501.

## 5. Deploy on Streamlit Community Cloud (free)
1. Upload the **contents** of this folder to the **root** of a GitHub repo, so `app.py` and
   `requirements.txt` are side by side. Do NOT upload `.env`.
2. Go to https://share.streamlit.io > **New app**, choose the repo, branch and `app.py`.
3. Open **Advanced settings > Secrets** and paste:
   ```toml
   ANTHROPIC_API_KEY = "your-real-key"
   ```
4. Click **Deploy**. After changing files or secrets, use **Manage app > Reboot**.

Other hosts (Render, Railway, Hugging Face Spaces): set `ANTHROPIC_API_KEY` as an environment variable and run
`streamlit run app.py --server.port $PORT --server.address 0.0.0.0`.

## Limitations
- AI can be wrong. Check important facts against your textbook.
- Limits: 3 files of 5 MB each, about 40,000 characters of file text, messages up to 4,000 characters, last 20 messages remembered.
- Scanned PDFs have no text and are rejected. Upload a clear photo (PNG/JPG) instead.
- Images apply only to the next question you send.
- No login or saved history: refreshing clears the chat. Use **Download chat** to keep it.
- Every message uses your API credits and there is no per-user cap, so don't share a public deployment widely.
- Default model is `claude-sonnet-5-5`. Set `ANTHROPIC_MODEL` if your account uses another.

## Troubleshooting
- **ModuleNotFoundError**: a file or package is missing. Check that `app.py` and `requirements.txt` are in the same folder
  (the repo root on Streamlit Cloud), then reboot.
- **No API key found**: check `.env` (or Secrets) and restart.
- **API key was rejected**: create a new key and paste it again.
- **Model not found**: set `ANTHROPIC_MODEL` to a model listed in your Anthropic console.
