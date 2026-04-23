def parse_srt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = content.strip().split("\n\n")
    subtitles = []

    for block in blocks:
        lines = block.split("\n")

        if len(lines) >= 3:
            subtitles.append({
                "index": lines[0],
                "timecode": lines[1],
                "text": " ".join(lines[2:])
            })

    return subtitles