import streamlit as st

def render_toggle_buttons():
    st.session_state["region_time"] = st.toggle("Show Region Time", value=st.session_state.get("region_time", False))

    if st.session_state["region_time"]:
        st.markdown("<p style='color: #00E7D5; text-align: center; font-weight: bold;'>Region Time is Active</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='color: #AAAAAA; text-align: center; font-weight: bold;'>UTC is Active</p>", unsafe_allow_html=True)

    return st.session_state["region_time"]