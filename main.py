from os import path as os_path, listdir as os_listdir, rename as os_rename
from sys import argv as sys_argv, exit as sys_exit
from re import search as re_search

VIDEO_EXTENSIONS = [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"]
SUB_EXTENSIONS = [".srt", ".ass", ".ssa", ".vtt", ".sub"]

MATCH_RE = r'[sS]?(\d+)[eExX](\d+)'

def group_files_by_chaper(directory):

    def get_chapter(extensions):
        if not filename.lower().endswith(tuple(extensions)) or \
           not (match := re_search(MATCH_RE, filename)) or \
           not (chapter := match.group(2).strip().lstrip('0')):
            return None
        return chapter

    srt, video = {}, {}
    for filename in os_listdir(directory):
        if sub_chapter := get_chapter(SUB_EXTENSIONS):
            srt[sub_chapter] = filename
        elif video_chapter := get_chapter(VIDEO_EXTENSIONS):
            video[video_chapter] = filename
        else:
            continue
    return srt, video

if __name__ == "__main__":
    directory = sys_argv[1] if len(sys_argv) > 1 else None
    preview = sys_argv[2] if len(sys_argv) > 2 and sys_argv[2] == "--preview" else False
    
    if not directory or not os_path.isdir(directory):
        print("Usage: python main.py <directory>")
        sys_exit(1)

    srt_filenames, video_filenames = group_files_by_chaper(directory)

    for srt_chapter, srt_filename in srt_filenames.items():
        sub_extension = f".{srt_filename.split('.')[-1]}"
        str_full_path = f"{directory}{"/" if not directory.endswith("/") else ""}{srt_filename}"
        video_filename = video_filenames.get(srt_chapter)
        if not video_filename:
            continue
        video_full_path = f"{directory}{"/" if not directory.endswith("/") else ""}{video_filename}"
        extension = f".{video_filename.split('.')[-1]}"
        new_str_full_path = f"{video_full_path.replace(extension, sub_extension)}"
        print(f"Renaming {str_full_path} to {new_str_full_path}")
        if not preview:
            os_rename(str_full_path, new_str_full_path)
        else:
            user_input = input("Confirm? (y/n): ")
            if user_input.lower() == "n":
                continue
            os_rename(str_full_path, new_str_full_path)
