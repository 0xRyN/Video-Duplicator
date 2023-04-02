import ffmpeg
import os

DIR = "videos"

# The goal of this script is to process a video and to make multiple variants of it.
# The variants are slightly different versions of the original video to make it undetectable by the algorithm.
# The variants should not affect the quality of the video and should be as close as possible to the original video.
# The variants are:
# - zoom in the video
# - Flip horizontally
# - Add noise
# - Add saturation
# - Add contrast
# - Add brightness
# - Add sharpness
# - Add hue
# - Add gamma


# Slightly zoom in the video, no animation
# Zooming is a two step process. You want to:

# zoom the video by a 1.1x factor.
# Crop the video back to its original size.


def zoom_video(path, factor_percent=110):
    factor_str = str(factor_percent) + "%"
    res_file_name = path.replace(".mp4", f"_zoomed_{factor_str}.mp4")
    try:
        # First, get the video's width and height
        probe = ffmpeg.probe(path)
        video_stream = next(
            (stream for stream in probe["streams"] if stream["codec_type"] == "video"),
            None,
        )
        input_video_width = int(video_stream["width"])
        input_video_height = int(video_stream["height"])
        (
            ffmpeg.input(path)
            .filter("scale", w=input_video_width * (factor_percent / 100), h=-1)
            .filter("crop", w=input_video_width, h=input_video_height)
            .output(res_file_name, map_metadata=-1)
            .run()
        )
        return True
    except ffmpeg.Error as e:
        print(e.stderr)
        return False


# - Flip horizontally


def flip_video(path):
    try:
        (
            ffmpeg.input(path)
            .filter("hflip")
            .output(path.replace(".mp4", "_flipped.mp4"), map_metadata=-1)
            .run()
        )
        return True
    except ffmpeg.Error as e:
        print(e.stderr)
        return False


def cleanup():
    filters = [
        "_zoomed",
        "_flipped",
        "_noised",
        "_saturated",
        "_contrasted",
        "_brightened",
    ]
    for file in os.listdir(DIR):
        path = os.path.join(DIR, file)
        for filter in filters:
            if filter in path:
                print("Removing: " + path)
                os.remove(path)
                break


def main():
    cleanup()
    for file in os.listdir(DIR):
        path = os.path.join(DIR, file)
        zoom_video(path, 105)
        zoom_video(path, 110)
        zoom_video(path, 115)
    print("Done!")


if __name__ == "__main__":
    main()
