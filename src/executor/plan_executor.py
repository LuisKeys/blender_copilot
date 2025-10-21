"""
Plan execution utilities for Blender Copilot
"""

import json
import bpy
from .context_checker import ContextChecker
from .operator_executor import OperatorExecutor


class PlanExecutor:
    """Handles execution of JSON plans containing multiple operations."""

    @staticmethod
    def execute_plan_json(plan_text):
        """Execute a JSON plan of Blender operations safely."""
        print(f"Blender Copilot: Executing plan: {plan_text[:200]}...")

        # Parse the plan
        plan_data = PlanExecutor._parse_plan(plan_text)
        if not plan_data:
            return "Invalid plan: Could not parse JSON"

        # Execute each step
        logs = []
        for i, step in enumerate(plan_data):
            tool = step.get("tool")
            args = step.get("args", {})

            if not tool:
                print(f"Blender Copilot: Step {i} missing tool")
                logs.append(f"[{i}] Missing tool ✗")
                continue

            print(f"Blender Copilot: Executing step {i}: {tool} with args {args}")

            try:
                # Auto-select object for transforms if needed
                ContextChecker.auto_select_object_for_transform(tool)

                # Execute the operator
                OperatorExecutor.execute_operator(tool, args)
                logs.append(f"[{i}] {tool} ✓")

            except Exception as e:
                print(f"Blender Copilot: Step {i} failed: {e}")
                logs.append(f"[{i}] {tool} ✗ {e}")

        print("Blender Copilot: Plan execution complete")
        return "\n".join(logs)

    @staticmethod
    def _parse_plan(plan_text):
        """Parse JSON plan from text."""
        txt = plan_text.strip()

        # Try to extract JSON if wrapped in text
        start = txt.find("{")
        end = txt.rfind("}")
        if start != -1 and end != -1 and end > start:
            txt = txt[start : end + 1]
        else:
            print("Blender Copilot: No JSON object found in plan text")
            return None

        try:
            data = json.loads(txt)
            print(
                f"Blender Copilot: Parsed plan with {len(data.get('plan', []))} steps"
            )
            return data.get("plan", [])
        except json.JSONDecodeError as e:
            print(f"Blender Copilot: JSON decode error: {e}")
            return None
