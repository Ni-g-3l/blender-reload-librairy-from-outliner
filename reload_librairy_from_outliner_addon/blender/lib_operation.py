from typing import Any
import bpy
from bpy.types import Context

class LIBRAIRY_OT_lib_reload(bpy.types.Operator):

    bl_idname = "librairy.reload"
    bl_label = "Reload librairy linked to this object"
    bl_description = "Reload librairy linked to this object"

    @classmethod
    def poll(cls, context: Context | Any) -> bool:
        for obj in context.selected_ids:
            if obj.data.library is not None:
                return True
        return False

    def execute(self, context: Context | Any):
        for obj in context.selected_ids:
            if obj.data.library is not None:
                self.report({"INFO"}, f"Reload '{obj.data.library.name}' librairy.")
                obj.data.library.reload()
        return {"FINISHED"}