import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import streamlit as st
import time

# Funzione per disegnare il rotolo statico

def draw_roll(D, L, highlight_point=None):
    fig, ax = plt.subplots(figsize=(7, 7))
    R = D / 2
    theta = L / R

    angle_nip_deg = 250
    angle_nip_rad = np.radians(angle_nip_deg)
    x_nip = R * np.cos(angle_nip_rad)
    y_nip = R * np.sin(angle_nip_rad)

    angle_colla_init_deg = 90
    angle_colla_init_rad = np.radians(angle_colla_init_deg)
    angle_colla_final_rad = angle_colla_init_rad + theta
    angle_colla_final_deg = np.degrees(angle_colla_final_rad) % 360
    x_colla_init = R * np.cos(angle_colla_init_rad)
    y_colla_init = R * np.sin(angle_colla_init_rad)
    x_colla_final = R * np.cos(angle_colla_final_rad)
    y_colla_final = R * np.sin(angle_colla_final_rad)

    theta_deg = (angle_nip_deg - angle_colla_final_deg) % 360

    ax.set_facecolor("#f9f9f9")
    ax.grid(True, linestyle='--', alpha=0.3)

    roll = plt.Circle((0, 0), R, fill=False, linewidth=2, edgecolor="#333")
    core = plt.Circle((0, 0), R * 0.3, fill=False, linestyle='--', linewidth=1.2, edgecolor="#666")
    ax.add_patch(roll)
    ax.add_patch(core)

    ax.plot([x_nip - L, x_nip], [y_nip, y_nip], color="#795548", linewidth=3.0, label='Velo da tagliare (L)')

    ax.plot([x_colla_init], [y_colla_init], 'o', color="#e53935", markersize=8, label='Colla applicata (@90°)')
    ax.plot([x_colla_final], [y_colla_final], 'o', color="#43a047", markersize=8, label=f'Posizione dopo rotazione ({angle_colla_final_deg:.1f}°)')
    ax.plot([x_nip], [y_nip], 'o', color="#1e88e5", markersize=8, label='Punto di NIP (fisso @250°)')

    arc = patches.Arc((0, 0), 2*R, 2*R, angle=0,
                      theta1=angle_colla_init_deg,
                      theta2=angle_colla_final_deg,
                      color='#ffa726', linewidth=2.5, label='Rotazione pre-taglio θ')
    ax.add_patch(arc)

    arc_theta = patches.Arc((0, 0), 0.6*R, 0.6*R, angle=0,
                            theta1=angle_colla_init_deg,
                            theta2=angle_nip_deg,
                            color='blue', linewidth=1.5, linestyle='--')
    ax.add_patch(arc_theta)

    angle_label = angle_colla_init_rad + theta / 2
    x_theta = 0.4 * R * np.cos(angle_label)
    y_theta = 0.4 * R * np.sin(angle_label)
    ax.text(x_theta, y_theta, 'θ', fontsize=14, color='blue', ha='center', va='center')

    for deg in [0, 90, 180, 210, 250, 270, 360]:
        angle_rad = np.radians(deg)
        x = (R + 20) * np.cos(angle_rad)
        y = (R + 20) * np.sin(angle_rad)
        ax.text(x, y, f"{deg}°", ha='center', va='center', fontsize=9, color='black')

    rullo_raggio = 20
    rullo_offset_y = -R - 40
    distanza_rulli = 2 * R * 0.8
    for x in [-distanza_rulli/2, distanza_rulli/2]:
        ax.add_patch(plt.Circle((x, rullo_offset_y), rullo_raggio, color='gray'))
        ax.add_patch(plt.Circle((x, rullo_offset_y), rullo_raggio+5, fill=False, edgecolor='yellow', linewidth=2))

    if highlight_point:
        ax.plot(*highlight_point, 'o', color='red', markersize=6)
        ax.plot([0, highlight_point[0]], [0, highlight_point[1]], color='red', linestyle='--', linewidth=1.5)

    ax.set_xlim(-R - 200, R + 200)
    ax.set_ylim(rullo_offset_y - 60, R + 120)
    ax.set_aspect('equal')
    ax.set_title(f"\u2728 Bobina Interattiva \u2728\nDiametro = {D:.0f} mm | Lunghezza Velo = {L:.0f} mm",
                 fontsize=13, fontweight='bold', color="#333")

    return fig, theta_deg, angle_colla_init_rad, theta, R

# Funzione per animare la rotazione della colla

def animate_rotation(D, L):
    steps = 20
    R = D / 2
    theta = L / R
    angle_colla_init_rad = np.radians(90)
    fig_base, *_ = draw_roll(D, L, highlight_point=None)  # disegno base senza colla animata
    for i in range(steps + 1):
        step_theta = theta * i / steps
        angle_step = angle_colla_init_rad + step_theta
        x_step = R * np.cos(angle_step)
        y_step = R * np.sin(angle_step)
        fig, ax = plt.subplots(figsize=(7, 7))
        ax.imshow(fig_base.canvas.buffer_rgba(), extent=ax.get_window_extent().bounds, aspect='auto')
        ax.plot([0, x_step], [0, y_step], color='red', linestyle='--', linewidth=2)
        ax.plot(x_step, y_step, 'o', color='red', markersize=6)
        ax.set_xlim(-R - 200, R + 200)
        ax.set_ylim(-R - 200, R + 200)
        ax.axis('off')
        st.pyplot(fig, use_container_width=True)
        time.sleep(0.05)

# Streamlit app
st.set_page_config(page_title="Bobina Interattiva", layout="centered")
st.title("🌀 Bobina Interattiva")

D = st.slider("Diametro della bobina (mm)", min_value=800, max_value=1200, value=1000, step=10)
L = st.slider("Lunghezza del velo (mm)", min_value=50, max_value=2000, value=1200, step=10)

animate = st.checkbox("Mostra animazione della rotazione")

fig, theta_deg, *_ = draw_roll(D, L)
st.pyplot(fig, use_container_width=True)

if animate:
    animate_rotation(D, L)

st.markdown(f"#### θ = {theta_deg:.2f}° → Rotazione da applicare PRIMA del taglio per far combaciare la colla con il punto NIP")
