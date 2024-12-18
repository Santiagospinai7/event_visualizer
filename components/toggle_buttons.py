import streamlit as st

def render_toggle_buttons():
    col1, col2 = st.columns(2)
    with col1:
        if st.button("UTC", key="utc_button"):
            st.session_state["region_time"] = False
    with col2:
        if st.button("Region Time", key="region_button"):
            st.session_state["region_time"] = True
    return st.session_state["region_time"]