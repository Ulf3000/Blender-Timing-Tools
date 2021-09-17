bl_info = {
    "name": "GP Timing Tools",
    "author": "Alexander Mehler (Ulf3000)",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Adds a few Operators to make working with keyframes easier",
    "warning": "",
    "doc_url": "https://github.com/Ulf3000/Blender-Timing-Tools",
    "category": "Gpencil",
}


import bpy
from bpy.types import Operator


#-------------- functions --------------------------------------------

def refreshGPObject(obj):
    # trick to update the animation of the GP object
    
    for win in bpy.context.window_manager.windows:
        for area in win.screen.areas:
            #if area.type == 'DOPESHEET_EDITOR':
               # area.tag_redraw()      
            if area.type == 'VIEW_3D':
                area.tag_redraw()                         
   
    
def jumpFrame(count):

    for obj in bpy.context.selected_editable_objects:
        if obj.type == 'GPENCIL':

            for layer in obj.data.layers:
                keyframes = layer.frames.values()
                keyframeCount = len(keyframes)
                
                if keyframeCount==0: # no keyframes
                    continue
                
                currentFrame = bpy.context.scene.frame_current
                
                selectedKeyframes = []
                i = int(-1)
                
                for kf in keyframes:
                    i += 1
                    if kf.select == True: # and kf.frame_number<keyframes[keyframeCount-1].frame_number:
                        selectedKeyframes.append(i)
                        
                if len(selectedKeyframes)==0: # no keyframes selected
                    continue
                
                firstSelected = selectedKeyframes[0] 
                
                if count > 0:       
                
                    for skf in reversed(selectedKeyframes) :
                        #if skf == selectedKeyframes[len(selectedKeyframes)-1]:
                         #   break
                        keyframes[skf].select = False
                        keyframes[skf + count].select = True
                elif count < 0:       
                
                    for skf in selectedKeyframes :
                        #if skf == selectedKeyframes[len(selectedKeyframes)-1]:
                         #   break
                        keyframes[skf].select = False
                        keyframes[skf + count].select = True
            
                layer.frames.update()
           
            refreshGPObject(obj)


        if obj.type != 'GPENCIL':

            for fCurve in obj.animation_data.action.fcurves   :
                keyframes = fCurve.keyframe_points
        
                if len(keyframes)==0: # no keyframes
                    continue
                
                currentFrame = bpy.context.scene.frame_current
                
                selectedKeyframes = []
                i = int(-1)
                
                for kf in keyframes:
                    i += 1
                    if kf.select_control_point == True: # and kf.frame_number<keyframes[keyframeCount-1].frame_number:
                        selectedKeyframes.append(i)
                        
                if len(selectedKeyframes)==0: # no keyframes selected
                    continue
                
                firstSelected = selectedKeyframes[0] 
                
                if count > 0:       
                
                    for skf in reversed(selectedKeyframes) :
                        # if skf == selectedKeyframes[len(selectedKeyframes)]:
                        #     break
                        keyframes[skf].select_control_point = False
                        keyframes[skf].select_left_handle = False
                        keyframes[skf].select_right_handle = False


                        keyframes[skf + count].select_control_point = True
                        keyframes[skf + count].select_left_handle = True
                        keyframes[skf + count].select_right_handle = True
                elif count < 0:       
                
                    for skf in selectedKeyframes :
                        #if skf == selectedKeyframes[len(selectedKeyframes)-1]:
                         #   break
                        keyframes[skf].select_control_point = False
                        keyframes[skf].select_left_handle = False
                        keyframes[skf].select_right_handle = False


                        keyframes[skf + count].select_control_point = True
                        keyframes[skf + count].select_left_handle = True
                        keyframes[skf + count].select_right_handle = True
            
            #     layer.frames.update()
            # bpy.context.scene.frame_current+=1 
            # bpy.context.scene.frame_current-=1
           
            # refreshGPObject(obj)
            
