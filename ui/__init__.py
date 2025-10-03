# ui/__init__.py: APT pipeline module for UI registration
# Algebraic Notation: Let $x_1$ = UI\\_modules, $y_1$ = registered\\_panels
# $y_1 = register\\_ui(x_1)$ where register_ui: UIModules → RegisteredPanels

def register():
    from . import render_panel
    render_panel.register()

    # AI UI modules (APT pipeline stage)
    try:
        from . import ai_panel
        ai_panel.register()
    except ImportError as e:
        print(f"[VSEndless.APT] AI UI modules not available: {e}")

def unregister():
    try:
        from . import ai_panel
        ai_panel.unregister()
    except ImportError:
        pass

    from . import render_panel
    render_panel.unregister()
