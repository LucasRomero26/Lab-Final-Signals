import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

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


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.page_link("app.py", label="Home", use_container_width=True)

with col2:
    st.page_link("pages/punto1.py", label="Series Examples", use_container_width=True)

with col3:
    st.page_link("pages/punto2.py", label="Signal Modulation", use_container_width=True)

with col4:
    st.page_link("pages/punto1.py", label="Amplitude Modulation", use_container_width=True)


from scipy.io import wavfile

uploaded_files = st.file_uploader("Choose audio files", accept_multiple_files=True, type=["wav"])

if uploaded_files:
    for uploaded_file in uploaded_files:
        # Read the file
        samplerate, data = wavfile.read(uploaded_file)
        
        # Calculate the audio duration
        length = data.shape[0] / samplerate

        # Define status
        if length != 0:
            status = "Audio Uploaded"
            status2 = "ON"
        else:
            status = "No Audio Data"
            status2 = "OFF"

        # Display metrics
        col31, col32 = st.columns(2)
        col31.metric("Status Audio", status, status2)
        col32.metric("Duration", f"{length:.2f}", "SECONDS")
    
    time = np.linspace(0., length, data.shape[0])

    if len(data.shape) == 2 and data.shape[1] == 2:  
        fig, ax = plt.subplots()
        ax.plot(time, data[:, 0] / np.max(data[:, 0]), label="Left channel")
        ax.plot(time, data[:, 1] / np.max(data[:, 1]), label="Right channel")
        ax.legend()
        ax.set_xlabel("Time [s]")
        ax.set_ylabel("Amplitude")
        ax.set_title("Stereo signal")
        plt.style.use("dark_background")
        fig.patch.set_alpha(0.0)  # Fondo de la figura
        ax.patch.set_alpha(0.0)   # Fondo del área de los ejes
        st.pyplot(fig)
    else:  
        fig, ax = plt.subplots()
        ax.plot(time, data / np.max(data), label="Mono channel")
        ax.legend()
        plt.style.use("dark_background")
        fig.patch.set_alpha(0.0)  # Fondo de la figura
        ax.patch.set_alpha(0.0)   # Fondo del área de los ejes
        ax.set_xlabel("Time [s]")
        ax.set_ylabel("Amplitude")
        ax.set_title("Mono signal")
        st.pyplot(fig)
        
    if data.shape[1] == 2:
        x_t = data[:, 0] / np.max(data[:, 0])
    else:
        x_t = data

    w = np.linspace(-len(x_t)/2, len(x_t)/2, len(x_t))

    x_w = np.fft.fft(x_t)
    x_w_centrado = np.abs(np.fft.fftshift(x_w))
    x_w_normalizado = x_w_centrado / np.max(x_w_centrado)

    fig, ax = plt.subplots()
    ax.plot(w, x_w_normalizado)
    plt.style.use("dark_background")
    fig.patch.set_alpha(0.0)  # Fondo de la figura
    ax.patch.set_alpha(0.0)   # Fondo del área de los ejes
    ax.set_ylabel('Normalized magnitude')
    ax.set_xlabel('Frequency [Hz]')

    st.pyplot(fig)

    frecuencia_muestreo = samplerate
    n_muestras = len(x_t)
    frecuencias = np.fft.fftfreq(n_muestras, d=1/frecuencia_muestreo)
    frecuencias_centradas = np.fft.fftshift(frecuencias)

    indice_frecuencia = np.argmax(x_w_centrado)
    frecuencia = frecuencias_centradas[indice_frecuencia]

    st.subheader(f"The frequency of the function is approximately {abs(frecuencia)} Hz")

    A = st.number_input("Enter the carrier amplitude (e.g., 1):", value=1.0)
    frecuencia_modulante = st.number_input("Enter the modulating signal frequency (in Hz, e.g., 30000):", value=30000.0)

    f0 = st.number_input("Enter the carrier frequency (in Hz, e.g., 300000):", value=300000.0)

    while f0 < (10 * frecuencia_modulante):
        st.warning("The carrier frequency must be at least 10 times the modulating signal frequency.")
        f0 = st.number_input("Enter the carrier frequency (in Hz, e.g., 300000):", value=f0)

    w0 = 2 * np.pi * f0
    p_t = A * np.cos(w0 * time)

    st.subheader("Modulation")

    x_mod = x_t * p_t

    fig, ax = plt.subplots()
    ax.plot(time, x_mod)
    plt.style.use("dark_background")
    fig.patch.set_alpha(0.0)  # Fondo de la figura
    ax.patch.set_alpha(0.0)   # Fondo del área de los ejes
    ax.set_ylabel('Normalized magnitude')
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Amplitude")
    ax.set_title("Modulating and Carrier Signal")

    st.pyplot(fig)

    st.subheader("Visual comparison of the original audio signal x_t with the modulated signal x_modS")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    ax1.plot(time[0:2000], x_t[0:2000])
    ax1.set_title('x_t')
    plt.style.use("dark_background")
    fig.patch.set_alpha(0.0)  # Fondo de la figura
    ax1.patch.set_alpha(0.0)   # Fondo del área de los ejes

    ax2.plot(time[0:2000], x_mod[0:2000])
    ax2.set_title('x_mod')
    plt.style.use("dark_background")
    fig.patch.set_alpha(0.0)  # Fondo de la figura
    ax2.patch.set_alpha(0.0)   # Fondo del área de los ejes

    st.pyplot(fig)

    st.subheader("Calculation of the FFT of the modulated signal")
    
    w = np.linspace(-len(x_mod)/2, len(x_mod)/2, len(x_mod))

    x_w_mod = np.fft.fft(x_mod)

    x_w_mod_centrado = np.abs(np.fft.fftshift(x_w_mod))
    x_w_mod_normalizado = x_w_mod_centrado / np.max(x_w_mod_centrado)

    plt.figure(figsize=(10, 5))
    plt.plot(w, x_w_mod_normalizado)
    plt.style.use("dark_background")

    fig = plt.gcf()  # Obtener la figura actual
    ax = plt.gca()   # Obtener el eje actual

    fig.patch.set_alpha(0.0)  # Fondo de la figura
    ax.patch.set_alpha(0.0)   # Fondo del área de los ejes

    st.pyplot(fig)

    st.subheader("Original and Modulated Signal in the Frequency Domain")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    ax1.plot(w, x_w_normalizado)
    ax1.set_title('Original Signal in Frequency Domain')
    plt.style.use("dark_background")
    fig.patch.set_alpha(0.0)  # Fondo de la figura
    ax1.patch.set_alpha(0.0)   # Fondo del área de los ejes


    ax2.plot(w, x_w_mod_normalizado)
    ax2.set_title('Modulated Signal in Frequency Domain')
    plt.style.use("dark_background")
    fig.patch.set_alpha(0.0)  # Fondo de la figura
    ax2.patch.set_alpha(0.0)   # Fondo del área de los ejes


    st.pyplot(fig)

    st.subheader("Demodulation")

    x_dem = x_mod * p_t

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 15))

    ax1.plot(time[0:2000], x_t[0:2000])
    ax1.set_title('Original Signal')
    plt.style.use("dark_background")
    fig.patch.set_alpha(0.0)  # Fondo de la figura
    ax1.patch.set_alpha(0.0)   # Fondo del área de los ejes

    ax2.plot(time[0:2000], x_mod[0:2000])
    ax2.set_title('Modulated Signal')
    plt.style.use("dark_background")
    fig.patch.set_alpha(0.0)  # Fondo de la figura
    ax2.patch.set_alpha(0.0)   # Fondo del área de los ejes

    ax3.plot(time[0:2000], x_dem[0:2000])
    ax3.set_title('Demodulated Signal (Unfiltered)')
    plt.style.use("dark_background")
    fig.patch.set_alpha(0.0)  # Fondo de la figura
    ax3.patch.set_alpha(0.0)   # Fondo del área de los ejes

    st.pyplot(fig)


    st.subheader(" FFT of the demodulated signal")
    x_w_dem = np.fft.fft(x_dem)
    x_w_dem_centrado = np.abs(np.fft.fftshift(x_w_dem))
    x_w_dem_normalizado = x_w_dem_centrado / np.max(x_w_dem_centrado)

    # Configuración del estilo
    plt.style.use("dark_background")

    # Crear la figura y el eje
    fig, ax1 = plt.subplots(figsize=(10, 5))
    fig.patch.set_alpha(0.0)  # Fondo de la figura
    ax1.patch.set_alpha(0.0)  # Fondo del área de los ejes

    # Graficar los datos
    ax1.plot(w, x_w_dem_normalizado)

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 15))

    ax1.plot(w, x_w_normalizado)
    ax1.set_title('Original Signal in Frequency Domain')
    plt.style.use("dark_background")
    fig.patch.set_alpha(0.0)  # Fondo de la figura
    ax1.patch.set_alpha(0.0)   # Fondo del área de los ejes

    ax2.plot(w, x_w_mod_normalizado)
    ax2.set_title('Modulated Signal in Frequency Domain')
    plt.style.use("dark_background")
    fig.patch.set_alpha(0.0)  # Fondo de la figura
    ax2.patch.set_alpha(0.0)   # Fondo del área de los ejes

    ax3.plot(w, x_w_dem_normalizado)
    ax3.set_title('Demodulated Signal (Unfiltered) in Frequency Domain')
    plt.style.use("dark_background")
    fig.patch.set_alpha(0.0)  # Fondo de la figura
    ax3.patch.set_alpha(0.0)   # Fondo del área de los ejes

    st.pyplot(fig)

    st.subheader("Low-pass filtered signal")

    limit1 = int(-samplerate/2 + int(len(w)/2))
    limit2 = int(samplerate/2 + int(len(w)/2))

    x_w_recortado = x_w_dem_normalizado[limit1:limit2]

    # Configuración de estilo oscuro
    plt.style.use("dark_background")

    # Crear la figura y el eje
    fig, ax3 = plt.subplots(figsize=(10, 5))
    ax3.plot(x_w_recortado)

    # Configurar transparencia de fondos
    fig.patch.set_alpha(0.0)  # Fondo de la figura
    ax3.patch.set_alpha(0.0)  # Fondo del área de los ejes

    # Mostrar la gráfica en Streamlit
    st.pyplot(fig)


else:
    st.warning("No audio files uploaded yet.")


