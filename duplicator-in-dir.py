import os
import ffmpeg
import random
from tqdm import tqdm
import time

KEYWORDS = [
    "becomingafemmefatale",
    "femmefatale",
    "seduction",
    "manipulation",
    "viral",
    "power",
    "foryou",
    "fyp",
    "darkfeminine",
    "darkfemininity",
    "darkfeminineenergy",
    "darkfemme",
    "maneater",
    "confidence",
    "siren",
    "learnontiktok",
]


def get_metadata_dict(video_keywords_str):
    metadata_title = video_keywords_str.replace("_", " ")
    metadata_description = "#" + video_keywords_str.replace("_", " #")
    metadata_keywords = video_keywords_str.replace("_", ",")

    metadata_dict = {
        "metadata:g:0": f"title={metadata_title}",
        "metadata:g:1": f"description={metadata_description}",
        "metadata:g:2": f"keywords={metadata_keywords}",
    }
    return metadata_dict


def get_unique_name_and_metadata(str_effect=""):
    """Generate a unique name for the video

    Args:
        str_effect (str, optional): String to append to the name related to the effect. Defaults to "".

    Returns:
        str: Unique name for the video
    """

    video_keywords = random.sample(KEYWORDS, 5)
    unique_hash = random.randint(10000000, 99999999)
    video_keywords_str = "_".join(video_keywords)
    file_name = f"{unique_hash}_{video_keywords_str}_{str_effect}.mp4"

    metadata_dict = get_metadata_dict(video_keywords_str)

    return file_name, metadata_dict


def get_video_dimensions(path):
    """Get the dimensions of the video

    Args:
        path (str): Path to the video

    Returns:
        tuple: Height, Width dimensions of the video
    """
    probe = ffmpeg.probe(path)
    video_stream = next(
        (stream for stream in probe["streams"] if stream["codec_type"] == "video"), None
    )
    width = int(video_stream["width"])
    height = int(video_stream["height"])
    return width, height


def zoom_video(path, factor_percent=110):
    """Zoom in the video by a factor of factor_percent

    Args:
        path (str): Path to the video
        factor_percent (int, optional): Zoom factor. Defaults to 110.

    Returns:
        bool: True if the video was successfully processed, False otherwise
    """

    factor_str = str(factor_percent)
    video_name, metadata = get_unique_name_and_metadata(f"z_{factor_str}")
    parent_dir = os.path.dirname(path)
    res_file_name = os.path.join(parent_dir, video_name)
    try:
        width, height = get_video_dimensions(path)
        (
            ffmpeg.input(path)
            .filter("scale", w=width * (factor_percent / 100), h=-1)
            .filter("crop", w=width, h=height)
            .output(
                res_file_name,
                loglevel="quiet",
                map_metadata=-1,
                **metadata,
            )
            .run()
        )
        return True
    except ffmpeg.Error as e:
        print(e.stderr)
        return False


def flip_video(path):
    """Flip the video horizontally

    Args:
        path (str): Path to the video

    Returns:
        bool: True if the video was successfully processed, False otherwise
    """

    # Flip is done after zooming, so we take the original video name and append the effect
    processed_video_name = os.path.basename(path)
    processed_video_effect = processed_video_name.split("_")[-1].split(".")[0]
    video_name, metadata = get_unique_name_and_metadata(f"{processed_video_effect}_f")
    parent_dir = os.path.dirname(path)
    res_file_name = os.path.join(parent_dir, video_name)
    try:
        (
            ffmpeg.input(path)
            .filter("hflip")
            .output(
                res_file_name,
                loglevel="quiet",
                map_metadata=-1,
                **metadata,
            )
            .run()
        )
        return True
    except ffmpeg.Error as e:
        print(e.stderr)
        return False


def copy_video(path):
    """Copy the video

    Args:
        path (str): Path to the video

    Returns:
        bool: True if the video was successfully processed, False otherwise
    """

    video_name, metadata = get_unique_name_and_metadata("o")
    parent_dir = os.path.dirname(path)
    res_file_name = os.path.join(parent_dir, video_name)
    try:
        (
            ffmpeg.input(path)
            .output(
                res_file_name,
                loglevel="quiet",
                map_metadata=-1,
                **metadata,
            )
            .run()
        )
        return True
    except ffmpeg.Error as e:
        print(e.stderr)
        return False


def process_dir(path):
    """Process the videos in a directory

    Args:
        path (str): Path to the directory
    """
    print(f"Processing directory {path}...")

    print("Step 1. Zooming videos...")
    videos_to_process = os.listdir(path)
    for video in tqdm(videos_to_process):
        video_path = os.path.join(path, video)
        copy_video(video_path)
        zoom_video(video_path, factor_percent=105)
        zoom_video(video_path, factor_percent=110)
        os.remove(video_path)

    print("Step 2. Flipping videos...")
    videos_to_process = os.listdir(path)
    for video in tqdm(videos_to_process):
        video_path = os.path.join(path, video)
        flip_video(video_path)


def walk():
    # Will walk on the videos
    for dirpath, dirnames, filenames in os.walk("videos"):
        # Check if .mp4 files. If so, send it to the processing function
        for file in filenames:
            if file.lower().endswith(".mp4"):
                process_dir(dirpath)
                break


def main():
    print("Starting...")
    walk()


if __name__ == "__main__":
    main()
