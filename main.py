from os import path as os_path, listdir as os_listdir, rename as os_rename, walk as os_walk
from sys import exit as sys_exit
from re import search as re_search
from utils import get_args

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

def rename_files(dir_full_path):
    srt_filenames, video_filenames = group_files_by_chaper(dir_full_path)
    for srt_chapter, srt_filename in srt_filenames.items():
        sub_extension = f".{srt_filename.split('.')[-1]}"
        str_full_path = f"{dir_full_path}{"/" if not dir_full_path.endswith("/") else ""}{srt_filename}"
        video_filename = video_filenames.get(srt_chapter)
        if not video_filename:
            continue
        video_full_path = f"{dir_full_path}{"/" if not dir_full_path.endswith("/") else ""}{video_filename}"
        extension = f".{video_filename.split('.')[-1]}"
        new_str_full_path = f"{video_full_path.replace(extension, sub_extension)}"
        if not no_log:
            print(f"Renaming {str_full_path} to {new_str_full_path}")
        if not preview:
            os_rename(str_full_path, new_str_full_path)
        else:
            user_input = input("Confirm? (y/n): ")
            if user_input.lower() == "n":
                continue
            os_rename(str_full_path, new_str_full_path)

if __name__ == "__main__":
    recursive, preview, no_log, directory_list = get_args()

    if recursive:
        for super_dir in directory_list:
            for root, dirs, files in os_walk(super_dir):
                rename_files(root)
                for directory in dirs:
                    dir_full_path = f"{root}{"/" if not root.endswith("/") else ""}{directory}"
                    rename_files(dir_full_path)
    else:
        for directory in directory_list:
            rename_files(directory)
