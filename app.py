import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import time

# Funzione per disegnare il rotolo con angolo custom

def draw_roll(D, L, theta_anim=None):
    fig, ax = plt.subplots(figsize=(6, 6))
    R = D / 2
    theta = L / R if theta_anim is None else theta_anim

    # Disegno del rotolo
    roll = plt.Circle((0, 0), R, fill=False, linewidth=2)
    core = plt.Circle((0, 0), R * 0.3, fill=False, linestyle='--')
    ax.add_patch(roll)
    ax.add_patch(core)

    # Punto iniziale del velo (a ore 9 = punto di contatto col rullo sinistro)
    x_start = -R
    y_start = 0

    # Punto colla ruotato in avanti (senso orario) di theta
    angle_colla = np.pi - theta
    x_colla = R * np.cos(angle_colla)
    y_colla = R * np.sin(angle_colla)

    # Disegno del velo e colla
    ax.plot([x_start, x_colla], [y_start, y_colla], 'g-', linewidth=2, label='Velo L')
    ax.plot([x_colla], [y_colla], 'ro', label='Colla')

    # Aggiunta dei rulli sotto la bobina
    rullo_raggio = 20
    rullo_offset_y = -R - 40
    distanza_rulli = 2 * R * 0.8

    rullo_sx = plt.Circle((-distanza_rulli / 2, rullo_offset_y), rullo_raggio, color='gray')
    rullo_dx = plt.Circle((distanza_rulli / 2, rullo_offset_y), rullo_raggio, color='gray')
    ax.add_patch(rullo_sx)
    ax.add_patch(rullo_dx)

    ax.set_xlim(-R - 150, R + 150)
    ax.set_ylim(rullo_offset_y - 50, R + 100)
    ax.set_aspect('equal')
    ax.set_title(f"Bobina Interattiva\nD = {D:.0f} mm, L = {L:.0f} mm, θ = {np.degrees(theta):.2f}°")
    ax.legend()

    return fig

# Streamlit app
st.title("Bobina Interattiva")

D = st.slider("Diametro D (mm)", min_value=800, max_value=1200, value=1000)
L = st.slider("Lunghezza L (mm)", min_value=50, max_value=600, value=300)
animate = st.button("▶️ Anima Rotazione")

if animate:
    theta_target = L / (D / 2)
    steps = 30
    for i in range(steps + 1):
        theta_step = theta_target * i / steps
        fig = draw_roll(D, L, theta_step)
        st.pyplot(fig)
        time.sleep(0.05)
else:
    fig = draw_roll(D, L)
    st.pyplot(fig)

st.markdown(f"### Angolo di rotazione: {np.degrees(L / (D/2)):.2f}°")
