# presets.py: APT pipeline module for render presets
# Inputs: None
# Outputs: Preset dictionary

RENDER_PRESETS = {
    "YouTube 1080p": {
        "resolution_x": 1920,
        "resolution_y": 1080,
        "fps": 30,
        "format": "MP4"
    },
    "Instagram": {
        "resolution_x": 1080,
        "resolution_y": 1080,
        "fps": 30,
        "format": "MP4"
    }
}

def get_preset(name):
    return RENDER_PRESETS.get(name)
