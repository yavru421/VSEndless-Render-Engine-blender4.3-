# operators/__init__.py: APT pipeline module for operator registration
# Algebraic Notation: Let $x_1$ = operator modules, $y_1$ = registered operators
# $y_1 = register(x_1)$

def register():
    from . import render_operator
    render_operator.register()

def unregister():
    from . import render_operator
    render_operator.unregister()
