# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Face-Cap Tool",
    "author" : "Quinn Dacre", 
    "description" : "",
    "blender" : (3, 0, 0),
    "version" : (1, 0, 0),
    "location" : "",
    "warning" : "",
    "doc_url": "", 
    "tracker_url": "", 
    "category" : "3D View" 
}


import bpy
import bpy.utils.previews


addon_keymaps = {}
_icons = None
class SNA_PT_FACECAP_TOOL_60735(bpy.types.Panel):
    bl_label = 'Face-Cap Tool'
    bl_idname = 'SNA_PT_FACECAP_TOOL_60735'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = 'Face-Cap'
    bl_order = 0
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        op = layout.operator('sna.add_target_4bfa6', text='Add Depth Target', icon_value=93, emboss=True, depress=False)
        op = layout.operator('sna.add_armatures_c9da8', text='Add Armatures', icon_value=174, emboss=True, depress=False)
        op = layout.operator('sna.join__scale_3aa21', text='Join Armatures', icon_value=259, emboss=True, depress=False)
        op = layout.operator('sna.weight_up_f96f1', text='Weight up!', icon_value=178, emboss=True, depress=False)


class SNA_OT_Add_Target_4Bfa6(bpy.types.Operator):
    bl_idname = "sna.add_target_4bfa6"
    bl_label = "Add Target"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        for tracker in bpy.data.objects:
            #Empty?
            if tracker.type == "EMPTY":
                # If it is an empty it will make the empty we found the active object
                bpy.context.view_layer.objects.active = tracker
                bpy.context.object.constraints["Follow Track"].depth_object = bpy.data.objects["Head"]
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Add_Armatures_C9Da8(bpy.types.Operator):
    bl_idname = "sna.add_armatures_c9da8"
    bl_label = "Add Armatures"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        for tracker in bpy.data.objects: 
            if tracker.type == "EMPTY":
                # If it is an empty it will make the empty we found the active object
                bpy.context.view_layer.objects.active = tracker
                #adds armatures
                bpy.ops.object.armature_add(enter_editmode=False, location=tracker.matrix_world.translation)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Join__Scale_3Aa21(bpy.types.Operator):
    bl_idname = "sna.join__scale_3aa21"
    bl_label = "Join & Scale"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        # Get all bones in the scene
        bones = [bone for bone in bpy.data.objects if bone.type == 'ARMATURE']
        # Join all bones together
        bpy.ops.object.select_all(action='DESELECT')
        for bone in bones:
            bone.select_set(True)
        bpy.ops.object.join()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Weight_Up_F96F1(bpy.types.Operator):
    bl_idname = "sna.weight_up_f96f1"
    bl_label = "Weight Up!"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        # Select the 'Head' mesh
        bpy.data.objects['Head'].select_set(True)
        # Select the armature
        bpy.data.objects['Armature.007'].select_set(True)
        # Set the active object to the armature
        bpy.context.view_layer.objects.active = bpy.data.objects['Armature.007']
        # Parent the 'Head' mesh to the armature with automatic weights
        bpy.ops.object.parent_set(type='ARMATURE_AUTO')
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def register():
    global _icons
    _icons = bpy.utils.previews.new()
    bpy.utils.register_class(SNA_PT_FACECAP_TOOL_60735)
    bpy.utils.register_class(SNA_OT_Add_Target_4Bfa6)
    bpy.utils.register_class(SNA_OT_Add_Armatures_C9Da8)
    bpy.utils.register_class(SNA_OT_Join__Scale_3Aa21)
    bpy.utils.register_class(SNA_OT_Weight_Up_F96F1)


def unregister():
    global _icons
    bpy.utils.previews.remove(_icons)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    for km, kmi in addon_keymaps.values():
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    bpy.utils.unregister_class(SNA_PT_FACECAP_TOOL_60735)
    bpy.utils.unregister_class(SNA_OT_Add_Target_4Bfa6)
    bpy.utils.unregister_class(SNA_OT_Add_Armatures_C9Da8)
    bpy.utils.unregister_class(SNA_OT_Join__Scale_3Aa21)
    bpy.utils.unregister_class(SNA_OT_Weight_Up_F96F1)
