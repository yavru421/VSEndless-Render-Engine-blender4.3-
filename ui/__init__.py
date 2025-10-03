# ui/__init__.py: APT pipeline module for UI registration
# Algebraic Notation: Let $x_1$ = UI modules, $y_1$ = registered UI panels
# $y_1 = register(x_1)$

def register():
    from . import render_panel
    render_panel.register()

def unregister():
    from . import render_panel
    render_panel.unregister()
