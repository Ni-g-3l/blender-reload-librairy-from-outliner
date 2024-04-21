bl_info = {
    "name": "Reload librairy from Outliner",
    "author": "Ni-g-3l",
    "version": (0, 1, 0),
    "blender": (3, 5, 1),
    "location": "Interface",
    "description": "Reload librairy from Outliner easily",
    "warning": "",
    "doc_url": "",
    "category": "Interface",
}

import bpy
import bl_ui

from reload_librairy_from_outliner_addon.blender.lib_operation import LIBRAIRY_OT_lib_reload

LIBRAIRY_OVERRIDE_MENU_CODE = (
    "    layout.menu(\"OUTLINER_MT_liboverride\", icon='LIBRARY_DATA_OVERRIDE')\n"
)


class DrawFuncStore:
    bpy_type = "OUTLINER_MT_context_menu"  # Adjust this to the correct menu type
    bpy_type_class = getattr(bl_ui.space_outliner, bpy_type)
    draw = None


def register():
    bpy.utils.register_class(LIBRAIRY_OT_lib_reload)
    DrawFuncStore.draw = DrawFuncStore.bpy_type_class.draw_common_operators

    filepath = DrawFuncStore.bpy_type_class.draw_common_operators.__code__.co_filename
    print(filepath)
    if filepath == "<string>":
        return
    try:
        with open(filepath, "r") as file:
            lines = file.readlines()
    except:
        return

    line_start = (
        DrawFuncStore.bpy_type_class.draw_common_operators.__code__.co_firstlineno - 1
    )
    
    for i in range(line_start, len(lines)):
        line = lines[i]
        if not line[0].isspace() and line.lstrip()[0] not in ("#", "\n", "\r"):
            break
        if "    def draw(self, context):" in line:
            i -= 1
            break

    line_end = i

    # Unindent draw func by one level, since it won't sit inside a class
    lines = [l[4:] for l in lines[line_start:line_end]]

    # Find the line where you want to insert your operator
    insert_after = LIBRAIRY_OVERRIDE_MENU_CODE
    insert_code = """
    operator = layout.operator("librairy.reload", text="Reload", icon=\'FILE_REFRESH\')\n
"""

    for i, line in enumerate(lines, 1):
        if insert_after in line:
            lines.insert(i, insert_code)
            break

    l = {}
    exec("".join(lines), {}, l)

    DrawFuncStore.bpy_type_class.draw_common_operators = l["draw_common_operators"]


def unregister():
    bpy.utils.unregister_class(LIBRAIRY_OT_lib_reload)
    if DrawFuncStore.draw is not None:
        DrawFuncStore.bpy_type_class.draw_common_operators = DrawFuncStore.draw
        DrawFuncStore.draw = None
