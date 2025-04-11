import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import streamlit as st

# Funzione per disegnare il rotolo secondo la logica corretta del processo

def draw_roll(D, L):
    fig, ax = plt.subplots(figsize=(7, 7))
    R = D / 2
    theta = L / R  # angolo da ruotare la bobina PRIMA di tagliare il velo

    # Sfondo e griglia
    ax.set_facecolor("#f9f9f9")
    ax.grid(True, linestyle='--', alpha=0.3)

    # Rotolo e nucleo
    roll = plt.Circle((0, 0), R, fill=False, linewidth=2, edgecolor="#333")
    core = plt.Circle((0, 0), R * 0.3, fill=False, linestyle='--', linewidth=1.2, edgecolor="#666")
    ax.add_patch(roll)
    ax.add_patch(core)

    # Punto di chiusura del velo (punto fisso sul rullo) a 250°
    angle_target = np.radians(250)
    x_target = R * np.cos(angle_target)
    y_target = R * np.sin(angle_target)

    # Per far sì che il punto colla (inizialmente a 90°) si trovi nel punto target dopo la rotazione,
    # dobbiamo ruotare la bobina in avanti (senso orario) di un angolo θ = angolo tra 90° e 250° + (L / R)
    angle_colla = np.pi / 2  # 90° in radianti
    theta = (angle_target - angle_colla) % (2 * np.pi)  # angolo da ruotare per far combaciare la colla con il punto target

    # Colla iniziale a 90°
    x_colla_initial = R * np.cos(angle_colla)
    y_colla_initial = R * np.sin(angle_colla)

    # Dopo rotazione, la colla finisce nel punto target (che coincide con la fine del velo tagliato)
    # Visualizzazione del tratto di velo (che è in realtà ancora da tagliare)
    ax.plot([x_target - L, x_target], [y_target, y_target],
            color="#4caf50", linewidth=2.5, label='Velo che verrà tagliato (L)')

    # Punti colla
    ax.plot([x_colla_initial], [y_colla_initial], 'o', color="#e53935", markersize=8, label='Colla applicata (inizio @90°)')
    ax.plot([x_target], [y_target], 'o', color="#1e88e5", markersize=8, label='Colla dopo rotazione (posizione finale)')

    # Arco di rotazione θ (da 90° a 250°)
    arc = patches.Arc((0, 0), 2*R, 2*R, angle=0,
                      theta1=90,
                      theta2=250,
                      color='#ffa726', linewidth=2.5, label='Rotazione θ')
    ax.add_patch(arc)

    # Arco interno per θ
    arc_theta = patches.Arc((0, 0), 0.6*R, 0.6*R, angle=0,
                            theta1=90,
                            theta2=250,
                            color='blue', linewidth=1.5, linestyle='--')
    ax.add_patch(arc_theta)
    angle_label = (angle_colla + angle_target) / 2
    x_theta = 0.4 * R * np.cos(angle_label)
    y_theta = 0.4 * R * np.sin(angle_label)
    ax.text(x_theta, y_theta, 'θ', fontsize=14, color='blue', ha='center', va='center')

    # Etichette gradi
    for deg in [0, 90, 180, 210, 250, 270, 360]:
        angle_rad = np.radians(deg)
        x = (R + 20) * np.cos(angle_rad)
        y = (R + 20) * np.sin(angle_rad)
        ax.text(x, y, f"{deg}°", ha='center', va='center', fontsize=9, color='black')

    # Rulli
    rullo_raggio = 20
    rullo_offset_y = -R - 40
    distanza_rulli = 2 * R * 0.8
    ax.add_patch(plt.Circle((-distanza_rulli / 2, rullo_offset_y), rullo_raggio, color='#888'))
    ax.add_patch(plt.Circle((distanza_rulli / 2, rullo_offset_y), rullo_raggio, color='#888'))

    # Impostazioni finali
    ax.set_xlim(-R - 200, R + 200)
    ax.set_ylim(rullo_offset_y - 60, R + 120)
    ax.set_aspect('equal')
    ax.set_title(f"\u2728 Bobina Interattiva \u2728\nDiametro = {D:.0f} mm | Lunghezza Velo = {L:.0f} mm | Rotazione θ = {np.degrees(theta):.2f}°",
                 fontsize=13, fontweight='bold', color="#333")
    ax.legend(loc='upper right', frameon=True, framealpha=0.9)

    return fig

# Streamlit app
st.set_page_config(page_title="Bobina Interattiva", layout="centered")
st.title("🌀 Bobina Interattiva")

D = st.slider("Diametro della bobina (mm)", min_value=800, max_value=1200, value=1000, step=10)
L = st.slider("Lunghezza del velo (mm)", min_value=50, max_value=2000, value=1200, step=10)

fig = draw_roll(D, L)
st.pyplot(fig, use_container_width=True)

st.markdown(f"#### θ = {(250 - 90) % 360:.2f}° → Rotazione da applicare PRIMA del taglio per far combaciare la colla")
