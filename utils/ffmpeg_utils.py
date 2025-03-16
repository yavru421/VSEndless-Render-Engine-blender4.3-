import shutil
import platform

def get_ffmpeg_path():
    """Get the FFmpeg executable path or just 'ffmpeg' if it's in PATH"""
    ffmpeg_path = shutil.which("ffmpeg")
    return ffmpeg_path if ffmpeg_path else "ffmpeg"

def construct_ffmpeg_command(scene, timeline_data, output_path):
    ffmpeg_path = get_ffmpeg_path()
    inputs = []
    filter_complex = []
    
    # Base settings
    resolution = f"{scene.render.resolution_x}x{scene.render.resolution_y}"
    fps = scene.ffmpeg_frame_rate if scene.ffmpeg_custom_fps else scene.render.fps
    
    # Hardware acceleration for input decoding
    hw_accel_in = []
    if scene.use_hwaccel and scene.hwaccel_method != 'NONE':
        if scene.hwaccel_method == 'CUDA':
            hw_accel_in = ["-hwaccel", "cuda", "-hwaccel_output_format", "cuda"]
        elif scene.hwaccel_method == 'NVDEC':
            hw_accel_in = ["-hwaccel", "nvdec", "-hwaccel_output_format", "cuda"]
    
    # Input files with hardware acceleration
    for index, strip in enumerate(timeline_data):
        inputs.extend([*hw_accel_in, "-i", strip["filepath"]])
    
    # Prepare filter complex chains
    v_inputs = []
    for index, strip in enumerate(timeline_data):
        if strip["type"] == 'MOVIE':
            # Base input
            input_str = f"[{index}:v]"
            
            # Scale with GPU if enabled
            scale_filter = ""
            if scene.use_gpu_scaling:
                scale_filter = f"scale_cuda={resolution}"
            else:
                scale_filter = f"scale={resolution}"
                
            # Denoise with GPU if enabled
            if scene.enable_denoising and scene.use_gpu_denoising:
                scale_filter += f",hwupload_cuda,tnr_cuda=mode=spatial:strength={scene.denoise_strength}"
            elif scene.enable_denoising:
                scale_filter += f",nlmeans=s={scene.denoise_strength}"
                
            # Stabilization
            if scene.apply_stabilization:
                if scene.use_gpu_stabilization:
                    scale_filter += ",vidstabtransform_cuda=smoothing=30:input=/tmp/transforms.trf"
                else:
                    scale_filter += ",vidstabtransform=smoothing=30:input=/tmp/transforms.trf"
            
            # LUT for color correction
            if scene.apply_lut and scene.lut_file_path:
                scale_filter += f",lut3d=file='{scene.lut_file_path}'"
            
            # Output label
            filter_complex.append(f"{input_str}{scale_filter}[v{index}]")
            v_inputs.append(f"[v{index}]")
    
    # Concat all videos if there are multiple strips
    if len(v_inputs) > 1:
        filter_complex.append(f"{''.join(v_inputs)}concat=n={len(v_inputs)}:v=1:a=0[outv]")
        video_map = "[outv]"
    else:
        video_map = v_inputs[0]
    
    # Output codec settings
    codec_settings = []
    if scene.ffmpeg_codec == 'H264':
        codec_settings = ["-c:v", "h264_nvenc"]
        # Add H.264-specific NVENC settings
        codec_settings.extend([
            "-preset", scene.nvenc_preset,
            "-profile:v", scene.h264_profile,
            "-tune", scene.nvenc_tune
        ])
    elif scene.ffmpeg_codec == 'H265':
        codec_settings = ["-c:v", "hevc_nvenc"]
        # Add H.265-specific NVENC settings
        codec_settings.extend([
            "-preset", scene.nvenc_preset,
            "-profile:v", scene.hevc_profile,
            "-tune", scene.nvenc_tune
        ])
    
    # Rate control settings
    if scene.rate_control_mode == 'CBR':
        # Constant Bitrate
        bitrate_kbps = scene.ffmpeg_bitrate * 1000
        codec_settings.extend(["-b:v", f"{bitrate_kbps}k", "-maxrate", f"{bitrate_kbps}k", "-bufsize", f"{bitrate_kbps*2}k"])
    elif scene.rate_control_mode == 'VBR':
        # Variable Bitrate
        bitrate_kbps = scene.ffmpeg_bitrate * 1000
        codec_settings.extend(["-b:v", f"{bitrate_kbps}k", "-maxrate", f"{bitrate_kbps*1.5}k", "-bufsize", f"{bitrate_kbps*3}k"])
    elif scene.rate_control_mode == 'CQP':
        # Constant Quantization Parameter
        codec_settings.extend(["-qp", str(scene.constant_quality_level)])
    elif scene.rate_control_mode == 'CRF':
        # Constant Rate Factor
        codec_settings.extend(["-crf", str(scene.constant_quality_level)])
    
    # Multipass encoding
    if scene.use_multipass:
        codec_settings.extend(["-multipass", "2"])
    
    # Audio settings (often needed in video files even for VSE)
    audio_settings = ["-c:a", "aac", "-b:a", "192k"]
    
    # Build the final command
    command = [
        ffmpeg_path,
        # Input files (already constructed)
        *inputs,
        # Filter complex
        "-filter_complex", ";".join(filter_complex),
        # Map outputs
        "-map", video_map,
        # Video settings
        *codec_settings,
        # Frame rate
        "-r", str(fps),
        # Audio settings
        *audio_settings,
        # Output file
        "-y", output_path
    ]
    
    return command
