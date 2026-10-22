"""AI Study Assistant: Streamlit user interface."""
import streamlit as st

from ai_client import MODES, AIError, get_api_key, stream_reply
from file_utils import ALLOWED_TYPES, MAX_FILE_MB, MAX_FILES, FileError, build_context, parse_file

MAX_MESSAGE_CHARS = 4000
MAX_HISTORY = 20  # messages sent to the AI per request

st.set_page_config(page_title="AI Study Assistant", page_icon="📘", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@600;700&family=Inter:wght@400;500&display=swap');
:root { --ink:#14213d; --teal:#0f766e; --mist:#eef3f6; }
html, body, [class*="css"] { font-family:'Inter',sans-serif; }
h1, h2, h3 { font-family:'Source Serif 4',serif; color:var(--ink); }
[data-testid="stSidebar"] { background:var(--mist); }
[data-testid="stChatMessage"] { border-radius:14px; }
.stButton > button { border-radius:10px; border:1px solid var(--teal); color:var(--teal); }
.stButton > button:hover { background:var(--teal); color:#fff; }
.block-container { max-width:860px; padding-top:2rem; }
@media (max-width:640px) { .block-container { padding:1rem .75rem; } }
</style>
""", unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def read_upload(name: str, data: bytes):
    return parse_file(name, data)


if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- Sidebar ----------
with st.sidebar:
    st.header("Study setup")
    mode = st.selectbox("How should I help?", list(MODES))
    uploads = st.file_uploader(
        f"Add notes or images (up to {MAX_FILES} files, {MAX_FILE_MB} MB each)",
        type=ALLOWED_TYPES, accept_multiple_files=True)

    files = []
    if uploads and len(uploads) > MAX_FILES:
        st.error(f"Please keep it to {MAX_FILES} files. Only the first {MAX_FILES} are used.")
        uploads = uploads[:MAX_FILES]
    for up in uploads or []:
        try:
            files.append(read_upload(up.name, up.getvalue()))
        except FileError as e:
            st.error(str(e))
    if files:
        st.success(f"{len(files)} file(s) ready")
        if build_context(files)[1]:
            st.warning("Your files are long, so only the first part is used.")

    if st.session_state.messages:
        transcript = "\n\n".join(f"**{m['role'].title()}:** {m['content']}" for m in st.session_state.messages)
        st.download_button("Download chat", transcript, "study-chat.md", use_container_width=True)
        if st.button("Clear chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

# ---------- Main ----------
st.title("AI Study Assistant")
st.caption("Ask a question, paste your notes, or upload a file. Pick a mode in the sidebar.")

if not get_api_key():
    st.error("No API key found. Add `ANTHROPIC_API_KEY` to `.env` or Streamlit secrets, then restart.")

if not st.session_state.messages:
    st.info("Try: *Explain photosynthesis simply*, or upload your lecture notes and choose **Quiz me**.")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

prompt = st.chat_input("Type your question…")
if prompt is not None:
    prompt = prompt.strip()
    if not prompt:
        st.warning("Type a question before sending.")
    elif len(prompt) > MAX_MESSAGE_CHARS:
        st.warning(f"That message is {len(prompt):,} characters. Keep it under {MAX_MESSAGE_CHARS:,}, "
                   "or upload long text as a file.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            try:
                with st.spinner("Thinking…"):
                    reply = st.write_stream(
                        stream_reply(st.session_state.messages[-MAX_HISTORY:], files, mode))
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except AIError as e:
                st.error(str(e))
                st.session_state.messages.pop()  # let the user resend
            except Exception:
                st.error("Something unexpected went wrong. Please try again.")
                st.session_state.messages.pop()
