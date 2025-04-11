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

    # Punto iniziale del velo (a ore 7 = circa 210°)
    angle_start = 7 * np.pi / 6  # 210° in radianti
    x_start = R * np.cos(angle_start)
    y_start = R * np.sin(angle_start)

    # Punto colla a ore 12 (90° = pi/2)
    angle_colla = np.pi / 2
    x_colla_base = R * np.cos(angle_colla)
    y_colla_base = R * np.sin(angle_colla)

    # Calcolo dell'angolo di rotazione necessario per portare il punto colla a distanza L da ore 7
    theta_required = L / R
    angle_colla_rotated = angle_start - theta if theta_anim is not None else angle_start - theta_required
    x_colla = R * np.cos(angle_colla_rotated)
    y_colla = R * np.sin(angle_colla_rotated)

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
        st.pyplot(fig, use_container_width=True)
        time.sleep(0.05)
else:
    fig = draw_roll(D, L)
    st.pyplot(fig, use_container_width=True)

st.markdown(f"### Angolo di rotazione: {np.degrees(L / (D/2)):.2f}°")
