bl_info = {
    "name": "Bool Object",
    "author": "Ömer Faruk Öz",
    "version": (1, 0),
    "blender": (2, 90, 0),
    "location": "View3D > Object > Bool Normal",
    "description": "Bool a Object",
    "warning": "",
    "doc_url": "",
    "category": "Object",
}



import bpy

def edit(type):
    active=bpy.context.active_object
    bpy.ops.object.shade_smooth()
    
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.object.editmode_toggle()
    
    bpy.ops.object.select_all(action='DESELECT')
    
    
    bpy.ops.mesh.customdata_custom_splitnormals_add()
    
    for object in selects:
        area=bpy.context.area.ui_type
        bpy.context.area.ui_type = 'VIEW_3D'
        
        z=bpy.context.scene.objects[active.name]
        z.select_set(True)
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.select_all(action='DESELECT')
            
            
        z=bpy.context.scene.objects[active.name]
        z.select_set(True)
        bpy.ops.object.duplicate ()
        bpy.ops.object.select_all(action='DESELECT')
            
        look=bpy.context.active_object
        bpy.context.view_layer.objects.active=object
            
        bpy.ops.mesh.customdata_custom_splitnormals_add()
        bpy.context.view_layer.objects.active=active
            
        bool=active.modifiers.new('a', 'BOOLEAN')
        
        if type==1:
            bool.operation = 'UNION'
        elif type==2:
            bool.operation = 'INTERSECT'
            
        bool.double_threshold=0
        bool.object=object
        
        bpy.ops.object.modifier_apply(modifier="a")
            
        #vertex groups
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
        
        groupA=active.vertex_groups.new()
        bpy.ops.object.vertex_group_assign()
        
        groupB=active.vertex_groups.new()
        bpy.ops.mesh.select_all(action='INVERT')
        bpy.ops.object.vertex_group_assign()
        
        bpy.ops.mesh.split()
        bpy.ops.object.vertex_group_remove_from( use_all_groups = False , use_all_verts = False )
        
        bpy.ops.mesh.select_all(action='INVERT')
        bpy.data.objects[active.name].vertex_groups.active=groupA
        bpy.ops.object.vertex_group_remove_from( use_all_groups = False , use_all_verts = False )
        
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
        
        
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.data.objects[active.name].vertex_groups.active=groupB
        bpy.ops.object.vertex_group_select()
        groupD=active.vertex_groups.new()
        bpy.ops.object.vertex_group_assign()
        bpy.data.objects[active.name].vertex_groups.active=groupA
        
        
        
        #group remove sharp
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE')
        bpy.ops.mesh.select_all(action='DESELECT')
            
        bpy.ops.object.editmode_toggle()
        for e in bpy.context.object.data.edges:
            if e.use_edge_sharp: 
                e.select = True
            
        bpy.ops.object.editmode_toggle()
            
        bpy.ops.object.vertex_group_remove_from( use_all_groups = False , use_all_verts = False )
        bpy.data.objects[active.name].vertex_groups.active=groupB
        bpy.ops.object.vertex_group_remove_from( use_all_groups = False , use_all_verts = False )
        
        bpy.ops.object.editmode_toggle()
        
        #modifiers
        data=active.modifiers.new('dataNormalAddonwwww', 'DATA_TRANSFER')
        data.object=look
        data.vertex_group=groupA.name
        data.use_loop_data = True
        data.data_types_loops = {'CUSTOM_NORMAL'}
        data.loop_mapping = 'POLYINTERP_LNORPROJ'
        bpy.ops.object.modifier_apply(modifier="dataNormalAddonwwww")
            
            
            
        #modifiers
        data=active.modifiers.new('dataNormalAddonwwww', 'DATA_TRANSFER')
        data.object=object
        data.vertex_group=groupB.name
        data.use_loop_data = True
        data.data_types_loops = {'CUSTOM_NORMAL'}
        data.loop_mapping = 'POLYINTERP_LNORPROJ'
        bpy.ops.object.modifier_apply(modifier="dataNormalAddonwwww")
        
        
        
        if type==0:
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.vertex_group_select()
            bpy.ops.mesh.flip_normals(only_clnors=True)
            bpy.ops.object.editmode_toggle()
        
        
        bpy.ops.object.editmode_toggle()
        bpy.data.objects[active.name].vertex_groups.active=groupD
        bpy.ops.object.vertex_group_select()
        bpy.ops.mesh.remove_doubles()
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.editmode_toggle()
        
        
        #remove vetex group
        active.vertex_groups.remove(groupA)
        active.vertex_groups.remove(groupB)
        active.vertex_groups.remove(groupD)
        
        
        
        objs = [bpy.context.scene.objects[look.name]]
        bpy.ops.object.delete({"selected_objects": objs})
      
    
    for object in selects:
        z=bpy.context.scene.objects[object.name]
        z.select_set(True)
    selects.clear()
    bpy.context.area.ui_type = area







selects=[]
def mainBool(type):
    area=bpy.context.area.ui_type
    bpy.context.area.ui_type = 'VIEW_3D'
    smooth=True
    for object in bpy.context.selected_objects:
        if not object.data.use_auto_smooth:
            smooth=False
        if not object==bpy.context.active_object:
            selects.append(object)
    bpy.context.area.ui_type = area
    
    if smooth:
        
        if 0 < len(selects):
            if type=="OP1":
                edit(0)
            elif type=="OP2":
                edit(1)
            elif type=="OP3":
                edit(2)
                
    else:
        raise Exception("Enable 'Auto Smooth' in Objects Data Properties")






def fixError():
    bpy.ops.object.shade_smooth()
    active=bpy.context.active_object
    for object in bpy.context.selected_objects:
        bpy.context.view_layer.objects.active=object
        bpy.context.object.data.use_auto_smooth = True
        
    bpy.context.view_layer.objects.active=active
    
    bpy.ops.wm.bool_normal("INVOKE_DEFAULT")






class BoolNormal(bpy.types.Operator):
    bl_label="BoolNormal"
    bl_idname="wm.bool_normal"
    
    
    preset_enum :bpy.props.EnumProperty(
        name="",
        description="Select Option",
        items=[
            ("OP1","Difference",""),
            ("OP2","Union",""),
            ("OP3","Intersect",""),
            ("OP4","Fix Normals","")
        ]
    )
    def execute(self,context):
        if self.preset_enum=="OP4":
            fixError()
        else:
            mainBool(self.preset_enum)
        return {"FINISHED"}
    
    def invoke(self,context,event):
        return context.window_manager.invoke_props_dialog(self)







def menu_func(self, context):
    layout = self.layout
    layout.separator()
    layout.operator("wm.bool_normal")
    
    
def register():
    bpy.utils.register_class(BoolNormal)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    
def unregister():
    bpy.utils.unregister_class(BoolNormal)
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    
if __name__ == "__main__":
    register()
