import requests


def call_groq_api(prompt, api_key):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant for video post-processing and creative rendering.",
            },
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 256,
        "temperature": 0.7,
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=15)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[Groq API error: {e}]"


def construct_ffmpeg_command(scene, timeline_data, output_path):
    ffmpeg_path = "ffmpeg"
    inputs = []
    filter_complex = []

    resolution = f"{scene.render.resolution_x}x{scene.render.resolution_y}"
    fps = scene.ffmpeg_frame_rate if scene.ffmpeg_custom_fps else scene.render.fps
    # Video codec selection
    if scene.output_format in ("MP4", "MKV"):
        codec = "h264_nvenc" if scene.ffmpeg_codec == "H264" else "hevc_nvenc"
    elif scene.output_format == "MOV":
        codec = "prores_ks"
    elif scene.output_format == "GIF":
        codec = "gif"
    elif scene.output_format == "PNGSEQ":
        codec = "png"
    else:
        codec = None
    # Audio codec selection
    if scene.output_format in ("MP4", "MKV", "MOV"):
        if scene.audio_codec == "AAC":
            acodec = "aac"
        elif scene.audio_codec == "MP3":
            acodec = "libmp3lame"
        elif scene.audio_codec == "PCM_S16LE":
            acodec = "pcm_s16le"
        else:
            acodec = "aac"
    elif scene.output_format in ("WAV",):
        acodec = "pcm_s16le"
    elif scene.output_format == "MP3":
        acodec = "libmp3lame"
    else:
        acodec = None

    for index, strip in enumerate(timeline_data):
        inputs.extend(["-i", strip["filepath"]])
        if strip["type"] == "MOVIE" and codec not in (None, "gif", "png"):
            filter_complex.append(f"[{index}:v]scale={resolution}[v{index}]")

    # Output extension
    ext_map = {
        "MP4": ".mp4",
        "MKV": ".mkv",
        "MOV": ".mov",
        "GIF": ".gif",
        "PNGSEQ": "%04d.png",
        "WAV": ".wav",
        "MP3": ".mp3",
    }
    ext = ext_map.get(scene.output_format, ".mp4")
    if not output_path.endswith(ext):
        output_path += ext

    command = [ffmpeg_path, *inputs]
    if filter_complex:
        command += ["-filter_complex", ";".join(filter_complex)]
    command += ["-r", str(fps)]
    if codec:
        command += ["-c:v", codec]
    if acodec:
        command += ["-c:a", acodec]
    command += ["-preset", scene.ffmpeg_preset]
    command += [output_path]

    # Handle advanced FFmpeg presets
    if (
        hasattr(scene, "ffmpeg_advanced_preset")
        and scene.ffmpeg_advanced_preset == "INSTA_IMAGE_SEQUENCE"
    ):
        resolution = "1080x1080"
        fps = 30
        ext = ".mp4"
        codec = "h264_nvenc"
        acodec = "aac"
        # Override output path extension
        if not output_path.endswith(ext):
            output_path += ext
        # Add Instagram-specific FFmpeg options
        command = [
            ffmpeg_path,
            *inputs,
            "-filter_complex",
            f"[0:v]scale={resolution},setsar=1:1[v]",
            "-map",
            "[v]",
            "-r",
            str(fps),
            "-c:v",
            codec,
            "-c:a",
            acodec,
            "-preset",
            scene.ffmpeg_preset,
            output_path,
        ]
        return command

    return command
