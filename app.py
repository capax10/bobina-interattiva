import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Funzione per disegnare il rotolo
def draw_roll(D, L):
    fig, ax = plt.subplots(figsize=(5, 5))
    R = D / 2

    # Disegno del rotolo
    roll = plt.Circle((0, 0), R, fill=False, linewidth=2)
    core = plt.Circle((0, 0), R * 0.3, fill=False, linestyle='--')
    ax.add_patch(roll)
    ax.add_patch(core)

    # Angolo di rotazione theta (in radianti)
    theta = 2 * L / D

    # Punto colla ruotato in avanti di theta (verso arrotolamento)
    x_colla = R * np.sin(-theta)
    y_colla = R * np.cos(-theta)
    ax.plot([x_colla], [y_colla], 'ro', label='Colla')

    # Punto iniziale del velo (dalla parte opposta rispetto al punto colla)
    x_velo_start = R * np.sin(0)
    y_velo_start = R * np.cos(0)
    ax.plot([x_velo_start, x_colla], [y_velo_start, y_colla], 'g-', linewidth=2, label='Velo L')

    ax.set_xlim(-R - 100, R + 100)
    ax.set_ylim(-R - 100, R + 100)
    ax.set_aspect('equal')
    ax.set_title(f"Bobina Interattiva\nD = {D:.0f} mm, L = {L:.0f} mm, θ = {np.degrees(theta):.2f}°")
    ax.legend()

    return fig

# Streamlit app
st.title("Bobina Interattiva")

D = st.slider("Diametro D (mm)", min_value=800, max_value=1200, value=1000)
L = st.slider("Lunghezza L (mm)", min_value=50, max_value=600, value=300)

fig = draw_roll(D, L)
st.pyplot(fig)

st.markdown(f"### Angolo di rotazione: {np.degrees(2 * L / D):.2f}°")
