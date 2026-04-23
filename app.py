import streamlit as st
import os
import json
import uuid

from parsers.srt_parser import parse_srt
from parsers.itt_parser import parse_itt
from analyzer.text_analysis import analyze_subtitles

from db import init_db, save_report, get_history


# -----------------------
# INIT DATABASE
# -----------------------
init_db()


# -----------------------
# FILE ROUTER
# -----------------------
def parse_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".srt":
        return parse_srt(file_path)

    elif ext == ".itt":
        return parse_itt(file_path)

    else:
        raise ValueError("Unsupported format")


# -----------------------
# UI CONFIG
# -----------------------
st.set_page_config(page_title="Subtitle QC Tool", layout="wide")

st.title("🎬 Subtitle QC Analyzer (SRT + ITT)")


uploaded_file = st.file_uploader("Upload subtitle file", type=["srt", "itt"])


# -----------------------
# PROCESS FILE
# -----------------------
if uploaded_file is not None:

    # Safe unique temp file (avoids conflicts)
    temp_path = f"temp_{uuid.uuid4()}{os.path.splitext(uploaded_file.name)[1]}"

    with open(temp_path, "wb") as f:
        f.write(uploaded_file.read())

    # Parse + analyze
    subtitles = parse_file(temp_path)
    report = analyze_subtitles(subtitles)

    # Save to history DB
    save_report(uploaded_file.name, report)


    # -----------------------
    # SIDEBAR DASHBOARD
    # -----------------------
    st.sidebar.title("QC Summary")

    st.sidebar.metric("Total Subtitles", report["total_subtitles"])
    st.sidebar.metric("Issues", len(report["issues"]))
    st.sidebar.metric("Language", report["overall_language"])


    # -----------------------
    # MAIN REPORT
    # -----------------------
    st.subheader("📊 Analysis Report")
    st.json(report)


    # -----------------------
    # QC ISSUES
    # -----------------------
    st.subheader("❗ QC Issues")

    if report["issues"]:

        for issue in report["issues"]:

            if issue["type"] == "OVERLAP":
                st.error(
                    f"OVERLAP between {issue['index']} and {issue['next_index']} "
                    f"(end {issue['curr_end']} → start {issue['next_start']})"
                )

            elif issue["type"] == "LONG_LINE":
                st.warning(f"LONG LINE: {issue['text']}")

            elif issue["type"] == "EMPTY_SUBTITLE":
                st.error(f"EMPTY subtitle at index {issue['index']}")

            else:
                st.info(issue)

    else:
        st.success("🎉 No QC issues found")


    # -----------------------
    # SUBTITLE VIEWER
    # -----------------------
    st.subheader("📝 Subtitle Viewer")

    for sub in subtitles:

        text = sub["text"]

        if sub.get("italic"):
            st.markdown(f"🟡 *ITALIC:* {text}")

        elif sub.get("bold"):
            st.markdown(f"🔵 **BOLD:** {text}")

        else:
            st.write(text)


# -----------------------
# HISTORY SECTION
# -----------------------
st.divider()
st.subheader("📚 History")

history = get_history()

if history:

    for filename, timestamp, report_json in history:

        with st.expander(f"{filename} - {timestamp}"):
            st.json(json.loads(report_json))

else:
    st.info("No history yet")