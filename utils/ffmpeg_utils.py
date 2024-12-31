def construct_ffmpeg_command(scene, timeline_data, output_path):
    ffmpeg_path = "ffmpeg"
    inputs = []
    filter_complex = []

    resolution = f"{scene.render.resolution_x}x{scene.render.resolution_y}"
    fps = scene.ffmpeg_frame_rate if scene.ffmpeg_custom_fps else scene.render.fps
    codec = "h264_nvenc" if scene.ffmpeg_codec == 'H264' else "hevc_nvenc"

    for index, strip in enumerate(timeline_data):
        inputs.extend(["-i", strip["filepath"]])
        if strip["type"] == 'MOVIE':
            filter_complex.append(f"[{index}:v]scale={resolution}[v{index}]")

    command = [
        ffmpeg_path,
        *inputs,
        "-filter_complex", ";".join(filter_complex),
        "-r", str(fps),
        "-c:v", codec,
        "-preset", scene.ffmpeg_preset,
        output_path
    ]
    return command
