"""
UI panels and operators for Blender Copilot
"""

import bpy
from .ollama_client import ollama_generate
from .executor import execute_plan_json
from .prompts import PROMPT_TEMPLATE


class PLAN_PT_Panel(bpy.types.Panel):
    bl_label = "Gemma JSON Plan"
    bl_idname = "PLAN_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Blender Copilot"

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.prop(context.scene, "plan_prompt")
        col.operator("gemma.plan_run", text="Run")
        col.separator()
        col.label(text="Examples:")
        row = col.row(align=True)
        row.operator("gemma.plan_example", text="Cube").example = (
            "Create a 2 m cube centered on the origin, and shade smooth."
        )


class PLAN_OT_Run(bpy.types.Operator):
    bl_idname = "gemma.plan_run"
    bl_label = "Run via Ollama"

    def execute(self, context):
        text = context.scene.plan_prompt.strip()
        print(f"Blender Copilot: User prompt: {text}")
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
    bl_idname = "gemma.plan_example"
    bl_label = "Insert example"
    example: bpy.props.StringProperty(default="")

    def execute(self, context):
        context.scene.plan_prompt = self.example
        return {"FINISHED"}


def register_ui():
    """Register UI classes"""
    bpy.utils.register_class(PLAN_PT_Panel)
    bpy.utils.register_class(PLAN_OT_Run)
    bpy.utils.register_class(PLAN_OT_Example)

    bpy.types.Scene.plan_prompt = bpy.props.StringProperty(
        name="AI Command",
        description="Describe what you want. The model returns a SAFE JSON plan (no code).",
        default="Create a 1 m cube, then add a SUBSURF modifier level 2 and apply it.",
    )


def unregister_ui():
    """Unregister UI classes"""
    del bpy.types.Scene.plan_prompt
    bpy.utils.unregister_class(PLAN_OT_Example)
    bpy.utils.unregister_class(PLAN_OT_Run)
    bpy.utils.unregister_class(PLAN_PT_Panel)
