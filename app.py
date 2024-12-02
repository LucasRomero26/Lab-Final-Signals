import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


st.markdown("<h1 style='text-align: center; color: white;'>Laboratorio Final</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: white;'>Series y Transformada de Fourier</h3>", unsafe_allow_html=True)



expander = st.expander("Opciones")
expander.write('''
    The chart above shows some numbers I picked for you.
    I rolled actual dice for these, so they're *guaranteed* to
    be random.
''')
expander.image("https://static.streamlit.io/examples/dice.jpg")