# --------- move first selected  ------------
    
    
def move(count):
    for obj in bpy.context.selected_editable_objects:
            
        if obj.type == 'GPENCIL':
            for layer in obj.data.layers:
                keyframes = layer.frames.values()
        
                if len(keyframes)==0: # no keyframes
                    continue
        
                selectedKeyframes = []
        
                for kf in keyframes:
                    if kf.select == True:
                        selectedKeyframes.append(kf)
                        kf.frame_number += count
                        break
                
                layer.frames.update()
        
            refreshGPObject(obj)
        
        if obj.type != 'GPENCIL':
            for fCurve in obj.animation_data.action.fcurves   :
                keyframes = fCurve.keyframe_points
        
                if len(keyframes)==0: # no keyframes
                    continue
        
                selectedKeyframes = []
        
                for kf in keyframes:
                    if kf.select_control_point == True:
                        selectedKeyframes.append(kf)
                        kf.co.x += count
                        kf.handle_left.x += count
                        kf.handle_right.x += count
                        break
                
            #     layer.frames.update()
        
            # refreshGPObject(obj)
    

# --------- move first selected and all later keyframes ------------
    
    
def rippleMove(count):
    for obj in bpy.context.selected_editable_objects:
            
        if obj.type == 'GPENCIL':
            for layer in obj.data.layers:
                keyframes = layer.frames.values()
        
                if len(keyframes)==0: # no keyframes
                    continue
        
                selectedKeyframes = []
        
                for kf in keyframes:
                    if kf.select == True:
                        selectedKeyframes.append(kf)
                
                if len(selectedKeyframes)==0: # no keyframes selected
                    continue
        
                firstSelected = selectedKeyframes[0]        
        
                for kf in keyframes:
                    if count < 0:
                        if kf.frame_number - count == firstSelected.frame_number:
                            break
                    
                    if kf.frame_number >= firstSelected.frame_number:  # >=
                        kf.frame_number += count
                layer.frames.update()
        
            refreshGPObject(obj)

        #-------------------------------------------------------------------

        if obj.type != 'GPENCIL':
            for fCurve in obj.animation_data.action.fcurves   :
                keyframes = fCurve.keyframe_points
        
                if len(keyframes)==0: # no keyframes
                    continue
        
                selectedKeyframes = []
        
                for kf in keyframes:
                    if kf.select_control_point == True:
                        selectedKeyframes.append(kf)
                
                if len(selectedKeyframes)==0: # no keyframes selected
                    continue
        
                firstSelected = selectedKeyframes[0]        
        
                for kf in keyframes:
                    if count < 0:
                        if kf.co.x - count == firstSelected.co.x:
                            break
                    
                    if kf.co.x >= firstSelected.co.x:  # >=
                        kf.co.x += count
                        kf.handle_left.x += count
                        kf.handle_right.x += count
        
# --------- make frame longer (or shorter) like adobe flash/animate F5 ------------
    

def rippleLength(count): 
    for obj in bpy.context.selected_editable_objects:
        if obj.type == 'GPENCIL':
            for layer in obj.data.layers:
                keyframes = layer.frames.values()
                keyframeCount = len(keyframes)
                
                if keyframeCount==0: # no keyframes
                    continue
                
                currentFrame = bpy.context.scene.frame_current
                
                selectedKeyframes = []
                
                for kf in keyframes:
                    if kf.select == True: # and kf.frame_number<keyframes[keyframeCount-1].frame_number:
                        selectedKeyframes.append(kf)
                        
                if len(selectedKeyframes)==0: # no keyframes selected
                    continue
                
                firstSelected = selectedKeyframes[0]        
                
                for kf in keyframes:
                    if kf.frame_number > firstSelected.frame_number:   # >
                        kf.frame_number += count
                        
                layer.frames.update()

            refreshGPObject(obj)

        # ---------------------------------------------------------------------

        if obj.type != 'GPENCIL':
            for fCurve in obj.animation_data.action.fcurves   :
                keyframes = fCurve.keyframe_points
        
                if len(keyframes)==0: # no keyframes
                    continue
        
                selectedKeyframes = []
        
                for kf in keyframes:
                    if kf.select_control_point == True:
                        selectedKeyframes.append(kf)
                
                if len(selectedKeyframes)==0: # no keyframes selected
                    continue
        
                firstSelected = selectedKeyframes[0]        
        
                for kf in keyframes:
                    if count < 0:
                        if kf.co.x - count == firstSelected.co.x:
                            break
                    
                    if kf.co.x > firstSelected.co.x:  # >
                        kf.co.x += count
                        kf.handle_left.x += count
                        kf.handle_right.x += count
            
            

