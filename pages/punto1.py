import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

def fourier_series_reconstruction(periodo=1, N=5, delta=0.001, ciclos=2, Scale=0.25):
    t1 = np.arange(-(periodo / 2), 0, delta)
    t2 = np.arange(0, (periodo/2) + delta, delta)
    t = np.concatenate((t1, t2))

    x1 = 1+4*(t1/periodo)
    x2 = 1-4*(t2/periodo)
    x = np.concatenate((x1, x2))

    t_extended = np.concatenate([t + i * periodo for i in range(ciclos)])
    x_extended = np.tile(x, ciclos)

    x_recostruida = np.zeros(len(x), dtype=float)
    Coeficientes = np.zeros(N + 1)
    W0 = (2*np.pi)/periodo
    W = np.zeros(N + 1)

    An_0 = 0
    x_recostruida += An_0
    Coeficientes[0] = An_0

    for n in range(1, N+1):
        An = (4/((n*np.pi)**2))*(1-np.cos(n*np.pi))
        x_recostruida += An*np.cos(n*W0*t)
        Coeficientes[n] = An
        W[n] = n

    x_re_extended = np.tile(x_recostruida, ciclos)

    fig, ax = plt.subplots(1, 2, figsize=(10, 4))

    min_y = min(np.min(x_extended), np.min(x_re_extended))
    max_y = max(np.max(x_extended), np.max(x_re_extended))
    lim_y = max(abs(min_y), abs(max_y)) * Scale

    min_x = min(t_extended)
    max_x = max(t_extended)
    lim_x = max(abs(min_x), abs(max_x)) * Scale

    min_n = min(Coeficientes)
    max_n = max(Coeficientes)
    lim_n = max(abs(min_n), abs(max_n)) * Scale

    fig, ax = plt.subplots(2, 1, figsize=(12, 15))

    # First subplot: Signal Reconstruction
    ax[0].set_title('Trigonometric Series Reconstruction',fontsize=22)
    ax[0].plot(t_extended, x_extended, linewidth=4.0, label="Señal original")
    ax[0].plot(t_extended, x_re_extended, linewidth=4.0, label="Reconstrucción", color="red")
    ax[0].set_xlabel("t",fontsize=20)
    ax[0].set_ylabel("Amplitude",fontsize=20)
    ax[0].set_xlim(min_x-0.5, max_x+0.5)
    ax[0].set_ylim(min_y-0.5, max_y+0.5)
    ax[0].legend(fontsize=16)
    plt.style.use("dark_background")
    fig.patch.set_alpha(0.0)  # Fondo de la figura
    ax[0].patch.set_alpha(0.0)   # Fondo del área de los ejes
    ax[1].patch.set_alpha(0.0)   # Fondo del área de los ejes
    ax[0].grid(True)

    
    # Second subplot: Spectrum
    ax[1].set_title('Line spectrum',fontsize=22)
    ax[1].stem(W, Coeficientes, basefmt=" ", linefmt='r-')
    ax[1].set_xlabel("Harmonic",fontsize=20)
    ax[1].set_xlim(np.min(W)-1, np.max(W)+1)
    ax[1].set_ylim(min_n-0.5, max_n+0.5)
    ax[1].grid(True)

    plt.tight_layout()
    st.pyplot(fig)

