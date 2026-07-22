"""
Contribution & Impact Tracker — Streamlit wrapper.

Serves the self-contained tracker (tracker.html). To open it, a person just
types their name (no password). Their name is passed into the tracker so their
update notes are signed automatically.

To restrict WHO can open the app at all, set the app to private in
Streamlit Cloud → Settings → Sharing and invite people by email.
"""
import json
import pathlib
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Contribution & Impact Tracker",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
      #MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
      .block-container {padding-top: 1rem; padding-bottom: 0; max-width: 100% !important;}
    </style>
    """,
    unsafe_allow_html=True,
)


def login_gate():
    if st.session_state.get("auth_user"):
        return True
    st.markdown("## 📊 Contribution & Impact Tracker")
    st.caption("Enter your name to open the tracker — your update notes will be signed with it.")
    with st.form("login_form"):
        name = st.text_input("Your name").strip()
        submitted = st.form_submit_button("Open tracker")
    if submitted:
        if name:
            st.session_state["auth_user"] = name
            st.rerun()
        else:
            st.error("Please type your name.")
    return False


if not login_gate():
    st.stop()

user = st.session_state["auth_user"]

with st.sidebar:
    st.write(f"Signed in as **{user}**")
    if st.button("Log out"):
        del st.session_state["auth_user"]
        st.rerun()

# Load the tracker and inject the signed-in name so update notes are auto-signed.
html = pathlib.Path(__file__).with_name("tracker.html").read_text(encoding="utf-8")
inject = (
    "<script>window.addEventListener('load',function(){"
    "var w=document.getElementById('whoami');"
    "if(w){w.value=" + json.dumps(user) + ";w.dispatchEvent(new Event('input'));}"
    "});</script>"
)
_i = html.rfind("</body>")
if _i != -1:
    html = html[:_i] + inject + html[_i:]
else:
    html = html + inject

components.html(html, height=2600, scrolling=True)
