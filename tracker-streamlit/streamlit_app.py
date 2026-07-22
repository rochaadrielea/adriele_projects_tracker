"""
Contribution & Impact Tracker — Streamlit wrapper.

To open it, a person types their name once (no password). The name is stored in
a browser cookie, so on this device they stay signed in and skip the prompt next
time. Their name is passed into the tracker so update notes are auto-signed.

To restrict WHO can open the app at all, set the app to private in
Streamlit Cloud → Settings → Sharing and invite people by email.
"""
import json
import pathlib
from datetime import datetime, timedelta

import streamlit as st
import streamlit.components.v1 as components
import extra_streamlit_components as stx

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

COOKIE = "tracker_user"

# One cookie manager for the whole app.
cookies = stx.CookieManager(key="cookie_mgr")

# If a cookie exists from a previous visit, sign in automatically.
saved_name = cookies.get(COOKIE)
if not st.session_state.get("auth_user") and saved_name:
    st.session_state["auth_user"] = saved_name

# ---- login gate (name only, remembered by cookie) ----
if not st.session_state.get("auth_user"):
    st.markdown("## 📊 Contribution & Impact Tracker")
    st.caption("Enter your name once — this device will remember you next time.")
    with st.form("login_form"):
        name = st.text_input("Your name").strip()
        submitted = st.form_submit_button("Open tracker")
    if submitted and name:
        st.session_state["auth_user"] = name
        cookies.set(COOKIE, name, expires_at=datetime.now() + timedelta(days=365))
    if not st.session_state.get("auth_user"):
        if submitted and not name:
            st.error("Please type your name.")
        st.stop()

user = st.session_state["auth_user"]

with st.sidebar:
    st.write(f"Signed in as **{user}**")
    if st.button("Log out (forget me)"):
        cookies.delete(COOKIE)
        st.session_state.pop("auth_user", None)
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
html = html[:_i] + inject + html[_i:] if _i != -1 else html + inject

components.html(html, height=2600, scrolling=True)
