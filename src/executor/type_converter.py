"""
Type conversion utilities for Blender operator arguments
"""

import math
from mathutils import Vector, Euler


class TypeConverter:
    """Handles type conversion for Blender operator arguments."""

    @staticmethod
    def convert_argument(tool_name, key, value):
        """Convert an argument value to the appropriate Blender type."""
        if key == "location" and isinstance(value, list) and len(value) == 3:
            return Vector(value)
        elif key == "rotation" and isinstance(value, list) and len(value) == 3:
            return Euler(value)
        elif key == "value" and isinstance(value, list) and len(value) == 3:
            return TypeConverter._convert_value_argument(tool_name, value)
        else:
            return value

    @staticmethod
    def _convert_value_argument(tool_name, value):
        """Convert value argument based on tool type."""
        if tool_name in {"transform.translate", "transform.resize"}:
            return Vector(value)
        elif tool_name == "transform.rotate":
            return TypeConverter._convert_rotation_value(value)
        else:
            return Vector(value)  # default for other values

    @staticmethod
    def _convert_rotation_value(value):
        """Convert rotation value from [x,y,z] format to single axis rotation."""
        print(f"DEBUG: Processing rotate with value {value}")
        for i, angle in enumerate(value):
            if angle != 0.0:
                # Convert degrees to radians if angle > 2*pi (likely degrees)
                if abs(angle) > 6.28:  # > 2*pi, probably degrees
                    angle = math.radians(angle)
                result = float(angle)
                axis = {0: "X", 1: "Y", 2: "Z"}[i]
                print(f"DEBUG: Set rotation angle {result} on axis {axis}")
                return result, axis
        print("DEBUG: No rotation, set value to 0.0")
        return 0.0, None

    @staticmethod
    def handle_resize_xyz(args):
        """Handle special x/y/z parameters for resize operations."""
        safe_kwargs = {}
        for k, v in args.items():
            if k in {"x", "y", "z"}:
                if "value" not in safe_kwargs:
                    safe_kwargs["value"] = [1.0, 1.0, 1.0]
                idx = {"x": 0, "y": 1, "z": 2}[k]
                safe_kwargs["value"][idx] = v
            else:
                safe_kwargs[k] = v
        return safe_kwargs
