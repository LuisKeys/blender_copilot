"""
UI panels and operators for Blender Copilot
"""

import bpy
from .ollama_client import ollama_generate
from .executor import execute_plan_json
from .prompts import PROMPT_TEMPLATE


class PLAN_PT_Panel(bpy.types.Panel):
    bl_label = "Blender Copilot"
    bl_idname = "PLAN_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Blender Copilot"

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)

        # Always show the text input - create property if needed
        col.label(text="AI Command:")

        # Use a larger text area for better usability
        col.prop(context.scene, "plan_prompt", text="")

        col.operator("plan.run", text="🚀")
        col.separator()
        col.label(text="Quick Examples:")

        # Add multiple example buttons
        examples = [
            ("Cube", "Create a 2m cube at origin"),
            ("Sphere", "Add a UV sphere with radius 1.5"),
            ("Cylinder", "Create a cylinder and smooth shade it"),
        ]

        for name, command in examples:
            op = col.operator("plan.example", text=name)
            op.example = command


class PLAN_OT_Run(bpy.types.Operator):
    bl_idname = "plan.run"
    bl_label = "Run AI Command"

    def execute(self, context):
        # Get the prompt safely
        text = getattr(context.scene, "plan_prompt", "Create a 1m cube").strip()
        print(f"Blender Copilot: User prompt: {text}")

        # Use the AI pipeline
        prompt = PROMPT_TEMPLATE.replace("{user_text}", text)
        print(f"Blender Copilot: Generated prompt for Ollama")

        response = ollama_generate(prompt_text=prompt)
        if response.startswith("__ERROR__"):
            self.report({"ERROR"}, response)
            return {"CANCELLED"}

        log = execute_plan_json(response)
        if "✗" in log:
            self.report({"ERROR"}, log)
            return {"CANCELLED"}
        else:
            self.report({"INFO"}, log)
            return {"FINISHED"}


class PLAN_OT_Example(bpy.types.Operator):
    bl_idname = "plan.example"
    bl_label = "Set Example"
    example: bpy.props.StringProperty(default="")

    def execute(self, context):
        if hasattr(context.scene, "plan_prompt"):
            context.scene.plan_prompt = self.example
        return {"FINISHED"}


def register_ui():
    """Register UI classes"""
    # Register scene property first
    bpy.types.Scene.plan_prompt = bpy.props.StringProperty(
        name="AI Command",
        description="Describe what you want to create",
        default="Create a 1m cube at origin",
        maxlen=1024,
    )

    # Register classes
    bpy.utils.register_class(PLAN_PT_Panel)
    bpy.utils.register_class(PLAN_OT_Run)
    bpy.utils.register_class(PLAN_OT_Example)


def unregister_ui():
    """Unregister UI classes"""
    try:
        bpy.utils.unregister_class(PLAN_OT_Example)
        bpy.utils.unregister_class(PLAN_OT_Run)
        bpy.utils.unregister_class(PLAN_PT_Panel)
    except RuntimeError:
        pass

    try:
        del bpy.types.Scene.plan_prompt
    except AttributeError:
        pass
