"""
Context validation utilities for Blender operations
"""

import bpy
from .operators import requires_active_object


class ContextChecker:
    """Handles context validation for Blender operations."""

    @staticmethod
    def validate_context(tool_name):
        """Validate that the required context exists for the operation."""
        if requires_active_object(tool_name) and not bpy.context.active_object:
            raise ValueError(f"Operator {tool_name} requires an active object")

    @staticmethod
    def auto_select_object_for_transform(tool_name):
        """Auto-select the last created object if needed for transform operations."""
        if tool_name.startswith("transform.") and not bpy.context.active_object:
            if bpy.data.objects:
                last_obj = bpy.data.objects[-1]  # Select the most recent object
                bpy.context.view_layer.objects.active = last_obj
                last_obj.select_set(True)
                print(
                    f"Blender Copilot: Auto-selected object '{last_obj.name}' for transform"
                )
