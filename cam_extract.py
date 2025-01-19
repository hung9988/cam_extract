import os
import re
from moviepy.video.io.VideoFileClip import VideoFileClip
import argparse
parser=argparse.ArgumentParser()
# Define the folder paths
# input_folder = "/Volumes/Untitled"
# output_folder = "output_WD"
# start_time = 15
# end_time = 30

parser.add_argument("--input_folder", type=str, default="Videos", help="Input folder containing the video files")
parser.add_argument("--output_folder", type=str, default="output", help="Output folder to save the extracted clips")
parser.add_argument("--start_time", type=int, default=0, help="Start time in seconds for the clip")
parser.add_argument("--end_time", type=int, default=15, help="End time in seconds for the clip")
args=parser.parse_args()
input_folder=args.input_folder
output_folder=args.output_folder
start_time=args.start_time
end_time=args.end_time

os.makedirs(output_folder, exist_ok=True)

# Define the time spans
TIME_SPANS = [
    (8, 9),    # 8:00 to 9:00
    (11, 13),  # 11:00 to 13:00
    (16, 18),  # 16:00 to 18:00
    (21, 23),  # 21:00 to 23:00
]

# Regular expression to parse file names
file_pattern = re.compile(r"D(?P<camera>\d+)_\d{4}(?P<month>\d{2})(?P<day>\d{2})(?P<hour>\d{2})(?P<minute>\d{2})(?P<second>\d{2})")

# Dictionary to store processed cameras and time spans
processed_clips = {}

# Function to check if a time falls within a span
def in_time_span(hour, time_spans):
    for start, end in time_spans:
        if start <= hour < end:
            return (start, end)
    return None

# Process the files in the input folder
for filename in os.listdir(input_folder):
    if not filename.endswith(".mp4"):
        continue

    match = file_pattern.match(filename)
    if not match:
        continue

    # Extract timestamp details
    camera = match.group("camera")
    hour = int(match.group("hour"))

    # Check if the hour falls within a defined time span
    span = in_time_span(hour, TIME_SPANS)
    if not span:
        continue

    # Keep track of processed time spans for each camera
    if camera not in processed_clips:
        processed_clips[camera] = set()

    if span in processed_clips[camera]:
        continue

    # Process the video
    input_path = os.path.join(input_folder, filename)
    try:
        with VideoFileClip(input_path) as video:
            # Check if the video is long enough for a 15-second clip
            if video.duration < end_time:
                continue

            # Extract a 15-second clip from the start of the video
            clip = video.subclip(start_time, end_time)

            # Save the clip to the output folder
            output_filename = f"Camera{camera}_{span[0]}-{span[1]}_{filename}"
            output_path = os.path.join(output_folder, output_filename)
            clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

            # Mark this time span as processed for the camera
            processed_clips[camera].add(span)
    except Exception as e:
        print(f"Error processing {filename}: {e}")

print("Processing complete!")
