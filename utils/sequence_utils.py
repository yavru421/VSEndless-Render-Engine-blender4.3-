# sequence_utils.py: Advanced sequence utilities for VSEndless
# Inputs: Blender VSE sequences
# Outputs: Sequence analysis, timeline data, helpers

import bpy
import os
import logging

logger = logging.getLogger("VSEndless.Sequence")

def get_sequences(context):
    """Get all sequences from the VSE timeline"""
    if not context.scene.sequence_editor:
        return []
    return context.scene.sequence_editor.sequences_all

def extract_timeline_data(scene):
    """
    Extracts data from the Video Sequence Editor (VSE) timeline.
    Returns processed timeline data suitable for FFmpeg processing.
    """
    vse = scene.sequence_editor
    if not vse or not vse.sequences_all:
        logger.warning("No sequences found in VSE")
        return []

    timeline_data = []
    for seq in vse.sequences_all:
        if hasattr(seq, "filepath") and seq.filepath:
            abs_path = bpy.path.abspath(seq.filepath)
            if os.path.exists(abs_path):
                timeline_data.append({
                    "name": seq.name,
                    "type": seq.type,
                    "filepath": abs_path,
                    "start_frame": seq.frame_start,
                    "end_frame": seq.frame_final_end,
                    "channel": seq.channel,
                    "blend_type": getattr(seq, 'blend_type', 'REPLACE'),
                    "ffmpeg_filter": getattr(seq, 'ffmpeg_filter', ''),
                })
                logger.debug(f"Added sequence: {seq.name} ({seq.type})")
            else:
                logger.warning(f"Sequence file not found: {abs_path}")
        elif seq.type in ['COLOR', 'TEXT', 'ADJUSTMENT']:
            # Handle generated strips
            timeline_data.append({
                "name": seq.name,
                "type": seq.type,
                "filepath": '',
                "start_frame": seq.frame_start,
                "end_frame": seq.frame_final_end,
                "channel": seq.channel,
                "blend_type": getattr(seq, 'blend_type', 'REPLACE'),
                "ffmpeg_filter": getattr(seq, 'ffmpeg_filter', ''),
            })
            logger.debug(f"Added generated sequence: {seq.name} ({seq.type})")

    logger.info(f"Extracted {len(timeline_data)} sequences from timeline")
    return timeline_data

def validate_sequences(timeline_data):
    """Validate sequence data for rendering"""
    valid_sequences = []

    for seq_data in timeline_data:
        if seq_data.get("filepath") and not os.path.exists(seq_data["filepath"]):
            logger.error(f"Missing file: {seq_data['filepath']}")
            continue

        if seq_data.get("type") == "MOVIE" and not seq_data.get("filepath"):
            logger.error(f"Movie sequence missing filepath: {seq_data['name']}")
            continue

        valid_sequences.append(seq_data)

    logger.info(f"Validated {len(valid_sequences)}/{len(timeline_data)} sequences")
    return valid_sequences

def get_timeline_range(timeline_data):
    """Get the overall frame range of the timeline"""
    if not timeline_data:
        return 1, 250  # Default range

    start_frames = [seq["start_frame"] for seq in timeline_data]
    end_frames = [seq["end_frame"] for seq in timeline_data]

    return min(start_frames), max(end_frames)
