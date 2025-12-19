import os
import sys
from re import search as re_search
video_extensions = [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"]

if __name__ == "__main__":
    srt_filenames = []
    video_filenames = []
    
    directory = sys.argv[1]
    for filename in os.listdir(directory):
        if filename.endswith(".srt"):
            srt_filenames.append(filename)
        if filename.endswith(tuple(video_extensions)):
            video_filenames.append(filename)

    for video_filename in video_filenames:
        matched_chapter_number = re_search(r'[Ss](\d+)[Ee](\d+)', video_filename)
        if matched_chapter_number:
            chapter_number = matched_chapter_number.group(2)
        
        for srt_filename in srt_filenames:
            matched_chapter_number_srt = re_search(r'[Ss](\d+)[Ee](\d+)', srt_filename)
            if matched_chapter_number_srt:
                chapter_number_srt = matched_chapter_number_srt.group(2)
                if chapter_number == chapter_number_srt:
                    str_full_path = f"{directory}/{srt_filename}"
                    video_full_path = f"{directory}/{video_filename}"
                    extension = f".{video_filename.split('.')[-1]}"
                    new_str_full_path = f"{video_full_path.replace(extension, '.srt')}"
                    print(str_full_path)
                    print(new_str_full_path)
                    os.rename(str_full_path, new_str_full_path)