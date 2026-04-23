from parsers.srt_parser import parse_srt
from analyzer.text_analysis import analyze_subtitles

file_path = "samples/sample.srt"

subtitles = parse_srt(file_path)

report = analyze_subtitles(subtitles)

print("\n--- ANALYSIS REPORT ---")
print(report)