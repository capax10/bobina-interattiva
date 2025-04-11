import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import streamlit as st

# Funzione per disegnare il rotolo con etichette e arco evidenziato

def draw_roll(D, L):
    fig, ax = plt.subplots(figsize=(6, 6))
    R = D / 2
    theta = L / R

    # Disegno del rotolo
    roll = plt.Circle((0, 0), R, fill=False, linewidth=2)
    core = plt.Circle((0, 0), R * 0.3, fill=False, linestyle='--')
    ax.add_patch(roll)
    ax.add_patch(core)

    # Punto iniziale del velo (a ore 7 = circa 210°)
    angle_start = 7 * np.pi / 6
    x_start = R * np.cos(angle_start)
    y_start = R * np.sin(angle_start)

    # Punto colla dopo rotazione dal punto ore 7
    theta_required = L / R
    angle_colla_rotated = angle_start - theta_required
    x_colla = R * np.cos(angle_colla_rotated)
    y_colla = R * np.sin(angle_colla_rotated)

    # Disegno del velo e colla
    ax.plot([x_start, x_colla], [y_start, y_colla], 'g-', linewidth=2, label='Velo L')
    ax.plot([x_colla], [y_colla], 'ro', label='Colla')

    # Evidenziazione dell'arco di lunghezza L
    arc = patches.Arc((0, 0), 2*R, 2*R, angle=0,
                      theta1=np.degrees(angle_colla_rotated),
                      theta2=np.degrees(angle_start),
                      color='orange', linewidth=2, label='Arco L')
    ax.add_patch(arc)

    # Etichette per ore 12 e ore 7
    x_ore12 = R * np.cos(np.pi / 2)
    y_ore12 = R * np.sin(np.pi / 2)
    ax.text(x_ore12, y_ore12 + 20, "Ore 12", ha='center', va='bottom', fontsize=9, color='black')

    x_ore7 = R * np.cos(angle_start)
    y_ore7 = R * np.sin(angle_start)
    ax.text(x_ore7 - 20, y_ore7 - 10, "Ore 7", ha='right', va='top', fontsize=9, color='black')

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

fig = draw_roll(D, L)
st.pyplot(fig, use_container_width=True)

st.markdown(f"### Angolo di rotazione: {np.degrees(L / (D/2)):.2f}°")
