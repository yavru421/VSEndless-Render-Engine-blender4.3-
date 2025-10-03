# utils/__init__.py: APT pipeline module for utility registration
# Algebraic Notation: Let $x_1$ = utility\\_modules, $y_1$ = registered\\_utilities
# $y_1 = register\\_utils(x_1)$ where register_utils: UtilModules → RegisteredUtils

from . import ffmpeg_utils, sequence_utils, presets

# AI processing utilities (APT pipeline stage)
try:
    from . import ai_processor
except ImportError:
    ai_processor = None

# Cloud rendering utilities (APT pipeline stage)
try:
    from . import cloud_renderer
except ImportError:
    cloud_renderer = None

def register():
    # APT pipeline: register all utility modules
    pass

def unregister():
    # APT pipeline: unregister all utility modules
    pass
