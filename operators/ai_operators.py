# ai_operators.py: APT pipeline module for AI-powered operators
# Algebraic Notation: Let $x_1$ = timeline\_data, $x_2$ = user\_input, $y_1$ = ai\_results
# $y_1 = AI\_operator(x_1, x_2)$ where AI_operator: Timeline × UserInput → AIResults
# Inputs: VSE timeline data, user preferences, AI model parameters
# Outputs: Optimized render settings, upscaled videos, scene markers, analysis reports

import bpy
import logging
import threading
from typing import Dict, Any
from ..utils import ai_processor, sequence_utils

logger = logging.getLogger("VSEndless.AI.Operators")

class VSEndless_OT_AIAnalyzeTimeline(bpy.types.Operator):
    bl_idname = "vsendless.ai_analyze_timeline"
    bl_label = "AI Analyze Timeline"
    bl_description = "Use AI to analyze timeline and recommend optimal encoding settings"

    def execute(self, context):
        scene = context.scene

        # Get timeline data
        timeline_data = sequence_utils.extract_timeline_data(scene)
        if not timeline_data:
            self.report({'ERROR'}, "No sequences found in timeline!")
            return {'CANCELLED'}

        try:
            # Run AI analysis
            self.report({'INFO'}, "Starting AI analysis of timeline...")
            ai_proc = ai_processor.get_ai_processor()

            # Run analysis in background to avoid blocking UI
            def run_analysis():
                try:
                    analysis = ai_proc.analyze_timeline(timeline_data)

                    # Store results in scene for UI display
                    scene["vsendless_ai_analysis"] = analysis

                    # Apply recommendations automatically if enabled
                    if getattr(scene, 'vsendless_auto_apply_ai', True):
                        self._apply_ai_recommendations(scene, analysis)

                    logger.info("AI analysis completed successfully")

                except Exception as e:
                    logger.error(f"AI analysis failed: {e}")

            # Start analysis thread
            analysis_thread = threading.Thread(target=run_analysis)
            analysis_thread.daemon = True
            analysis_thread.start()

            self.report({'INFO'}, "AI analysis started in background...")
            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"AI analysis failed: {e}")
            logger.error(f"AI analysis error: {e}")
            return {'CANCELLED'}

    def _apply_ai_recommendations(self, scene, analysis: Dict[str, Any]):
        """Apply AI recommendations to scene settings"""
        recommendations = analysis.get("encoding_recommendations", {})

        if recommendations:
            # Update codec settings based on AI recommendations
            if hasattr(scene, 'vsendless_props') and scene.vsendless_props:
                props = scene.vsendless_props

                # Apply codec recommendation
                if "codec" in recommendations:
                    codec_map = {
                        "h264_nvenc": "h264_nvenc",
                        "hevc_nvenc": "hevc_nvenc",
                        "libx264": "libx264",
                        "libx265": "libx265"
                    }
                    if recommendations["codec"] in codec_map:
                        props.ffmpeg_codec = codec_map[recommendations["codec"]]

                # Apply bitrate recommendation
                if "bitrate" in recommendations:
                    props.ffmpeg_bitrate = recommendations["bitrate"]

            # Apply other recommendations to scene properties
            if hasattr(scene, 'nvenc_preset') and "preset" in recommendations:
                preset_map = {
                    "slow": "p1",
                    "medium": "p3",
                    "fast": "p5",
                    "lossless": "p1"
                }
                if recommendations["preset"] in preset_map:
                    scene.nvenc_preset = preset_map[recommendations["preset"]]

            logger.info(f"Applied AI recommendations: {recommendations}")

