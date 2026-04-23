import xml.etree.ElementTree as ET


def parse_time(time_str):
    """
    Converts 00:00:01:00 → seconds (approx)
    Format: HH:MM:SS:FF (frames optional)
    """
    try:
        parts = time_str.split(":")
        h = int(parts[0])
        m = int(parts[1])
        s = int(parts[2])
        return h * 3600 + m * 60 + s
    except:
        return 0


def parse_itt(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    subtitles = []

    # TTML namespace-safe parsing
    for p in root.iter():

        if p.tag.endswith("p"):

            text = "".join(p.itertext()).strip()

            begin = p.attrib.get("begin", "")
            end = p.attrib.get("end", "")

            # STYLE DETECTION
            raw_xml = ET.tostring(p, encoding="unicode")

            subtitles.append({
                "text": text,
                "start": parse_time(begin),
                "end": parse_time(end),
                "raw": raw_xml
            })

    return subtitles