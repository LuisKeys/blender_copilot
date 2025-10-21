"""
Blender operator executor
Handles safe execution of whitelisted Blender operators
"""

from .plan_executor import PlanExecutor

# Backward compatibility - export the main function
execute_plan_json = PlanExecutor.execute_plan_json
