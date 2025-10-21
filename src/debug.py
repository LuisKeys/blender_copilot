"""
Debug utilities for Blender Copilot
"""

# Debug support
try:
    import debugpy
except ImportError:
    debugpy = None


def setup_debug():
    """Setup debug server for remote debugging"""
    if debugpy is not None:
        try:
            debugpy.listen(("localhost", 5678))
            # Optionally wait for debugger to attach:
            # debugpy.wait_for_client()
            print("Blender Copilot: Debug server listening on localhost:5678")
        except Exception as e:
            print(f"Blender Copilot: Failed to start debug server: {e}")
    else:
        print("Blender Copilot: debugpy not available, debug server not started")
