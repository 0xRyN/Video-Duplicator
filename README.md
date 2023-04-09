# Steps to use

## Install Homebrew

To install Homebrew, run this command

`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

## Install FFMpeg

To install FFMpeg, run this command

`brew install ffmpeg`

## Install FFMpeg-Python

To install FFMpeg-Python, run this command

`pip install ffmpeg-python`

## Install tqdm

To install tqdm, run this command

`pip install tqdm`

## Runnning the script

Place the videos in the "videos" folder - create it if needed. Then run the script.

`python3 main.py`

## Output

The output will be in the "output" folder - create it if needed.

The script will change the name, metadata and apply filters to the video.

# Notes

Zoomed video output : videoname_z_factor.mp4
Flipped video output : videoname_f.mp4
Original video re-processed : videoname_o.mp4
