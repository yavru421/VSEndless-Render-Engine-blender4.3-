import bpy
import os

def extract_timeline_data(scene):
    """
    Extracts data from the Video Sequence Editor (VSE) timeline.

    :param scene: Blender scene object.
    :return: List of dictionaries containing timeline data or None if no sequences found.
    """
    vse = scene.sequence_editor
    if not vse or not vse.sequences_all:
        return None

    timeline_data = []
    for seq in vse.sequences_all:
        if hasattr(seq, "filepath") and os.path.exists(bpy.path.abspath(seq.filepath)):
            timeline_data.append({
                "name": seq.name,
                "type": seq.type,
                "filepath": bpy.path.abspath(seq.filepath),
                "start_frame": seq.frame_start,
                "end_frame": seq.frame_final_end,
                "channel": seq.channel,
            })
    return timeline_data
