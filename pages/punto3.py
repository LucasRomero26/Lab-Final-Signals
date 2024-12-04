import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter

st.markdown("<h1 style='text-align: center; color: white;'>Phase-Quadrature</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: white;'>Amplitude Modulation and Demodulation</h3>", unsafe_allow_html=True)

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

def low_pass_filter(signal, w_0, fs):
    w = 2*np.pi* np.fft.fftfreq(len(signal), d=1/fs)
    x_w = np.fft.fft(signal)
    filter = np.abs(w) <= w_0
    x_w_filtered = x_w * filter
    filtered_signal = np.fft.ifft(x_w_filtered)
    return np.real(filtered_signal)

def create_plot(fig, subplot_pos, t, signal, w, spectrum, title_time, title_freq, color):
    # Time domain
    ax1 = plt.subplot(subplot_pos[0])
    plt.plot(t, signal, color=color)
    plt.title(title_time)
    plt.ylabel('Amplitude')
    plt.xlabel('Time [s]')
    config_subplot(ax1)
    
    # Frequency domain
    ax2 = plt.subplot(subplot_pos[1])
    plt.plot(w, spectrum, color=color)
    plt.title(title_freq)
    plt.ylabel('Normalized Magnitude')
    plt.xlabel('Frequency [w]')
    config_subplot(ax2)

def config_subplot(ax):
    ax.patch.set_alpha(0.0)
    ax.grid(True, alpha=0.3)
    for spine in ax.spines.values():
        spine.set_color('white')

