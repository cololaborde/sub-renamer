from os import path as os_path, listdir as os_listdir, rename as os_rename
from sys import argv as sys_argv, exit as sys_exit
from re import search as re_search

VIDEO_EXTENSIONS = [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"]

if __name__ == "__main__":
    directory = sys_argv[1] if len(sys_argv) > 1 else None
    preview = sys_argv[2] if len(sys_argv) > 2 and sys_argv[2] == "--preview" else False
    
    if not directory or not os_path.isdir(directory):
        print("Usage: python main.py <directory>")
        sys_exit(1)

    srt_filenames = {}
    video_filenames = {}
    match_re = r'[sS]?(\d+)[eExX](\d+)'

    for filename in os_listdir(directory):
        if filename.lower().endswith(".srt"):
            matched_chapter_number_srt = re_search(match_re, filename)
            if matched_chapter_number_srt:
                chapter_number_srt = matched_chapter_number_srt.group(2).strip().lstrip('0')
                srt_filenames[chapter_number_srt] = filename

        if filename.lower().endswith(tuple(VIDEO_EXTENSIONS)):
            matched_chapter_number = re_search(match_re, filename)
            if matched_chapter_number:
                chapter_number = matched_chapter_number.group(2).strip().lstrip('0')
                video_filenames[chapter_number] = filename

    for srt_chapter, srt_filename in srt_filenames.items():
        str_full_path = f"{directory}{"/" if not directory.endswith("/") else ""}{srt_filename}"
        video_filename = video_filenames.get(srt_chapter)
        if not video_filename:
            continue
        video_full_path = f"{directory}{"/" if not directory.endswith("/") else ""}{video_filename}"
        extension = f".{video_filename.split('.')[-1]}"
        new_str_full_path = f"{video_full_path.replace(extension, '.srt')}"
        print(f"Renaming {str_full_path} to {new_str_full_path}")
        if not preview:
            os_rename(str_full_path, new_str_full_path)
        else:
            user_input = input("Confirm? (y/n): ")
            if user_input.lower() == "n":
                continue
            os_rename(str_full_path, new_str_full_path)