class VSEndless_OT_AIUpscale(bpy.types.Operator):
    bl_idname = "vsendless.ai_upscale"
    bl_label = "AI Upscale Selected Strip"
    bl_description = "Upscale selected video strip using AI"

    upscale_model = bpy.props.EnumProperty(
        name="AI Model",
        description="AI upscaling model to use",
        items=[
            ("real_esrgan", "Real-ESRGAN", "Best for real-world content"),
            ("esrgan", "ESRGAN", "Good general-purpose upscaling"),
            ("waifu2x", "Waifu2x", "Optimized for anime/cartoon content")
        ],
        default="real_esrgan"
    )

    scale_factor = bpy.props.IntProperty(
        name="Scale Factor",
        description="Upscaling factor (2x, 4x)",
        default=2,
        min=2,
        max=4
    )

    @classmethod
    def poll(cls, context):
        return (context.active_sequence_strip and
                context.active_sequence_strip.type == 'MOVIE')

    def execute(self, context):
        strip = context.active_sequence_strip

        if not strip or strip.type != 'MOVIE':
            self.report({'ERROR'}, "Select a video strip to upscale!")
            return {'CANCELLED'}

        input_path = bpy.path.abspath(strip.filepath)
        output_path = input_path.replace('.', f'_upscaled_{self.scale_factor}x.')

        try:
            self.report({'INFO'}, f"Starting AI upscaling with {self.upscale_model}...")

            ai_proc = ai_processor.get_ai_processor()
            upscaler = ai_proc.upscaler

            def upscale_async():
                success = upscaler.upscale_video(
                    input_path, output_path,
                    self.upscale_model, self.scale_factor
                )

                if success:
                    # Create new strip with upscaled video
                    bpy.app.timers.register(
                        lambda: self._create_upscaled_strip(context, output_path, strip),
                        first_interval=1.0
                    )

            # Start upscaling in background
            upscale_thread = threading.Thread(target=upscale_async)
            upscale_thread.daemon = True
            upscale_thread.start()

            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"AI upscaling failed: {e}")
            return {'CANCELLED'}

    def _create_upscaled_strip(self, context, upscaled_path: str, original_strip):
        """Create new strip with upscaled video"""
        try:
            if context.scene.sequence_editor:
                seq_editor = context.scene.sequence_editor

                # Create new movie strip
                new_strip = seq_editor.sequences.new_movie(
                    name=f"{original_strip.name}_AI_upscaled",
                    filepath=upscaled_path,
                    channel=original_strip.channel + 1,
                    frame_start=original_strip.frame_start
                )

                logger.info(f"Created upscaled strip: {new_strip.name}")

        except Exception as e:
            logger.error(f"Failed to create upscaled strip: {e}")

class VSEndless_OT_AISceneDetection(bpy.types.Operator):
    bl_idname = "vsendless.ai_scene_detection"
    bl_label = "AI Scene Detection"
    bl_description = "Detect scene changes and automatically create markers"

    sensitivity = bpy.props.FloatProperty(
        name="Sensitivity",
        description="Scene detection sensitivity (higher = more scenes)",
        default=0.6,
        min=0.1,
        max=1.0
    )

    create_markers = bpy.props.BoolProperty(
        name="Create Markers",
        description="Automatically create timeline markers at scene changes",
        default=True
    )    @classmethod
    def poll(cls, context):
        return (context.active_sequence_strip and
                context.active_sequence_strip.type == 'MOVIE')

    def execute(self, context):
        strip = context.active_sequence_strip

        if not strip or strip.type != 'MOVIE':
            self.report({'ERROR'}, "Select a video strip for scene detection!")
            return {'CANCELLED'}

        input_path = bpy.path.abspath(strip.filepath)

        try:
            self.report({'INFO'}, "Running AI scene detection...")

            ai_proc = ai_processor.get_ai_processor()
            scene_detector = ai_proc.scene_detector

            # Detect scenes
            scenes = scene_detector.detect_scenes(input_path)

            if not scenes:
                self.report({'WARNING'}, "No scene changes detected!")
                return {'FINISHED'}

            # Create markers if requested
            if self.create_markers:
                self._create_scene_markers(context, scenes, strip)

            self.report({'INFO'}, f"Detected {len(scenes)} scene changes")
            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"Scene detection failed: {e}")
            return {'CANCELLED'}

    def _create_scene_markers(self, context, scenes, strip):
        """Create timeline markers at scene change points"""
        scene = context.scene

        for i, scene_change in enumerate(scenes):
            frame = strip.frame_start + int(scene_change["timestamp"] * scene.render.fps)

            # Create marker
            marker = scene.timeline_markers.new(
                name=f"Scene {i+1}",
                frame=frame
            )

            logger.debug(f"Created scene marker at frame {frame}")

