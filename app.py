import streamlit as st
from parsers.srt_parser import parse_srt
from analyzer.text_analysis import analyze_subtitles
import tempfile

st.title("Subtitle Analyzer Tool")

st.write("Upload an SRT file to analyze tags, characters, and language.")

uploaded_file = st.file_uploader("Choose a subtitle file", type=["srt"])

if uploaded_file is not None:
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".srt") as tmp:
        tmp.write(uploaded_file.read())
        temp_path = tmp.name

    # Run pipeline
    subtitles = parse_srt(temp_path)
    report = analyze_subtitles(subtitles)

    st.subheader("Analysis Report")
    st.json(report)

    st.subheader("Raw Subtitles Preview")
    st.write(subtitles[:5])