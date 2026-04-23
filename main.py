import os
from parsers.srt_parser import parse_srt
from parsers.itt_parser import parse_itt

def parse_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".srt":
        return parse_srt(file_path)

    elif ext == ".itt":
        return parse_itt(file_path)

    else:
        raise ValueError("Unsupported format")