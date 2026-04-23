import streamlit as st
import os
import json

from parsers.srt_parser import parse_srt
from parsers.itt_parser import parse_itt
from analyzer.text_analysis import analyze_subtitles

from db import init_db, save_report, get_history


# ---------------------------
# INIT DATABASE
# ---------------------------
init_db()


# ---------------------------
# PARSER ROUTER
# ---------------------------
def parse_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".srt":
        return parse_srt(file_path)

    elif ext == ".itt":
        return parse_itt(file_path)

    else:
        raise ValueError("Unsupported file format")


# ---------------------------
# STREAMLIT UI
# ---------------------------
st.set_page_config(page_title="Subtitle QC Tool", layout="wide")

st.title("🎬 Subtitle QC Analyzer (SRT + ITT)")

uploaded_file = st.file_uploader(
    "Upload subtitle file",
    type=["srt", "itt"]
)


# ---------------------------
# MAIN PROCESSING
# ---------------------------
if uploaded_file is not None:

    temp_path = "temp_file" + os.path.splitext(uploaded_file.name)[1]

    with open(temp_path, "wb") as f:
        f.write(uploaded_file.read())

    # Parse + Analyze
    subtitles = parse_file(temp_path)
    report = analyze_subtitles(subtitles)

    # Save to DB
    save_report(uploaded_file.name, report)

    # ---------------------------
    # REPORT SECTION
    # ---------------------------
    st.subheader("📊 Analysis Report")
    st.json(report)

    # ---------------------------
    # QC ISSUES (RED HIGHLIGHTS)
    # ---------------------------
    st.subheader("❗ QC Issues")

    issues = report.get("issues", [])

    if issues:

        for issue in issues:

            if issue["type"] == "OVERLAP":
                st.error(
                    f"⚠ OVERLAP detected between subtitle {issue['index']} "
                    f"and {issue['next_index']} "
                    f"(end={issue['curr_end']} → start={issue['next_start']})"
                )

            elif issue["type"] == "EMPTY_SUBTITLE":
                st.error(f"❌ EMPTY subtitle at index {issue['index']}")

            elif issue["type"] == "LONG_LINE":
                st.warning(
                    f"⚠ LONG LINE at index {issue['index']}: {issue['text']}"
                )

            else:
                st.info(issue)

    else:
        st.success("🎉 No QC issues found")


    # ---------------------------
    # PREVIEW
    # ---------------------------
    st.subheader("📝 Subtitle Preview")

    st.dataframe(subtitles[:10])


# ---------------------------
# HISTORY SECTION
# ---------------------------
st.divider()
st.subheader("📚 History (Previous Analyses)")

history = get_history()

if history:

    for item in history:
        filename, timestamp, report_json = item

        with st.expander(f"{filename} — {timestamp}"):

            st.json(json.loads(report_json))

else:
    st.info("No history available yet")