import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from io import BytesIO
import base64
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

    # Punto colla (a ore 12)
    ax.plot([0], [R], 'ro', label='Colla')

    # Angolo di rotazione theta
    theta = 2 * L / D  # in radianti
    x_end = R * np.sin(-theta)
    y_end = R * np.cos(-theta)

    # Velo non ancora arrotolato
    ax.plot([0, x_end], [R, y_end], 'g-', linewidth=2, label='Estremità velo')

    ax.set_xlim(-R - 100, R + 100)
    ax.set_ylim(-R - 100, R + 100)
    ax.set_aspect('equal')
    ax.set_title(f"D = {D:.0f} mm, L = {L:.0f} mm\nθ = {np.degrees(theta):.2f} gradi")
    ax.legend()

    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return img_base64

# Streamlit app
st.title("Simulatore di rotazione rotolo carta igienica")

D = st.slider("Diametro D (mm)", min_value=800, max_value=1200, value=1000)
L = st.slider("Lunghezza L (mm)", min_value=50, max_value=600, value=300)

img_data = draw_roll(D, L)
st.image(f"data:image/png;base64,{img_data}", use_column_width=True)

st.markdown(f"### Angolo di rotazione: {np.degrees(2 * L / D):.2f} gradi")
