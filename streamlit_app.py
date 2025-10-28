# streamlit_app.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random, math
from io import BytesIO

st.set_page_config(page_title="Generative Poster", page_icon="🎨", layout="centered")

# ---------- Core functions ----------
def random_palette(k=5, pastel=True, seed=None):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
    cols = []
    for _ in range(k):
        # 生成低饱和度、偏柔和的颜色
        r, g, b = np.random.rand(3)
        if pastel:
            r = 0.6*r + 0.4
            g = 0.6*g + 0.4
            b = 0.6*b + 0.4
        cols.append((float(r), float(g), float(b)))
    return cols

def blob(center=(0.5, 0.5), r=0.3, points=200, wobble=0.15):
    angles = np.linspace(0, 2*math.pi, points)
    radii = r * (1 + wobble*(np.random.rand(points)-0.5))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

def draw_poster(seed, bg_color, k_palette, n_layers, points, wobble_min, wobble_max,
                r_min, r_max, alpha_min, alpha_max, label_on=True):
    random.seed(seed)
    np.random.seed(seed)

    fig = plt.figure(figsize=(7,10), dpi=200)
    ax = plt.gca()
    ax.set_aspect("equal")
    ax.axis('off')
    ax.set_facecolor(bg_color)

    palette = random_palette(k=k_palette, pastel=True, seed=seed)
    for _ in range(n_layers):
        cx, cy = random.random(), random.random()
        rr = random.uniform(r_min, r_max)
        x, y = blob(center=(cx, cy), r=rr, points=points, wobble=random.uniform(wobble_min, wobble_max))
        color = random.choice(palette)
        alpha = random.uniform(alpha_min, alpha_max)
        plt.fill(x, y, color=color, alpha=alpha, edgecolor=(0,0,0,0))

    if label_on:
        ax.text(0.05, 0.95, "Generative Poster", fontsize=18, weight='bold', transform=ax.transAxes)
        ax.text(0.05, 0.91, "Week 2 • Arts & Advanced Big Data", fontsize=11, transform=ax.transAxes)

    ax.set_xlim(0,1); ax.set_ylim(0,1)
    plt.tight_layout(pad=0)
    return fig

# ---------- UI ----------
st.title("🎨 Generative Poster (Matplotlib + Streamlit)")
st.caption("Move the sliders and click **Generate** to create new posters. Download as PNG below.")

with st.sidebar:
    st.header("Controls")
    seed = st.number_input("Seed", min_value=0, max_value=999999, value=42, step=1)
    if st.button("🔀 Shuffle seed"):
        seed = random.randint(0, 999999)
        st.experimental_rerun()

    bg_color = st.color_picker("Background", value="#FAFAF7")
    n_layers = st.slider("Layers", 3, 30, 8)
    k_palette = st.slider("Palette size", 3, 12, 6)
    points = st.slider("Points per shape", 80, 600, 220, step=10)
    wobble_min, wobble_max = st.slider("Wobble range", 0.00, 0.50, (0.05, 0.25), step=0.01)
    r_min, r_max = st.slider("Radius range", 0.05, 0.60, (0.15, 0.45), step=0.01)
    alpha_min, alpha_max = st.slider("Alpha range", 0.05, 1.00, (0.25, 0.60), step=0.01)
    label_on = st.checkbox("Show label text", True)
    generate = st.button("🎉 Generate")

if generate or True:
    fig = draw_poster(
        seed=seed, bg_color=bg_color, k_palette=k_palette, n_layers=n_layers,
        points=points, wobble_min=wobble_min, wobble_max=wobble_max,
        r_min=r_min, r_max=r_max, alpha_min=alpha_min, alpha_max=alpha_max,
        label_on=label_on
    )
    st.pyplot(fig, clear_figure=True)

    # Download button
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches="tight", pad_inches=0)
    st.download_button("⬇️ Download PNG", data=buf.getvalue(), file_name="poster.png", mime="image/png")
