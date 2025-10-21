# VSEndless Render Engine - Linux Edition
# Updated for Linux compatibility and error feedback
# Created on 2025-10-21
# ===============================================================================
# VSEndless Live Render Output Storage
# ...existing code...

def get_ffmpeg_path():
    """Resolve ffmpeg binary with preference for a local portable copy.

    Search order (first hit wins):
    - ffmpeg next to this script (portable)
    - ffmpeg in the current .blend directory
    - system PATH resolution via shutil.which
    - fallback literal "ffmpeg" (lets ffmpeg resolve if available)
    """
    exe = "ffmpeg"  # Linux version
    # 1) Try script directory (guard __file__ for Blender Text Editor case)
    script_dir = None
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    except Exception:
        script_dir = None
    if script_dir:
        portable_path = os.path.join(script_dir, exe)
        if os.path.isfile(portable_path):
            return portable_path
    # 2) Try current .blend directory (//)
    try:
        blend_dir = bpy.path.abspath("//") if hasattr(bpy.path, 'abspath') else None
        if blend_dir:
            portable_blend_path = os.path.join(blend_dir, exe)
            if os.path.isfile(portable_blend_path):
                return portable_blend_path
    except Exception:
        pass
    # 3) PATH
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        return ffmpeg_path
    # 4) Fallback literal
    return "ffmpeg"
# ...existing code...
