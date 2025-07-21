import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PyPDF2 import PdfReader

# Konfigurasi halaman
st.set_page_config(
    page_title="Progress Arcade Fasil 2025",
    page_icon="📑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Logo dan Header
st.markdown(
    """
    <div style="display:flex; align-items:center; gap:10px;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg" width="40">
        <img src="https://dicoding-web-img.sgp1.cdn.digitaloceanspaces.com/original/academy/logo-academy.png" width="90">
        <h1 style="display:inline; color:#4CAF50;">Arclatori Pro</h1>
    </div>
    <h3 style="color:gray;">by Fasilitator Latifah Arum S</h3>
    """,
    unsafe_allow_html=True
)

# Sidebar
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg", width=50)
st.sidebar.image("https://dicoding-web-img.sgp1.cdn.digitaloceanspaces.com/original/academy/logo-academy.png", width=120)
st.sidebar.title("📂 Upload File")
uploaded_file = st.sidebar.file_uploader(
    "Upload file (CSV, Excel, TXT, PDF, Images)",
    type=["csv", "xlsx", "txt", "pdf", "png", "jpg", "jpeg"]
)

st.sidebar.markdown("---")
st.sidebar.header("⚙️ Pilihan Analisis")
analysis_option = st.sidebar.selectbox(
    "Pilih jenis analisis",
    ["Auto Detect", "Preview Data", "Descriptive Stats", "Generate WordCloud", "Extract PDF Text"]
)

st.sidebar.markdown("---")
theme = st.sidebar.radio("🎨 Tema", ["Light", "Dark"])

st.sidebar.markdown(
    """
    <hr>
    <p style="text-align:center; color:gray;">
    Made with ❤️ by <b>Fasilitator Latifah Arum S</b>
    </p>
    """, unsafe_allow_html=True
)

# Ganti tema warna
if theme == "Dark":
    st.markdown(
        """
        <style>
        body {
            background-color: #1e1e1e;
            color: #f1f1f1;
        }
        </style>
        """, unsafe_allow_html=True
    )

# Main Logic
if uploaded_file is not None:
    file_info = {
        "Filename": uploaded_file.name,
        "File Type": uploaded_file.type,
        "File Size": f"{uploaded_file.size / 1024:.2f} KB"
    }
    st.sidebar.markdown("### 📝 File Info")
    st.sidebar.json(file_info)

    file_name = uploaded_file.name.lower()

    if "csv" in file_name or "xlsx" in file_name:
        # Load data
        if file_name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        if analysis_option in ["Auto Detect", "Preview Data"]:
            st.subheader("👀 Data Preview")
            st.dataframe(df)
        if analysis_option in ["Auto Detect", "Descriptive Stats"]:
            st.subheader("📊 Descriptive Statistics")
            st.write(df.describe())

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Processed CSV",
            data=csv,
            file_name="processed_data.csv",
            mime="text/csv"
        )

    elif "txt" in file_name or "pdf" in file_name:
        # Handle text and PDFs
        text_content = ""
        if file_name.endswith(".txt"):
            text_content = str(uploaded_file.read(), "utf-8")
        elif file_name.endswith(".pdf"):
            reader = PdfReader(uploaded_file)
            for page in reader.pages:
                text_content += page.extract_text()

        if analysis_option in ["Auto Detect", "Extract PDF Text"]:
            st.subheader("📄 Extracted Text")
            st.text_area("Hasil Ekstraksi:", text_content, height=300)

        if analysis_option in ["Auto Detect", "Generate WordCloud"]:
            st.subheader("☁️ Word Cloud")
            wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text_content)
            fig, ax = plt.subplots()
            ax.imshow(wordcloud, interpolation="bilinear")
            ax.axis("off")
            st.pyplot(fig)

        st.download_button(
            label="📥 Download Extracted Text",
            data=text_content,
            file_name="extracted_text.txt",
            mime="text/plain"
        )

    else:
        st.warning("❗ Format file gambar belum diimplementasikan untuk analisis.")

else:
    st.info("⬅️ Upload file melalui sidebar untuk memulai analisis.")

# Footer Branding
st.markdown(
    """
    <hr>
    <p style="text-align:center; color:gray;">
    © 2025 Fasilitator Latifah Arum S • <a href="https://linkedin.com" target="_blank">LinkedIn</a> | <a href="https://github.com" target="_blank">GitHub</a>
    </p>
    """, unsafe_allow_html=True
)
