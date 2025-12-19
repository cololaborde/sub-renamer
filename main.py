import os
import sys
from re import search as re_search

VIDEO_EXTENSIONS = [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"]

if __name__ == "__main__":
    srt_filenames = []
    video_filenames = []
    
    directory = sys.argv[1]
    for filename in os.listdir(directory):
        if filename.lower().endswith(".srt"):
            srt_filenames.append(filename)
        if filename.lower().endswith(tuple(VIDEO_EXTENSIONS)):
            video_filenames.append(filename)

    for video_filename in video_filenames:
        match_re = r'[sS]?(\d+)[eExX](\d+)'
        matched_chapter_number = re_search(match_re, video_filename)
        if matched_chapter_number:
            chapter_number = matched_chapter_number.group(2).strip().lstrip('0')
        
        for srt_filename in srt_filenames:
            matched_chapter_number_srt = re_search(match_re, srt_filename)
            if matched_chapter_number_srt:
                chapter_number_srt = matched_chapter_number_srt.group(2).strip().lstrip('0')
                if chapter_number == chapter_number_srt:
                    str_full_path = f"{directory}{"/" if not directory.endswith("/") else ""}{srt_filename}"
                    video_full_path = f"{directory}{"/" if not directory.endswith("/") else ""}{video_filename}"
                    extension = f".{video_filename.split('.')[-1]}"
                    new_str_full_path = f"{video_full_path.replace(extension, '.srt')}"
                    print(f"Renaming {str_full_path} to {new_str_full_path}")
                    os.rename(str_full_path, new_str_full_path)
                    break
