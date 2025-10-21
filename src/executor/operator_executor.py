"""
Operator execution utilities for Blender Copilot
"""

import bpy
from .operators import get_operator_info
from .context_checker import ContextChecker
from .type_converter import TypeConverter


class OperatorExecutor:
    """Handles safe execution of Blender operators."""

    @staticmethod
    def execute_operator(tool_name, args):
        """Safely execute a Blender operator with validated arguments."""
        print(f"Blender Copilot: Calling operator {tool_name} with args {args}")

        # Get operator info
        op, allowed_params = get_operator_info(tool_name)

        # Validate context
        ContextChecker.validate_context(tool_name)

        # Prepare safe arguments
        safe_kwargs = OperatorExecutor._prepare_arguments(
            tool_name, args, allowed_params
        )

        # Execute operator
        if safe_kwargs:
            result = op(**safe_kwargs)
        else:
            result = op()

        # Post-execution checks
        OperatorExecutor._post_execution_check(tool_name)

        return result

    @staticmethod
    def _prepare_arguments(tool_name, args, allowed_params):
        """Prepare and validate operator arguments."""
        safe_kwargs = {}

        if isinstance(args, dict):
            # Handle special resize x/y/z parameters
            if tool_name == "transform.resize":
                args = TypeConverter.handle_resize_xyz(args)

            for k, v in args.items():
                if k in allowed_params:
                    # Special handling for transform.rotate value
                    if (
                        tool_name == "transform.rotate"
                        and k == "value"
                        and isinstance(v, list)
                        and len(v) == 3
                    ):
                        angle, axis = TypeConverter._convert_rotation_value(v)
                        safe_kwargs[k] = angle
                        if axis:
                            safe_kwargs["orient_axis"] = axis
                    else:
                        safe_kwargs[k] = TypeConverter.convert_argument(tool_name, k, v)
                elif tool_name == "transform.resize" and k in {"x", "y", "z"}:
                    # Already handled by handle_resize_xyz
                    pass

        return safe_kwargs

    @staticmethod
    def _post_execution_check(tool_name):
        """Perform post-execution checks and logging."""
        if tool_name.startswith("mesh.primitive_"):
            obj = bpy.context.active_object
            if obj:
                print(
                    f"Blender Copilot: Created object '{obj.name}' at {obj.location}, visible: {not obj.hide_viewport}"
                )
            else:
                print("Blender Copilot: No active object after primitive add")
