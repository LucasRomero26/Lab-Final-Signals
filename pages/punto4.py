import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.markdown("<h1 style='text-align: center; color: white;'>Amplitude Modulation</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: white;'>DSB-LC in Python</h3>", unsafe_allow_html=True)

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

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def main():
    st.title("Signal Processing and Modulation Visualization")
    
    # Sidebar for input parameters
    st.sidebar.header("Signal Parameters")
    
    # Input for the three signals
    with st.sidebar.expander("Signal 1"):
        f1 = st.number_input("Frequency of Signal 1 (Hz)", value=100.0, key="f1")
        A1 = st.number_input("Amplitude of Signal 1", value=1.0, key="a1")
    
    with st.sidebar.expander("Signal 2"):
        f2 = st.number_input("Frequency of Signal 2 (Hz)", value=200.0, key="f2")
        A2 = st.number_input("Amplitude of Signal 2", value=0.5, key="a2")
    
    with st.sidebar.expander("Signal 3"):
        f3 = st.number_input("Frequency of Signal 3 (Hz)", value=300.0, key="f3")
        A3 = st.number_input("Amplitude of Signal 3", value=0.3, key="a3")
    
    # Sampling parameters
    fs = 100000  # Sampling frequency (Hz)
    t = np.linspace(0, 0.015, int(fs * 0.015), endpoint=False)
    
    # Generate signals
    y1 = A1 * np.sin(2 * np.pi * f1 * t)
    y2 = A2 * np.sin(2 * np.pi * f2 * t)
    y3 = A3 * np.sin(2 * np.pi * f3 * t)
    y_t = y1 + y2 + y3
    
    # Plot individual signals
    st.header("Individual Signals and Composite Signal")
    fig, ax = plt.subplots(4, 1, figsize=(12, 15))
    plt.style.use("dark_background")
    fig.patch.set_alpha(0.0)
    
    for a in ax:
        a.patch.set_alpha(0.0)
    
    # Signal 1
    ax[0].plot(t, y1)
    ax[0].set_title(f"Signal 1: Frequency = {f1} Hz, Amplitude = {A1}", fontsize=14)
    ax[0].set_xlabel("Time (s)", fontsize=12)
    ax[0].set_ylabel("Amplitude", fontsize=12)
    ax[0].grid(True)
    
    # Signal 2
    ax[1].plot(t, y2)
    ax[1].set_title(f"Signal 2: Frequency = {f2} Hz, Amplitude = {A2}", fontsize=14)
    ax[1].set_xlabel("Time (s)", fontsize=12)
    ax[1].set_ylabel("Amplitude", fontsize=12)
    ax[1].grid(True)
    
    # Signal 3
    ax[2].plot(t, y3)
    ax[2].set_title(f"Signal 3: Frequency = {f3} Hz, Amplitude = {A3}", fontsize=14)
    ax[2].set_xlabel("Time (s)", fontsize=12)
    ax[2].set_ylabel("Amplitude", fontsize=12)
    ax[2].grid(True)
    
    # Composite signal
    ax[3].plot(t, y_t)
    ax[3].set_title("Composite Signal y(t)", fontsize=14)
    ax[3].set_xlabel("Time (s)", fontsize=12)
    ax[3].set_ylabel("Amplitude", fontsize=12)
    ax[3].grid(True)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # Carrier signal and modulation
    st.header("Signal Modulation Analysis")
    
    # Carrier signal parameters
    A_p = 1  # Carrier amplitude
    f0 = 3000  # Carrier frequency (Hz)
    p_t = A_p * np.cos(2 * np.pi * f0 * t)  # Carrier signal
    y_mod = y_t * p_t  # Amplitude modulation (DSB-SC)
    
    # Frequency domain analysis
    w = np.linspace(-len(y_mod)/2, len(y_mod)/2, len(y_mod))
    
    # Calculate FFTs
    y_w = np.fft.fftshift(np.abs(np.fft.fft(y_t)))
    y_w_norm = y_w / np.max(y_w)
    
    p_t_w = np.fft.fftshift(np.abs(np.fft.fft(p_t)))
    p_t_w_norm = p_t_w / np.max(p_t_w)
    
    y_mod_w = np.fft.fftshift(np.abs(np.fft.fft(y_mod)))
    y_mod_w_norm = y_mod_w / np.max(y_mod_w)
    
    # Plot modulation results
    fig2, ax2 = plt.subplots(3, 2, figsize=(15, 15))
    fig2.patch.set_alpha(0.0)
    
    for row in ax2:
        for a in row:
            a.patch.set_alpha(0.0)
    
    # Modulating signal
    ax2[0,0].plot(t, y_t)
    ax2[0,0].set_title("Modulating Signal", fontsize=14)
    ax2[0,0].set_xlabel("Time (s)", fontsize=12)
    ax2[0,0].set_ylabel("Amplitude", fontsize=12)
    ax2[0,0].grid(True)
    
    # Modulating signal spectrum
    ax2[0,1].plot(w, y_w_norm)
    ax2[0,1].set_title("Modulating Signal Spectrum", fontsize=14)
    ax2[0,1].set_xlabel("Frequency (Hz)", fontsize=12)
    ax2[0,1].set_ylabel("Normalized Amplitude", fontsize=12)
    ax2[0,1].grid(True)
    
    # Carrier signal
    ax2[1,0].plot(t, p_t, color='orange')
    ax2[1,0].set_title("Carrier Signal", fontsize=14)
    ax2[1,0].set_xlabel("Time (s)", fontsize=12)
    ax2[1,0].set_ylabel("Amplitude", fontsize=12)
    ax2[1,0].grid(True)
    
    # Carrier signal spectrum
    ax2[1,1].plot(w, p_t_w_norm, color='orange')
    ax2[1,1].set_title("Carrier Signal Spectrum", fontsize=14)
    ax2[1,1].set_xlabel("Frequency (Hz)", fontsize=12)
    ax2[1,1].set_ylabel("Normalized Amplitude", fontsize=12)
    ax2[1,1].grid(True)
    
    # Modulated signal
    ax2[2,0].plot(t, y_mod, color='green')
    ax2[2,0].set_title("DSB-SC Modulated Signal", fontsize=14)
    ax2[2,0].set_xlabel("Time (s)", fontsize=12)
    ax2[2,0].set_ylabel("Amplitude", fontsize=12)
    ax2[2,0].grid(True)
    
    # Modulated signal spectrum
    ax2[2,1].plot(w, y_mod_w_norm, color='green')
    ax2[2,1].set_title("DSB-SC Modulated Signal Spectrum", fontsize=14)
    ax2[2,1].set_xlabel("Frequency (Hz)", fontsize=12)
    ax2[2,1].set_ylabel("Normalized Amplitude", fontsize=12)
    ax2[2,1].grid(True)
    
    plt.tight_layout()
    st.pyplot(fig2)
    
    # Primera sección de índices de modulación
    st.header("DSB-LC Modulation Analysis")
    
    # Índices de modulación fijos para la primera sección
    mu_fixed = [1.2, 1.0, 0.7]
    
    # Crear figura para el primer conjunto de gráficas DSB-LC
    fig3, ax3 = plt.subplots(len(mu_fixed), 2, figsize=(15, 5*len(mu_fixed)))
    fig3.patch.set_alpha(0.0)
    
    for a in ax3.flat:
        a.patch.set_alpha(0.0)
    
    a_m = np.max(np.abs(y_t))
    
    for i, m in enumerate(mu_fixed):
        A_p = a_m / m
        y_mod = (A_p + y_t) * np.cos(2*np.pi*f0*t)
        
        # FFT de la señal modulada
        y_mod_w = np.fft.fftshift(np.abs(np.fft.fft(y_mod)))
        y_mod_w_norm = y_mod_w / np.max(y_mod_w)
        
        # Señal modulada
        ax3[i,0].plot(t, y_mod, color='green')
        ax3[i,0].set_title(f"DSB-LC Modulated Signal (μ = {m})", fontsize=14)
        ax3[i,0].set_xlabel("Time (s)", fontsize=12)
        ax3[i,0].set_ylabel("Amplitude", fontsize=12)
        ax3[i,0].grid(True)
        
        # Espectro de la señal modulada
        ax3[i,1].plot(w, y_mod_w_norm, color='red')
        ax3[i,1].set_title(f"DSB-LC Modulated Signal Spectrum (μ = {m})", fontsize=14)
        ax3[i,1].set_xlabel("Frequency (Hz)", fontsize=12)
        ax3[i,1].set_ylabel("Normalized Amplitude", fontsize=12)
        ax3[i,1].grid(True)
    
    plt.tight_layout()
    st.pyplot(fig3)
    
    # Segunda sección de índices de modulación con señales rectificadas
    st.header("DSB-LC Modulation Analysis with Signal Rectification")
    
    # Crear figura para las señales rectificadas
    fig4, ax4 = plt.subplots(len(mu_fixed), 2, figsize=(15, 5*len(mu_fixed)))
    fig4.patch.set_alpha(0.0)
    
    for a in ax4.flat:
        a.patch.set_alpha(0.0)
    
    for i, m in enumerate(mu_fixed):
        A_p = a_m / m
        y_mod = (A_p + y_t) * np.cos(2*np.pi*f0*t)
        y_mod_rect = np.abs(y_mod)
        
        # Señal modulada
        ax4[i,0].plot(t, y_mod, color='green')
        ax4[i,0].set_title(f"DSB-LC Modulated Signal (μ = {m})", fontsize=14)
        ax4[i,0].set_xlabel("Time (s)", fontsize=12)
        ax4[i,0].set_ylabel("Amplitude", fontsize=12)
        ax4[i,0].grid(True)
        
        # Señal rectificada
        ax4[i,1].plot(t, y_mod_rect, color='orange')
        ax4[i,1].set_title(f"Rectified Signal (μ = {m})", fontsize=14)
        ax4[i,1].set_xlabel("Time (s)", fontsize=12)
        ax4[i,1].set_ylabel("Amplitude", fontsize=12)
        ax4[i,1].grid(True)
    
    plt.tight_layout()
    st.pyplot(fig4)

if __name__ == "__main__":
    main()