class VSEndless_OT_AIOptimizeSettings(bpy.types.Operator):
    bl_idname = "vsendless.ai_optimize_settings"
    bl_label = "AI Optimize Render Settings"
    bl_description = "Let AI optimize all render settings for current timeline"

    target_quality = bpy.props.EnumProperty(
        name="Target Quality",
        description="Desired output quality vs speed tradeoff",
        items=[
            ("SPEED", "Speed Priority", "Optimize for fastest rendering"),
            ("BALANCED", "Balanced", "Balance quality and speed"),
            ("QUALITY", "Quality Priority", "Optimize for best quality"),
            ("STREAMING", "Streaming", "Optimize for live streaming")
        ],
        default="BALANCED"
    )

    def execute(self, context):
        scene = context.scene

        try:
            # Get timeline data
            timeline_data = sequence_utils.extract_timeline_data(scene)
            if not timeline_data:
                self.report({'ERROR'}, "No sequences found in timeline!")
                return {'CANCELLED'}

            self.report({'INFO'}, f"AI optimizing settings for {self.target_quality} priority...")

            # Run AI analysis
            ai_proc = ai_processor.get_ai_processor()
            analysis = ai_proc.analyze_timeline(timeline_data)

            # Get optimized settings based on target
            optimized_settings = self._get_optimized_settings(analysis, self.target_quality)

            # Apply settings
            self._apply_optimized_settings(scene, optimized_settings)

            self.report({'INFO'}, f"Applied AI-optimized settings for {self.target_quality}")
            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"AI optimization failed: {e}")
            return {'CANCELLED'}

    def _get_optimized_settings(self, analysis: Dict[str, Any], target: str) -> Dict[str, Any]:
        """Get AI-optimized settings based on target priority"""
        base_recommendations = analysis.get("encoding_recommendations", {})

        # Modify based on target priority
        if target == "SPEED":
            return {
                **base_recommendations,
                "codec": "h264_nvenc",
                "preset": "fast",
                "bitrate": max(6, base_recommendations.get("bitrate", 8) - 2),
                "multipass": False
            }
        elif target == "QUALITY":
            return {
                **base_recommendations,
                "codec": "hevc_nvenc",
                "preset": "slow",
                "bitrate": base_recommendations.get("bitrate", 10) + 5,
                "multipass": True
            }
        elif target == "STREAMING":
            return {
                **base_recommendations,
                "codec": "h264_nvenc",
                "preset": "fast",
                "bitrate": 8,  # Fixed bitrate for streaming
                "profile": "baseline",
                "cbr": True
            }
        else:  # BALANCED
            return base_recommendations

    def _apply_optimized_settings(self, scene, settings: Dict[str, Any]):
        """Apply optimized settings to scene"""
        # Apply to VSEndless properties
        if hasattr(scene, 'vsendless_props') and scene.vsendless_props:
            props = scene.vsendless_props

            if "codec" in settings:
                props.ffmpeg_codec = settings["codec"]
            if "bitrate" in settings:
                props.ffmpeg_bitrate = settings["bitrate"]

        # Apply to scene properties
        if "preset" in settings and hasattr(scene, 'nvenc_preset'):
            preset_map = {"slow": "p1", "medium": "p3", "fast": "p5"}
            if settings["preset"] in preset_map:
                scene.nvenc_preset = preset_map[settings["preset"]]

        if "multipass" in settings and hasattr(scene, 'use_multipass'):
            scene.use_multipass = settings["multipass"]

def register():
    bpy.utils.register_class(VSEndless_OT_AIAnalyzeTimeline)
    bpy.utils.register_class(VSEndless_OT_AIUpscale)
    bpy.utils.register_class(VSEndless_OT_AISceneDetection)
    bpy.utils.register_class(VSEndless_OT_AIOptimizeSettings)

    # Add AI properties to scene
    bpy.types.Scene.vsendless_auto_apply_ai = bpy.props.BoolProperty(
        name="Auto-Apply AI Recommendations",
        description="Automatically apply AI encoding recommendations",
        default=True
    )

    logger.info("VSEndless AI operators registered")

def unregister():
    bpy.utils.unregister_class(VSEndless_OT_AIAnalyzeTimeline)
    bpy.utils.unregister_class(VSEndless_OT_AIUpscale)
    bpy.utils.unregister_class(VSEndless_OT_AISceneDetection)
    bpy.utils.unregister_class(VSEndless_OT_AIOptimizeSettings)

    if hasattr(bpy.types.Scene, 'vsendless_auto_apply_ai'):
        del bpy.types.Scene.vsendless_auto_apply_ai

    logger.info("VSEndless AI operators unregistered")