# sub-renamer

A small Python script that renames subtitle files (.srt) to match the corresponding video filenames in the same directory. It is useful when subtitle filenames don't match video filenames but both contain episode identifiers like `S01E02`, `1x02`, etc.

## Features

- Finds pairs of video and subtitle files by matching common episode patterns (e.g. `S01E02`, `s1e2`, `1x02`, `01X02`).
- Renames the subtitle file so it has the same basename as the video but with `.srt` extension.
- Prints every rename operation before performing it.

## Requirements

- Python 3.6+

## Usage

Run the script with the target directory as the only argument:

```bash
python main.py /path/to/directory
```

If you run it without an argument or with a path that is not a directory, the script prints usage and exits with a non-zero status.

## How it works

- The script scans the given directory for:
  - Video files (extensions configured in the script)
  - Subtitle files with `.srt` extension
- It uses this regular expression to detect season/episode segments in filenames:

```python
match_re = r'[sS]?(\d+)[eExX](\d+)'
```

This pattern matches filenames containing:
- Optional `s` or `S`, followed by a season number (captured as group 1),
- followed by `e`, `E`, `x`, or `X`, followed by an episode number (captured as group 2).

Examples matched:
- `Show.Name.S01E02.mkv` -> season `01`, episode `02`
- `show.s1e2.mp4` -> season `1`, episode `2`
- `Show.1x02.avi` -> season `1`, episode `02`

The script uses the episode number (group 2) as the key (leading zeros are stripped) to pair a subtitle with a video.

When a matching video is found for a subtitle, the subtitle is renamed to the video's basename plus `.srt`. The script prints each rename action:

```
Renaming /path/to/dir/old_subtitle.srt to /path/to/dir/Video.Name.S01E02.srt
```

Then it performs the rename.

## Supported video extensions

By default the script treats files ending with these extensions (case-insensitive) as videos:

- .mp4, .mkv, .avi, .mov, .wmv, .flv, .webm

You can change or extend this list by editing the `VIDEO_EXTENSIONS` constant in `main.py`.

