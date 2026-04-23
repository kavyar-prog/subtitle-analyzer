
---

# 🚀 Now FULL `app.py` (clean production version)

This is your final working version with:
# QC engine  
# ITT + SRT support  
# Highlighting  
# Sidebar dashboard  
# History system  

---

## 🟦 FULL APP.PY

```python id="app_final"
import streamlit as st
import os
import json

from parsers.srt_parser import parse_srt
from parsers.itt_parser import parse_itt
from analyzer.text_analysis import analyze_subtitles

from db import init_db, save_report, get_history


# -----------------------
# INIT DB
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

st.title("🎬 Subtitle QC Analyzer")


uploaded_file = st.file_uploader("Upload subtitle file", type=["srt", "itt"])


# -----------------------
# PROCESS FILE
# -----------------------
if uploaded_file:

    temp_path = "temp_file" + os.path.splitext(uploaded_file.name)[1]

    with open(temp_path, "wb") as f:
        f.write(uploaded_file.read())

    subtitles = parse_file(temp_path)
    report = analyze_subtitles(subtitles)

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
    # QC ISSUES (RED UI)
    # -----------------------
    st.subheader("❗ QC Issues")

    if report["issues"]:
        for issue in report["issues"]:

            if issue["type"] == "OVERLAP":
                st.error(f"OVERLAP between {issue['index']} and {issue['next_index']}")

            elif issue["type"] == "LONG_LINE":
                st.warning(f"LONG LINE: {issue['text']}")

            elif issue["type"] == "EMPTY_SUBTITLE":
                st.error(f"EMPTY subtitle at {issue['index']}")

    else:
        st.success("No QC issues found 🎉")


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
# HISTORY
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