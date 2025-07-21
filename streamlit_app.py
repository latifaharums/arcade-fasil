import streamlit as st
import pandas as pd
import plotly.express as px

# Page setup
st.set_page_config(
    page_title="Dashboard Fasilitator Latifah Arum S",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Logo & Branding
st.markdown(
    """
    <div style="display:flex; align-items:center; gap:10px;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg" width="40">
        <img src="https://dicoding-web-img.sgp1.cdn.digitaloceanspaces.com/original/academy/logo-academy.png" width="90">
        <h1 style="display:inline; color:#4CAF50;">Dashboard Fasilitator</h1>
    </div>
    <h3 style="color:gray;">Latifah Arum S</h3>
    """,
    unsafe_allow_html=True
)

# Upload dataset
st.sidebar.title("📂 Upload Data Peserta")
data_file = st.sidebar.file_uploader("Upload file CSV/Excel", type=["csv", "xlsx"])

if data_file is not None:
    if data_file.name.endswith(".csv"):
        df = pd.read_csv(data_file)
    else:
        df = pd.read_excel(data_file)

    # Total Perolehan
    total_point = df["Total Point"].sum()
    total_peserta = df.shape[0]
    sudah_redeem = df[df["Redeem Status"] == "Sudah"].shape[0]
    sang_penguasa = df.sort_values(by="Total Point", ascending=False).iloc[0]

    # Layout 4 kolom statistik
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💎 Total Perolehan", f"{total_point:,} Point")
    col2.metric("👥 Total Peserta", total_peserta)
    col3.metric("🎁 Sudah Redeem Credit", sudah_redeem)
    col4.metric("👑 Sang Penguasa", sang_penguasa["Nama Peserta"])

    # Milestone Chart
    st.subheader("📈 Laporan Pencapaian Milestone")
    fig = px.bar(
        df,
        x="Nama Peserta",
        y="Milestone (%)",
        color="Milestone (%)",
        color_continuous_scale="Viridis",
        title="Pencapaian Milestone Setiap Peserta"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Leaderboard
    st.subheader("🏆 Leaderboard (Top 5)")
    leaderboard = df.sort_values(by="Total Point", ascending=False).head(5)
    st.table(leaderboard[["Nama Peserta", "Total Point"]])

else:
    st.info("⬅️ Upload data peserta untuk melihat dashboard.")
