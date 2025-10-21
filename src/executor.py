"""
Blender operator executor
Handles safe execution of whitelisted Blender operators
"""

import json
import math
import bpy
from mathutils import Vector, Euler


def _call_op(tool_name, args):
    """Safely call a whitelisted Blender operator with validated arguments."""
    print(f"Blender Copilot: Calling operator {tool_name} with args {args}")
    TOOLMAP = {
        "mesh.primitive_cube_add": (
            bpy.ops.mesh.primitive_cube_add,
            {"size", "location", "rotation"},
        ),
        "mesh.primitive_uv_sphere_add": (
            bpy.ops.mesh.primitive_uv_sphere_add,
            {"radius", "segments", "rings", "location", "rotation"},
        ),
        "mesh.primitive_cylinder_add": (
            bpy.ops.mesh.primitive_cylinder_add,
            {"radius", "depth", "vertices", "location", "rotation"},
        ),
        "mesh.primitive_plane_add": (
            bpy.ops.mesh.primitive_plane_add,
            {"size", "location", "rotation"},
        ),
        "mesh.primitive_cone_add": (
            bpy.ops.mesh.primitive_cone_add,
            {"radius1", "radius2", "depth", "vertices", "location", "rotation"},
        ),
        "mesh.primitive_torus_add": (
            bpy.ops.mesh.primitive_torus_add,
            {
                "major_radius",
                "minor_radius",
                "abso_major_rad",
                "abso_minor_rad",
                "location",
                "rotation",
            },
        ),
        "object.modifier_add": (bpy.ops.object.modifier_add, {"type"}),
        "object.modifier_apply": (
            bpy.ops.object.modifier_apply,
            {"modifier", "apply_as"},
        ),
        "object.shade_smooth": (bpy.ops.object.shade_smooth, set()),
        "transform.translate": (bpy.ops.transform.translate, {"value"}),
        "transform.rotate": (bpy.ops.transform.rotate, {"value", "orient_axis"}),
        "transform.resize": (bpy.ops.transform.resize, {"value"}),
        "object.duplicate": (bpy.ops.object.duplicate, {"linked", "mode"}),
        "object.delete": (bpy.ops.object.delete, {"use_global"}),
    }

    if tool_name not in TOOLMAP:
        raise ValueError(f"Tool not allowed: {tool_name}")
    op, allowed = TOOLMAP[tool_name]

    # Context checks for operators requiring active object
    context_requiring_ops = {
        "object.modifier_add",
        "object.modifier_apply",
        "object.shade_smooth",
        "transform.translate",
        "transform.rotate",
        "transform.resize",
        "object.duplicate",
        "object.delete",
    }
    if tool_name in context_requiring_ops and not bpy.context.active_object:
        raise ValueError(f"Operator {tool_name} requires an active object")

    safe_kwargs = {}
    if isinstance(args, dict):
        for k, v in args.items():
            if k in allowed:
                # Type conversion for common Blender types
                if k == "location" and isinstance(v, list) and len(v) == 3:
                    safe_kwargs[k] = Vector(v)
                elif k == "rotation" and isinstance(v, list) and len(v) == 3:
                    safe_kwargs[k] = Euler(v)
                elif k == "value" and isinstance(v, list) and len(v) == 3:
                    if tool_name in {"transform.translate", "transform.resize"}:
                        safe_kwargs[k] = Vector(v)
                    elif tool_name == "transform.rotate":
                        # For rotate, convert [x,y,z] rotation to single axis rotation
                        # Find the non-zero component and use it as value
                        print(f"DEBUG: Processing rotate with value {v}")
                        for i, angle in enumerate(v):
                            if angle != 0.0:
                                # Convert degrees to radians if angle > 2*pi (likely degrees)
                                if abs(angle) > 6.28:  # > 2*pi, probably degrees
                                    angle = math.radians(angle)
                                safe_kwargs[k] = float(angle)
                                if i == 0:
                                    safe_kwargs["orient_axis"] = "X"
                                elif i == 1:
                                    safe_kwargs["orient_axis"] = "Y"
                                elif i == 2:
                                    safe_kwargs["orient_axis"] = "Z"
                                print(
                                    f"DEBUG: Set rotation angle {safe_kwargs[k]} on axis {safe_kwargs.get('orient_axis')}"
                                )
                                break
                        else:
                            safe_kwargs[k] = 0.0  # No rotation
                            print(f"DEBUG: No rotation, set value to 0.0")
                    else:
                        safe_kwargs[k] = Vector(v)  # default for other values
                else:
                    safe_kwargs[k] = v
            # Special handling for resize: if x/y/z provided, convert to value
            elif tool_name == "transform.resize" and k in {"x", "y", "z"}:
                if "value" not in safe_kwargs:
                    safe_kwargs["value"] = [1.0, 1.0, 1.0]
                idx = {"x": 0, "y": 1, "z": 2}[k]
                safe_kwargs["value"][idx] = v
    if safe_kwargs:
        result = op(**safe_kwargs)
    else:
        result = op()

    # Post-op check for visibility
    if tool_name.startswith("mesh.primitive_"):
        obj = bpy.context.active_object
        if obj:
            print(
                f"Blender Copilot: Created object '{obj.name}' at {obj.location}, visible: {not obj.hide_viewport}"
            )
        else:
            print("Blender Copilot: No active object after primitive add")

    return result


def execute_plan_json(plan_text):
    """Execute a JSON plan of Blender operations safely."""
    print(f"Blender Copilot: Executing plan: {plan_text[:200]}...")
    txt = plan_text.strip()
    # Try to extract JSON if wrapped in text
    start = txt.find("{")
    end = txt.rfind("}")
    if start != -1 and end != -1 and end > start:
        txt = txt[start : end + 1]
    else:
        print("Blender Copilot: No JSON object found in plan text")
        return f"Invalid plan: No JSON object found in response.\n---\n{txt[:400]}"

    try:
        data = json.loads(txt)
        print(f"Blender Copilot: Parsed plan with {len(data.get('plan', []))} steps")
    except json.JSONDecodeError as e:
        print(f"Blender Copilot: JSON decode error: {e}")
        return f"Invalid plan (JSON): {e}\n---\n{txt[:400]}"

    if "plan" not in data or not isinstance(data["plan"], list):
        print("Blender Copilot: Invalid plan structure")
        return "Invalid plan: Missing 'plan' as list."

    logs = []
    for i, step in enumerate(data["plan"]):
        tool = step.get("tool")
        args = step.get("args", {})
        if not tool:
            print(f"Blender Copilot: Step {i} missing tool")
            logs.append(f"[{i}] Missing tool ✗")
            continue
        print(f"Blender Copilot: Executing step {i}: {tool} with args {args}")
        try:
            # Auto-select the last created object for transform ops if none active
            if tool.startswith("transform.") and not bpy.context.active_object:
                if bpy.data.objects:
                    last_obj = bpy.data.objects[-1]  # Select the most recent object
                    bpy.context.view_layer.objects.active = last_obj
                    last_obj.select_set(True)
                    print(
                        f"Blender Copilot: Auto-selected object '{last_obj.name}' for transform"
                    )
            _call_op(tool, args)
            logs.append(f"[{i}] {tool} ✓")
        except Exception as e:
            print(f"Blender Copilot: Step {i} failed: {e}")
            logs.append(f"[{i}] {tool} ✗ {e}")
    print(f"Blender Copilot: Plan execution complete")
    return "\n".join(logs)
