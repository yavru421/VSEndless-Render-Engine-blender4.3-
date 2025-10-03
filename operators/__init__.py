# operators/__init__.py: APT pipeline module for operator registration
# Algebraic Notation: Let $x_1$ = operator\\_modules, $y_1$ = registered\\_operators
# $y_1 = register\\_ops(x_1)$ where register_ops: OpModules → RegisteredOps

def register():
    # APT Stage 1: Core render operators
    from . import render_operator
    render_operator.register()

    # APT Stage 2: AI-powered operators (advanced pipeline)
    try:
        from . import ai_operators
        ai_operators.register()
        print("[VSEndless.APT] AI operators pipeline stage activated")
    except ImportError as e:
        print(f"[VSEndless.APT] AI pipeline stage not available: {e}")

    # APT Stage 3: Cloud operators (distributed pipeline)
    try:
        from . import cloud_operators
        cloud_operators.register()
        print("[VSEndless.APT] Cloud operators pipeline stage activated")
    except ImportError as e:
        print(f"[VSEndless.APT] Cloud pipeline stage not available: {e}")

def unregister():
    # APT unregistration: reverse order for proper dependency cleanup
    try:
        from . import cloud_operators
        cloud_operators.unregister()
    except ImportError:
        pass

    try:
        from . import ai_operators
        ai_operators.unregister()
    except ImportError:
        pass

    from . import render_operator
    render_operator.unregister()
