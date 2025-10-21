"""
Operator definitions and tool mapping for Blender Copilot
"""

import bpy


# Tool mapping: operator_name -> (operator_function, allowed_parameters)
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

# Operators that require an active object in the context
CONTEXT_REQUIRING_OPS = {
    "object.modifier_add",
    "object.modifier_apply",
    "object.shade_smooth",
    "transform.translate",
    "transform.rotate",
    "transform.resize",
    "object.duplicate",
    "object.delete",
}


def get_operator_info(tool_name):
    """Get operator function and allowed parameters for a tool."""
    if tool_name not in TOOLMAP:
        raise ValueError(f"Tool not allowed: {tool_name}")
    return TOOLMAP[tool_name]


def requires_active_object(tool_name):
    """Check if a tool requires an active object."""
    return tool_name in CONTEXT_REQUIRING_OPS