def main():
    st.title("Signal Modulation Analysis")
    
    # Sidebar for parameters
    st.sidebar.header("Signal Parameters")
    
    # Adjustable parameters
    fs = st.sidebar.slider("Sampling Frequency (Hz)", 500, 2000, 1000)
    f_1 = st.sidebar.slider("Modulating Signal 1 Frequency (Hz)", 1, 20, 5)
    f_2 = st.sidebar.slider("Modulating Signal 2 Frequency (Hz)", 1, 20, 7)
    f0 = st.sidebar.slider("Carrier Frequency (Hz)", 50, 200, 100)
    w_cutoff = st.sidebar.slider("Filter Cutoff Frequency (Hz)", 1, 50, 10)
    
    # Signal generation
    t = np.arange(0, 1, 1/fs)
    
    # Modulating signals
    x1_t = np.sin(2 * np.pi * f_1 * t)
    x2_t = np.sin(2 * np.pi * f_2 * t)
    
    # Carrier signals
    w0 = 2 * np.pi * f0
    p1_t = np.cos(w0 * t)
    p2_t = np.sin(w0 * t)
    
    # === FFT calculations for all signals ===
    
    # Helper function for FFT calculation
    def calc_fft(signal):
        w = np.linspace(-len(signal)/2, len(signal)/2, len(signal))
        fft = np.fft.fft(signal)
        fft_centered = np.abs(np.fft.fftshift(fft))
        fft_normalized = fft_centered/np.max(fft_centered)
        return w, fft_normalized
    
    # FFT for modulating signals
    w_1, x1_w_normalized = calc_fft(x1_t)
    w_2, x2_w_normalized = calc_fft(x2_t)
    
    # FFT for carrier signals
    w_p1, p1_w_normalized = calc_fft(p1_t)
    w_p2, p2_w_normalized = calc_fft(p2_t)
    
    # Modulation
    x1_mod = x1_t * p1_t
    x2_mod = x2_t * p2_t
    y_t = x1_mod + x2_mod
    
    # FFT for modulated signals
    w_1_mod, x1_mod_w_normalized = calc_fft(x1_mod)
    w_2_mod, x2_mod_w_normalized = calc_fft(x2_mod)
    w_total, y_w_normalized = calc_fft(y_t)
    
    # Demodulation
    y1_dem = y_t * p1_t
    y2_dem = y_t * p2_t
    
    # FFT for demodulated signals
    w_1_dem, y1_dem_w_normalized = calc_fft(y1_dem)
    w_2_dem, y2_dem_w_normalized = calc_fft(y2_dem)
    
    # Signal recovery with filter
    y1_recovered = low_pass_filter(y1_dem, 2*np.pi*w_cutoff, fs)
    y2_recovered = low_pass_filter(y2_dem, 2*np.pi*w_cutoff, fs)
    
    # FFT for recovered signals
    w_1_rec, y1_recovered_w_normalized = calc_fft(y1_recovered)
    w_2_rec, y2_recovered_w_normalized = calc_fft(y2_recovered)
    
    # === Visualizations ===
    st.header("1. Modulating Signals")
    fig1 = plt.figure(figsize=(12, 8))
    plt.style.use("dark_background")
    create_plot(fig1, [221, 222], t, x1_t, w_1, x1_w_normalized, 
                'Signal 1 - Time Domain', 'Signal 1 - Frequency Domain', 'orange')
    create_plot(fig1, [223, 224], t, x2_t, w_2, x2_w_normalized,
                'Signal 2 - Time Domain', 'Signal 2 - Frequency Domain', 'green')
    fig1.patch.set_alpha(0.0)
    plt.tight_layout()
    st.pyplot(fig1)
    
    st.header("2. Carrier Signals")
    fig2 = plt.figure(figsize=(12, 8))
    create_plot(fig2, [221, 222], t, p1_t, w_p1, p1_w_normalized,
                'Carrier 1 - Time Domain', 'Carrier 1 - Frequency Domain', 'orange')
    create_plot(fig2, [223, 224], t, p2_t, w_p2, p2_w_normalized,
                'Carrier 2 - Time Domain', 'Carrier 2 - Frequency Domain', 'green')
    fig2.patch.set_alpha(0.0)
    plt.tight_layout()
    st.pyplot(fig2)
    
    st.header("3. Modulated Signals")
    fig3 = plt.figure(figsize=(12, 12))
    create_plot(fig3, [321, 322], t, x1_mod, w_1_mod, x1_mod_w_normalized,
                'Modulated Signal 1 - Time Domain', 'Modulated Signal 1 - Frequency Domain', 'orange')
    create_plot(fig3, [323, 324], t, x2_mod, w_2_mod, x2_mod_w_normalized,
                'Modulated Signal 2 - Time Domain', 'Modulated Signal 2 - Frequency Domain', 'green')
    create_plot(fig3, [325, 326], t, y_t, w_total, y_w_normalized,
                'Total Signal - Time Domain', 'Total Signal - Frequency Domain', 'red')
    fig3.patch.set_alpha(0.0)
    plt.tight_layout()
    st.pyplot(fig3)
    
    st.header("4. Demodulated Signals")
    fig4 = plt.figure(figsize=(12, 8))
    create_plot(fig4, [221, 222], t, y1_dem, w_1_dem, y1_dem_w_normalized,
                'Demodulated Signal 1 - Time Domain', 'Demodulated Signal 1 - Frequency Domain', 'orange')
    create_plot(fig4, [223, 224], t, y2_dem, w_2_dem, y2_dem_w_normalized,
                'Demodulated Signal 2 - Time Domain', 'Demodulated Signal 2 - Frequency Domain', 'green')
    fig4.patch.set_alpha(0.0)
    plt.tight_layout()
    st.pyplot(fig4)
    
    st.header("5. Recovered Signals")
    fig5 = plt.figure(figsize=(12, 8))
    create_plot(fig5, [221, 222], t, y1_recovered, w_1_rec, y1_recovered_w_normalized,
                'Recovered Signal 1 - Time Domain', 'Recovered Signal 1 - Frequency Domain', 'orange')
    create_plot(fig5, [223, 224], t, y2_recovered, w_2_rec, y2_recovered_w_normalized,
                'Recovered Signal 2 - Time Domain', 'Recovered Signal 2 - Frequency Domain', 'green')
    fig5.patch.set_alpha(0.0)
    plt.tight_layout()
    st.pyplot(fig5)

if __name__ == "__main__":
    main()