#-------------------Classes for Blender Addon--------------------------------------------------------------

class GPencilSelectNextFrame(Operator):
    bl_idname = "view3d.rippleselectnext"
    bl_label = "Ripple Add One Frame to the (first) selected Frame"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        jumpFrame(1)
        return {'FINISHED'}
    

class GPencilSelectPrevFrame(Operator):
    bl_idname = "view3d.rippleselectprev"
    bl_label = "Ripple Add One Frame to the (first) selected Frame"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        jumpFrame(-1)
        return {'FINISHED'}
    
class GPencilMoveRight(Operator):
    bl_idname = "view3d.moveright"
    bl_label = "Move Greasepencil Keyframes"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):

        move(1)
        return {'FINISHED'}
    

class GPencilMoveLeft(Operator):
    bl_idname = "view3d.moveleft"
    bl_label = "Move Greasepencil Keyframes"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):

        move(-1)
        return {'FINISHED'}


class GPencilRippleMoveRight(Operator):
    bl_idname = "view3d.ripplemoveright"
    bl_label = "Ripple Move Greasepencil Keyframes"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):

        rippleMove(1)
        return {'FINISHED'}
    

class GPencilRippleMoveLeft(Operator):
    bl_idname = "view3d.ripplemoveleft"
    bl_label = "Ripple Move Greasepencil Keyframes"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):

        rippleMove(-1)
        return {'FINISHED'}


class GPencilRippleAddFrame(Operator):
    bl_idname = "view3d.rippleaddframe"
    bl_label = "Ripple Add One Frame to the (first) selected Frame"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):

        rippleLength(1)
        return {'FINISHED'}
    
class GPencilRippleDelFrame(Operator):
    bl_idname = "view3d.rippledelframe"
    bl_label = "Ripple Add One Frame to the (first) selected Frame"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):

        rippleLength(-1)
        return {'FINISHED'}

# --------- register the classes ----------------------------------

def register():
    bpy.utils.register_class(GPencilMoveRight)
    bpy.utils.register_class(GPencilMoveLeft)
    bpy.utils.register_class(GPencilRippleMoveRight)
    bpy.utils.register_class(GPencilRippleMoveLeft)
    bpy.utils.register_class(GPencilRippleDelFrame)
    bpy.utils.register_class(GPencilRippleAddFrame)
    bpy.utils.register_class(GPencilSelectNextFrame)
    bpy.utils.register_class(GPencilSelectPrevFrame)


def unregister():
    bpy.utils.unregister_class(GPencilMoveRight)
    bpy.utils.unregister_class(GPencilMoveLeft)
    bpy.utils.unregister_class(GPencilRippleMoveRight)
    bpy.utils.unregister_class(GPencilRippleMoveLeft)
    bpy.utils.unregister_class(GPencilRippleAddFrame)
    bpy.utils.unregister_class(GPencilRippleDelFrame)
    bpy.utils.unregister_class(GPencilSelectNextFrame)
    bpy.utils.unregister_class(GPencilSelectPrevFrame)



if __name__ == "__main__":
    register()