def fourier_series_reconstruction2(periodo=2*np.pi, N=5, delta=0.001, ciclos=2, Scale=0.25):
    t = np.arange(-(periodo / 2), (periodo/2) + delta, delta)
    x = t

    t_extended = np.concatenate([t + i * periodo for i in range(ciclos)])
    x_extended = np.tile(x, ciclos)

    x_recostruida = np.zeros(len(x), dtype=float)
    Coeficientes = np.zeros(N + 1)
    W0 = (2*np.pi)/periodo
    W = np.zeros(N + 1)

    An_0 = 0
    x_recostruida += An_0
    Coeficientes[0] = An_0

    for n in range(1, N+1):
        An = -2*(1/n)*np.cos(n*np.pi)
        x_recostruida += An*np.sin(n*W0*t)
        Coeficientes[n] = An
        W[n] = n

    x_re_extended = np.tile(x_recostruida, ciclos)

    fig, ax = plt.subplots(1, 2, figsize=(10, 4))

    min_y = min(np.min(x_extended), np.min(x_re_extended))
    max_y = max(np.max(x_extended), np.max(x_re_extended))
    lim_y = max(abs(min_y), abs(max_y)) * Scale

    min_x = min(t_extended)
    max_x = max(t_extended)
    lim_x = max(abs(min_x), abs(max_x)) * Scale

    min_n = min(Coeficientes)
    max_n = max(Coeficientes)
    lim_n = max(abs(min_n), abs(max_n)) * Scale

    fig, ax = plt.subplots(2, 1, figsize=(12, 15))

    # First subplot: Signal Reconstruction
    ax[0].set_title('Trigonometric Series Reconstruction',fontsize=22)
    ax[0].plot(t_extended, x_extended, linewidth=4.0, label="Señal original")
    ax[0].plot(t_extended, x_re_extended, linewidth=4.0, label="Reconstrucción", color="red")
    ax[0].set_xlabel("t",fontsize=20)
    ax[0].set_ylabel("Amplitud",fontsize=20)
    ax[0].set_xlim(min_x-0.5, max_x+0.5)
    ax[0].set_ylim(min_y-0.5, max_y+0.5)
    ax[0].legend(fontsize=16)
    plt.style.use("dark_background")
    fig.patch.set_alpha(0.0)  # Fondo de la figura
    ax[0].patch.set_alpha(0.0)   # Fondo del área de los ejes
    ax[1].patch.set_alpha(0.0)   # Fondo del área de los ejes
    ax[0].grid(True)

    
    # Second subplot: Spectrum
    ax[1].set_title('Line spectrum',fontsize=22)
    ax[1].stem(W, Coeficientes, basefmt=" ", linefmt='r-')
    ax[1].set_xlabel("Harmonic",fontsize=20)
    ax[1].set_xlim(np.min(W)-1, np.max(W)+1)
    ax[1].set_ylim(min_n-0.5, max_n+0.5)
    ax[1].grid(True)

    plt.tight_layout()
    st.pyplot(fig)

def fourier_series_reconstruction3(periodo=2*np.pi, N=5, delta=0.001, ciclos=2, Scale=0.25):
    t = np.arange(-(periodo / 2), (periodo/2) + delta, delta)
    x = t**2

    t_extended = np.concatenate([t + i * periodo for i in range(ciclos)])
    x_extended = np.tile(x, ciclos)

    x_recostruida = np.zeros(len(x), dtype=float)
    Coeficientes = np.zeros(N + 1)
    W0 = (2*np.pi)/periodo
    W = np.zeros(N + 1)

    An_0 = (np.pi**2)/3
    x_recostruida += An_0
    Coeficientes[0] = An_0

    for n in range(1, N+1):
        An = 4*(1/(n**2))*np.cos(n*np.pi)
        x_recostruida += An*np.cos(n*W0*t)
        Coeficientes[n] = An
        W[n] = n

    x_re_extended = np.tile(x_recostruida, ciclos)

    fig, ax = plt.subplots(1, 2, figsize=(10, 4))

    min_y = min(np.min(x_extended), np.min(x_re_extended))
    max_y = max(np.max(x_extended), np.max(x_re_extended))
    lim_y = max(abs(min_y), abs(max_y)) * Scale

    min_x = min(t_extended)
    max_x = max(t_extended)
    lim_x = max(abs(min_x), abs(max_x)) * Scale

    min_n = min(Coeficientes)
    max_n = max(Coeficientes)
    lim_n = max(abs(min_n), abs(max_n)) * Scale

    fig, ax = plt.subplots(2, 1, figsize=(12, 15))

    # First subplot: Signal Reconstruction
    ax[0].set_title('Trigonometric Series Reconstruction',fontsize=22)
    ax[0].plot(t_extended, x_extended, linewidth=4.0, label="Señal original")
    ax[0].plot(t_extended, x_re_extended, linewidth=4.0, label="Reconstrucción", color="red")
    ax[0].set_xlabel("t",fontsize=20)
    ax[0].set_ylabel("Amplitud",fontsize=20)
    ax[0].set_xlim(min_x-0.5, max_x+0.5)
    ax[0].set_ylim(min_y-0.5, max_y+0.5)
    ax[0].legend(fontsize=16)
    plt.style.use("dark_background")
    fig.patch.set_alpha(0.0)  # Fondo de la figura
    ax[0].patch.set_alpha(0.0)   # Fondo del área de los ejes
    ax[1].patch.set_alpha(0.0)   # Fondo del área de los ejes
    ax[0].grid(True)

    
    # Second subplot: Spectrum
    ax[1].set_title('Line spectrum',fontsize=22)
    ax[1].stem(W, Coeficientes, basefmt=" ", linefmt='r-')
    ax[1].set_xlabel("Harmonic",fontsize=20)
    ax[1].set_xlim(np.min(W)-1, np.max(W)+1)
    ax[1].set_ylim(min_n-0.5, max_n+0.5)
    ax[1].grid(True)

    plt.tight_layout()
    st.pyplot(fig)

