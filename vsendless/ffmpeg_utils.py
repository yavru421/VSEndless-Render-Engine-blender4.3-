
import os

def construct_ffmpeg_command(scene, timeline_data, output_path):
    ffmpeg_path = "ffmpeg"
    codec = scene.ffmpeg_codec
    bitrate = f"{scene.ffmpeg_bitrate}M"
    resolution = f"{scene.render.resolution_x}x{scene.render.resolution_y}"
    fps = scene.render.fps
    lut_file = scene.lut_file_path

    inputs = []
    filters = []

    for strip in timeline_data:
        inputs.extend(["-i", strip["filepath"]])
        if lut_file and os.path.exists(lut_file):
            filters.append(f"lut3d=file='{lut_file}'")

    filter_complex = ",".join(filters)
    command = [
        ffmpeg_path, *inputs, "-filter_complex", filter_complex if filter_complex else "",
        "-s", resolution, "-r", str(fps), "-c:v", codec, "-b:v", bitrate, output_path
    ]
    return [arg for arg in command if arg]
