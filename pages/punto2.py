import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import io

st.markdown("<h1 style='text-align: center; color: white;'>Signal Modulation</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: white;'>Modulation and Demodulation of an Audio File</h3>", unsafe_allow_html=True)

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

def filtro_pasa_bajas(signal, w_0, fs):
    w = 2*np.pi* np.fft.fftfreq(len(signal), d=1/fs)
    x_w = np.fft.fft(signal)
    filtro = np.abs(w) <= w_0
    x_w_filtrado = x_w * filtro
    signal_filtrada = np.fft.ifft(x_w_filtrado)
    return np.real(signal_filtrada)

def create_plot(fig, subplot_pos, x, y, title, xlabel, ylabel, color='blue'):
    ax = plt.subplot(subplot_pos)
    plt.plot(x, y, color=color)
    plt.title(title, fontsize=14, pad=10)  # Increased title font size
    plt.xlabel(xlabel, fontsize=12)  # Increased x-label font size
    plt.ylabel(ylabel, fontsize=12)  # Increased y-label font size
    ax.tick_params(axis='both', which='major', labelsize=10)  # Increased tick label size
    ax.patch.set_alpha(0.0)
    ax.grid(True, alpha=0.3)
    for spine in ax.spines.values():
        spine.set_color('white')

def create_audio_file(signal, samplerate):
    """Convert signal to WAV file bytes"""
    # Normalize the signal to 16-bit range
    normalized = np.int16(signal * 32767)
    # Create a BytesIO buffer
    buffer = io.BytesIO()
    # Write the WAV file to the buffer
    wavfile.write(buffer, samplerate, normalized)
    # Get the buffer value
    buffer.seek(0)
    return buffer