def fourier_series_reconstruction4(periodo=2, N=5, delta=0.001, ciclos=2, Scale=0.25):
    t1 = np.arange(-(periodo / 2), 0, delta)
    t2 = np.arange(0, (periodo/2) + delta, delta)
    t = np.concatenate((t1, t2))

    x1 = t1
    x2 = np.ones(len(t2))
    x = np.concatenate((x1, x2))

    t_extended = np.concatenate([t + i * periodo for i in range(ciclos)])
    x_extended = np.tile(x, ciclos)

    x_recostruida = np.zeros(len(x), dtype=float)
    Coeficientes = np.zeros(N + 1)
    W0 = (2*np.pi)/periodo
    W = np.zeros(N + 1)

    An_0 = 1/4
    x_recostruida += An_0
    Coeficientes[0] = An_0

    for n in range(1, N+1):
        An = (1/((n**2)*(np.pi**2)))*(1-((-1)**n))
        Bn = (1/(n*np.pi))*(1-2*(-1)**n)
        x_recostruida += An*np.cos(n*W0*t)+Bn*np.sin(n*W0*t)
        Coeficientes[n] = ((An)**2+(Bn)**2)**0.5
        W[n] = n

    x_re_extended = np.tile(x_recostruida, ciclos)

    fig, ax = plt.subplots(1, 2, figsize=(10, 4))

    min_y = min(np.min(x_extended), np.min(x_re_extended))
    max_y = max(np.max(x_extended), np.max(x_re_extended))
    lim_y = max(abs(min_y), abs(max_y)) * Scale

    min_x = min(t_extended)
    max_x = max(t_extended)
    lim_x = max(abs(min_x), abs(max_x)) * Scale

    min_n = min(Coeficientes)
    max_n = max(Coeficientes)
    lim_n = max(abs(min_n), abs(max_n)) * Scale

    fig, ax = plt.subplots(2, 1, figsize=(12, 15))

    # First subplot: Signal Reconstruction
    ax[0].set_title('Trigonometric Series Reconstruction',fontsize=22)
    ax[0].plot(t_extended, x_extended, linewidth=4.0, label="Señal original")
    ax[0].plot(t_extended, x_re_extended, linewidth=4.0, label="Reconstrucción", color="red")
    ax[0].set_xlabel("t",fontsize=20)
    ax[0].set_ylabel("Amplitude",fontsize=20)
    ax[0].set_xlim(min_x-0.5, max_x+0.5)
    ax[0].set_ylim(min_y-0.5, max_y+0.5)
    ax[0].legend(fontsize=16)
    plt.style.use("dark_background")
    fig.patch.set_alpha(0.0)  # Fondo de la figura
    ax[0].patch.set_alpha(0.0)   # Fondo del área de los ejes
    ax[1].patch.set_alpha(0.0)   # Fondo del área de los ejes
    ax[0].grid(True)

    
    # Second subplot: Spectrum
    ax[1].set_title('Line spectrum',fontsize=22)
    ax[1].stem(W, Coeficientes, basefmt=" ", linefmt='r-')
    ax[1].set_xlabel("Harmonic",fontsize=20)
    ax[1].set_xlim(np.min(W)-1, np.max(W)+1)
    ax[1].set_ylim(min_n-0.5, max_n+0.5)
    ax[1].grid(True)

    plt.tight_layout()
    st.pyplot(fig)


st.markdown("<h1 style='text-align: center; color: white;'>Series Examples</h1>", unsafe_allow_html=True)

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
    st.page_link("pages/punto1.py", label="Amplitude Mod", use_container_width=True)
with col5:
    st.page_link("pages/punto4.py", label="DSB-LC", use_container_width=True)

st.subheader("Select which series you want to watch")
signal = None
signal = st.selectbox(
    "",
    ("Example 1","Example 2", "Example 3", "Example 4"),placeholder="Choose an option",index=None
)
armonicos = ""
if signal != None:
    st.subheader("Insert a number of harmonics")
    armonicos = st.number_input(
    "", value=None, placeholder="Type a number...")
    if armonicos != None:
        armonicos = int(armonicos)

if type(armonicos) == int and signal !=None:
    if signal == "Example 1":
        st.subheader(f"Number of harmonics {armonicos}")
        fourier_series_reconstruction(N=armonicos)
    elif signal == "Example 2":
        st.subheader(f"Number of harmonics {armonicos}")
        fourier_series_reconstruction2(N=armonicos)
    elif signal == "Example 3":
        st.subheader(f"Number of harmonics {armonicos}")
        fourier_series_reconstruction3(N=armonicos)
    elif signal == "Example 4":
        st.subheader(f"Number of harmonics {armonicos}")
        fourier_series_reconstruction4(N=armonicos)




    



