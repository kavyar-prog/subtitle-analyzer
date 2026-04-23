from langdetect import detect, LangDetectException
import re


# ----------------------------
# STYLE DETECTION HELPERS
# ----------------------------

def detect_italic(raw_xml):
    return "<i>" in raw_xml or "fontStyle=\"italic\"" in raw_xml


def detect_bold(raw_xml):
    return "<b>" in raw_xml or "fontWeight=\"bold\"" in raw_xml


def detect_colors(raw_xml):
    return re.findall(r'color="([^"]+)"', raw_xml)


def find_special_characters(text):
    return re.findall(r"[^\x00-\x7F]", text)


def find_tags(text):
    return re.findall(r"<[^>]+>", text)


# ----------------------------
# LANGUAGE DETECTION
# ----------------------------

def detect_language(text):
    try:
        return detect(text)
    except LangDetectException:
        return "unknown"


# ----------------------------
# MAIN ANALYZER
# ----------------------------

def analyze_subtitles(subtitles):

    issues = []
    all_colors = []
    all_tags = []
    special_chars = []
    full_text = ""

    # ------------------------
    # SINGLE SUBTITLE CHECK
    # ------------------------
    for i, sub in enumerate(subtitles):

        text = sub.get("text", "")
        raw = sub.get("raw", "")

        start = sub.get("start", None)
        end = sub.get("end", None)

        full_text += " " + text

        # ------------------------
        # STYLE DETECTION
        # ------------------------
        italic = detect_italic(raw)
        bold = detect_bold(raw)
        colors = detect_colors(raw)

        sub["italic"] = italic
        sub["bold"] = bold
        sub["colors"] = colors

        all_colors.extend(colors)

        # ------------------------
        # QC RULES
        # ------------------------

        # Empty subtitle
        if not text.strip():
            issues.append({
                "type": "EMPTY_SUBTITLE",
                "index": i
            })

        # Long line check
        if len(text) > 42:
            issues.append({
                "type": "LONG_LINE",
                "text": text,
                "index": i
            })

        # Tag extraction (from raw XML/text)
        all_tags.extend(find_tags(raw))

        # Special characters
        special_chars.extend(find_special_characters(text))

    # ----------------------------
    # OVERLAP DETECTION
    # ----------------------------
    for i in range(len(subtitles) - 1):

        curr = subtitles[i]
        nxt = subtitles[i + 1]

        if (
            curr.get("end") is not None and
            nxt.get("start") is not None
        ):

            if curr["end"] > nxt["start"]:
                issues.append({
                    "type": "OVERLAP",
                    "index": i,
                    "next_index": i + 1,
                    "curr_end": curr["end"],
                    "next_start": nxt["start"]
                })

    # ----------------------------
    # LANGUAGE DETECTION
    # ----------------------------
    lang = detect_language(full_text)

    # ----------------------------
    # FINAL REPORT
    # ----------------------------
    return {
        "total_subtitles": len(subtitles),
        "issues": issues,
        "unique_tags": list(set(all_tags)),
        "unique_special_characters": list(set(special_chars)),
        "colors_used": list(set(all_colors)),
        "overall_language": lang
    }