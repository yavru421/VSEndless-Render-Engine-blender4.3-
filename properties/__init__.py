# properties/__init__.py: APT pipeline module for property registration
# Algebraic Notation: Let $x_1$ = property modules, $y_1$ = registered properties
# $y_1 = register(x_1)$

def register():
    from . import render_properties
    render_properties.register()

def unregister():
    from . import render_properties
    render_properties.unregister()
