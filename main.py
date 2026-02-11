import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Villen Manager Pro", layout="wide")

# Login (admin123)
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔐 Login")
    if st.text_input("Passwort", type="password") == "admin123":
        if st.button("Anmelden"):
            st.session_state.auth = True
            st.rerun()
    st.stop()

# Verbindung
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(ttl=0)

st.title("🏛️ Villen Manager Pro")
t1, t2, t3 = st.tabs(["📋 Liste", "➕ Neu", "📸 Kamera"])

with t1:
    if df is not None:
        st.dataframe(df, use_container_width=True, hide_index=True)

with t2:
    with st.form("neu"):
        gast = st.text_input("Gast Name")
        preis = st.number_input("Preis", min_value=0)
        if st.form_submit_button("Speichern"):
            new = pd.DataFrame([{"Gast": gast, "Preis": preis}])
            conn.update(data=pd.concat([df, new], ignore_index=True))
            st.success("Gespeichert!")
            st.rerun()

with t3:
    st.file_uploader("Kamera öffnen", type=['jpg', 'png'])