def main():
    st.title("Audio Analysis and Modulation")
    
    # File upload
    uploaded_file = st.file_uploader("Upload audio file (.wav)", type=['wav'])
    
    if uploaded_file is not None:
        # Read audio file
        try:
            # Convert uploaded file to a format that wavfile.read can handle
            audio_bytes = uploaded_file.read()
            audio_stream = io.BytesIO(audio_bytes)
            samplerate, data = wavfile.read(audio_stream)
            
            # Show basic audio information
            length = data.shape[0] / samplerate
            st.write(f"Sample rate: {samplerate} Hz")
            st.write(f"Duration: {length:.2f} seconds")

            # Create columns for audio players
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Original Audio")
                # Reset the uploaded file position
                uploaded_file.seek(0)
                st.audio(uploaded_file)
            
            # Create time vector
            t = np.linspace(0, length, data.shape[0])
            
            # Process audio (mono or stereo)
            if len(data.shape) == 2 and data.shape[1] == 2:
                st.write("Stereo audio detected")
                x_t = data[:, 0]/np.max(data[:, 0])  # Use left channel
            else:
                st.write("Mono audio detected")
                x_t = data/np.max(data)
            
            # Carrier parameters in sidebar
            st.sidebar.header("Modulation Parameters")
            A = st.sidebar.slider("Carrier amplitude", 0.1, 2.0, 1.0)
            
            # Calculate original signal frequency
            n_muestras = len(x_t)
            frecuencias = np.fft.fftfreq(n_muestras, d=1/samplerate)
            
            # FFT of original signal
            w = np.linspace(-len(x_t)/2, len(x_t)/2, len(x_t))
            x_w = np.fft.fft(x_t)
            x_w_centrado = np.abs(np.fft.fftshift(x_w))
            x_w_normalizado = x_w_centrado/np.max(x_w_centrado)
            
            # Find dominant frequency
            frecuencias_centradas = np.fft.fftshift(frecuencias)
            indice_frecuencia = np.argmax(x_w_centrado)
            frecuencia = abs(frecuencias_centradas[indice_frecuencia])
            
            st.write(f"Detected dominant frequency: {frecuencia:.2f} Hz")
            
            # Carrier frequency selector
            f0 = st.sidebar.slider("Carrier frequency (Hz)", 
                                 min_value=int(10*frecuencia),
                                 max_value=int(50*frecuencia),
                                 value=int(20*frecuencia))
            
            # Filter cutoff frequency
            w_corte = st.sidebar.slider("Filter cutoff frequency (Hz)",
                                      min_value=100,
                                      max_value=5000,
                                      value=2000)
            
            # Generate carrier signal
            w0 = 2 * np.pi * f0
            p_t = A * np.cos(w0 * t)
            
            # Modulation
            x_mod = x_t * p_t
            
            # Demodulation
            x_dem = x_mod * p_t
            
            # Filtering
            x_recuperada = filtro_pasa_bajas(x_dem, 2*np.pi*w_corte, samplerate)
            
            # Add audio player for recovered signal in the second column
            with col2:
                st.subheader("Recovered Audio")
                recovered_audio = create_audio_file(x_recuperada, samplerate)
                st.audio(recovered_audio)
            
            # FFT calculations
            def calc_fft(signal):
                fft = np.fft.fft(signal)
                fft_centered = np.abs(np.fft.fftshift(fft))
                return fft_centered/np.max(fft_centered)
            
            p_w_normalizado = calc_fft(p_t)
            x_mod_w_normalizado = calc_fft(x_mod)
            x_w_dem_normalizado = calc_fft(x_dem)
            x_recuperada_w_normalizado = calc_fft(x_recuperada)
            
            # 1. Initial audio visualization (stereo/mono)
            if len(data.shape) == 2 and data.shape[1] == 2:
                st.header("Original Audio Signal (Stereo)")
                fig_stereo = plt.figure(figsize=(15, 6))
                plt.style.use("dark_background")
                create_plot(fig_stereo, 111, t, data[:, 0] / np.max(data[:, 0]), 
                          "Audio Channels", "Time [s]", "Amplitude", "blue")
                plt.plot(t, data[:, 1] / np.max(data[:, 1]), label="Right channel", color="red")
                plt.legend(["Left channel", "Right channel"], fontsize=10)
                fig_stereo.patch.set_alpha(0.0)
                plt.tight_layout()
                st.pyplot(fig_stereo)

            # 2. Original Signal vs FFT
            st.header("Original Signal and its Transform")
            fig1 = plt.figure(figsize=(15, 6))
            plt.style.use("dark_background")
            create_plot(fig1, 121, t, x_t, "Original Signal - Time", "Time [s]", "Amplitude")
            create_plot(fig1, 122, w, x_w_normalizado, "Original Signal - Frequency", "Frequency [Hz]", "Magnitude")
            fig1.patch.set_alpha(0.0)
            plt.tight_layout()
            st.pyplot(fig1)
            
            # 3. Carrier Signal
            st.header("Carrier Signal")
            fig2 = plt.figure(figsize=(15, 6))
            create_plot(fig2, 121, t[:500], p_t[:500], "Carrier Signal - Time", "Time [s]", "Amplitude")
            create_plot(fig2, 122, w, p_w_normalizado, "Carrier Signal - Frequency", "Frequency [Hz]", "Magnitude")
            fig2.patch.set_alpha(0.0)
            plt.tight_layout()
            st.pyplot(fig2)
            
            # 4. Modulated Signal
            st.header("Modulated Signal")
            fig3 = plt.figure(figsize=(15, 6))
            create_plot(fig3, 121, t, x_mod, "Modulated Signal - Time", "Time [s]", "Amplitude")
            create_plot(fig3, 122, w, x_mod_w_normalizado, "Modulated Signal - Frequency", "Frequency [Hz]", "Magnitude")
            fig3.patch.set_alpha(0.0)
            plt.tight_layout()
            st.pyplot(fig3)

            # 5. Visual Comparison: Original vs Modulated (Time)
            st.header("Comparison: Original vs Modulated")
            fig_comp1 = plt.figure(figsize=(15, 6))
            plt.subplot(211)
            plt.plot(t[0:2000], x_t[0:2000], label="Original")
            plt.title("Original Signal (First 2000 samples)", fontsize=14, pad=10)
            plt.xlabel("Time [s]", fontsize=12)
            plt.ylabel("Amplitude", fontsize=12)
            plt.legend(fontsize=10)
            plt.tick_params(axis='both', which='major', labelsize=10)

            plt.subplot(212)
            plt.plot(t[0:2000], x_mod[0:2000], label="Modulated")
            plt.title("Modulated Signal (First 2000 samples)", fontsize=14, pad=10)
            plt.xlabel("Time [s]", fontsize=12)
            plt.ylabel("Amplitude", fontsize=12)
            plt.legend(fontsize=10)
            plt.tick_params(axis='both', which='major', labelsize=10)
            fig_comp1.patch.set_alpha(0.0)
            plt.tight_layout()
            st.pyplot(fig_comp1)

            # 6. Visual Comparison: Original vs Modulated (Frequency)
            st.header("Comparison: Original vs Modulated Spectra")
            fig_comp2 = plt.figure(figsize=(15, 6))
            plt.subplot(211)
            plt.plot(w, x_w_normalizado, label="Original")
            plt.title("Original Signal Spectrum", fontsize=14, pad=10)
            plt.xlabel("Frequency [Hz]", fontsize=12)
            plt.ylabel("Magnitude", fontsize=12)
            plt.legend(fontsize=10)
            plt.tick_params(axis='both', which='major', labelsize=10)

            plt.subplot(212)
            plt.plot(w, x_mod_w_normalizado, label="Modulated")
            plt.title("Modulated Signal Spectrum", fontsize=14, pad=10)
            plt.xlabel("Frequency [Hz]", fontsize=12)
            plt.ylabel("Magnitude", fontsize=12)
            plt.legend(fontsize=10)
            plt.tick_params(axis='both', which='major', labelsize=10)
            fig_comp2.patch.set_alpha(0.0)
            plt.tight_layout()
            st.pyplot(fig_comp2)
            
            # 7. Complete Process (Original, Modulated, Demodulated)
            st.header("Complete Modulation/Demodulation Process")
            fig_complete = plt.figure(figsize=(15, 12))
            
            # Original signal
            create_plot(fig_complete, 321, t[0:2000], x_t[0:2000], 
                       "Original Signal", "Time [s]", "Amplitude")
            
            # Original transform
            create_plot(fig_complete, 322, w, x_w_normalizado,
                       "Original Spectrum", "Frequency [Hz]", "Magnitude")
            
            # Modulated signal
            create_plot(fig_complete, 323, t[0:2000], x_mod[0:2000],
                       "Modulated Signal", "Time [s]", "Amplitude")
            
            # Modulated transform
            create_plot(fig_complete, 324, w, x_mod_w_normalizado,
                       "Modulated Spectrum", "Frequency [Hz]", "Magnitude")
            
            # Demodulated signal without filtering
            create_plot(fig_complete, 325, t[0:2000], x_dem[0:2000],
                       "Demodulated Signal (Unfiltered)", "Time [s]", "Amplitude")
            
            # Demodulated transform
            create_plot(fig_complete, 326, w, x_w_dem_normalizado,
                       "Demodulated Spectrum", "Frequency [Hz]", "Magnitude")
            
            fig_complete.patch.set_alpha(0.0)
            plt.tight_layout()
            st.pyplot(fig_complete)
            
            # 8. Final Recovered Signal
            st.header("Recovered Signal (After Filtering)")
            fig5 = plt.figure(figsize=(15, 6))
            create_plot(fig5, 121, t, x_recuperada, 
                       "Recovered Signal - Time", "Time [s]", "Amplitude", "orange")
            create_plot(fig5, 122, w, x_recuperada_w_normalizado,
                       "Recovered Signal - Frequency", "Frequency [Hz]", "Magnitude", "orange")
            fig5.patch.set_alpha(0.0)
            plt.tight_layout()
            st.pyplot(fig5)
            
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
    
    else:
        st.info("Please upload an audio file (.wav) to begin the analysis.")

if __name__ == "__main__":
    main()