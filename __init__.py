"""
Blender Copilot Add-on
Main entry point for the refactored add-on
"""

bl_info = {
    "name": "Blender Copilot",
    "author": "Luc",
    "version": (0, 1, 0),
    "blender": (4, 5, 3),
    "location": "View3D > Sidebar > Blender Copilot",
    "description": "Translate natural language commands to Blender ops.",
    "category": "3D View",
}

from .src.ui import register_ui, unregister_ui
from .src.debug import setup_debug


def register():
    """Register the add-on"""
    setup_debug()
    # Register UI components
    register_ui()


def unregister():
    """Unregister the add-on"""
    unregister_ui()


if __name__ == "__main__":
    register()
