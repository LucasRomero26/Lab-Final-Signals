import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


st.markdown("<h1 style='text-align: center; color: white;'>Final Laboratory</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: white;'>Series and Fourier Transform</h3>", unsafe_allow_html=True)


import streamlit as st

# Custom CSS for more attractive buttons
st.markdown("""
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #45a049;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
    }
    </style>
""", unsafe_allow_html=True)

col11, col22, col33 = st.columns(3)

# Colocar el GIF en la columna central
with col22:
    st.image("https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExcXdrbm45cXo1OG1tb3RiajUyd2swa20xbHlyMjY1OXcxc3IweXV4cSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/Su24EeLFHWH8ob1luY/giphy.gif")


# Create a row with two columns to place buttons side by side
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.page_link("app.py", label="Home", use_container_width=True)

with col2:
    st.page_link("pages/punto1.py", label="Series Examples", use_container_width=True)

with col3:
    st.page_link("pages/punto2.py", label="Signal Mod", use_container_width=True)

with col4:
    st.page_link("pages/punto3.py", label="Amplitude Mod", use_container_width=True)
with col5:
    st.page_link("pages/punto4.py", label="DSB-LC", use_container_width=True)
