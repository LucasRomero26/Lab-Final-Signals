import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

#Punto 1
def fourier_reconstruction(periodo=1, N=5, delta=0.001, ciclos=2, scale=0.25):
    t1 = np.arange(-(periodo / 2), 0, delta)
    t2 = np.arange(0, (periodo / 2) + delta, delta)
    t = np.concatenate((t1, t2))

    x1 = 1 + 4 * (t1 / periodo)
    x2 = 1 - 4 * (t2 / periodo)
    x = np.concatenate((x1, x2))

    t_extended = np.concatenate([t + i * periodo for i in range(ciclos)])
    x_extended = np.tile(x, ciclos)

    x_recostruida = np.zeros(len(x), dtype=float)
    Coeficientes = np.zeros(N + 1)
    W0 = (2 * np.pi) / periodo
    W = np.zeros(N + 1)

    An_0 = 0
    x_recostruida += An_0
    Coeficientes[0] = An_0

    for n in range(1, N + 1):
        An = (4 / ((n * np.pi) ** 2)) * (1 - np.cos(n * np.pi))
        x_recostruida += An * np.cos(n * W0 * t)
        Coeficientes[n] = An
        W[n] = n

    x_re_extended = np.tile(x_recostruida, ciclos)

    fig, ax = plt.subplots(1, 2, figsize=(10, 4))

    min_y = min(np.min(x_extended), np.min(x_re_extended))
    max_y = max(np.max(x_extended), np.max(x_re_extended))
    lim_y = max(abs(min_y), abs(max_y)) * scale

    min_x = min(t_extended)
    max_x = max(t_extended)
    lim_x = max(abs(min_x), abs(max_x)) * scale

    min_n = min(Coeficientes)
    max_n = max(Coeficientes)
    lim_n = max(abs(min_n), abs(max_n)) * scale

    ax[0].set_title('Reconstrucción Por Serie Trigonométrica')
    ax[0].plot(t_extended, x_extended, linewidth=3.0, label="Señal original")
    ax[0].plot(t_extended, x_re_extended, linewidth=3.0, label="Reconstrucción", color="red")
    ax[0].set_xlabel("t")
    ax[0].set_ylabel("Amplitud")
    ax[0].set_xlim(min_x - lim_x, max_x + lim_x)
    ax[0].set_ylim(min_y - lim_y, max_y + lim_y)
    ax[0].legend()
    ax[0].grid(True)

    ax[1].set_title('Espectro en Línea')
    ax[1].stem(W, Coeficientes, basefmt=" ", linefmt='r-')
    ax[1].set_xlabel("Armónico")
    ax[1].set_xlim(np.min(W) - 1, np.max(W) + 1)
    ax[1].set_ylim(min_n - lim_n, max_n + lim_n)
    ax[1].grid(True)

    plt.tight_layout()
    plt.show()


fourier_reconstruction(periodo=1, N=5, delta=0.001, ciclos=2, scale=0.25)
