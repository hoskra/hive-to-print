from math import sqrt
import bpy

l = 14.2
h = 3

verts = [
    (l, 0, 0),
    (l/2, (sqrt(3)*l)/2, 0),
    (-l/2, (sqrt(3)*l)/2, 0),
    (-l, 0, 0),
    (-l/2,-(sqrt(3)*l)/2,0),
    (l/2,-(sqrt(3)*l)/2,0),
    (l, 0, -h),
    (l/2, (sqrt(3)*l)/2, -h),
    (-l/2, (sqrt(3)*l)/2, -h),
    (-l, 0, -h),
    (-l/2,-(sqrt(3)*l)/2,-h),
    (l/2,-(sqrt(3)*l)/2,-h)
]

faces = [
    (5, 4, 3, 2, 1, 0),
    (6, 7, 8, 9, 10, 11),
    (0, 1, 7, 6),
    (1, 2, 8, 7),
    (2, 3, 9, 8),
    (3, 4, 10, 9),
    (4, 5, 11, 10),
    (5, 0, 6, 11)
]

edges = []

filename = "mosquito"
directory = "ABSOLUTE_PATH_TO_SVG_OR_RELATIVE_PATH_FROM_BLENDER_FILE_LOCATION" # <------ CHANGE THIS
svg = directory + filename + ".svg"
stl = directory + filename + ".stl"

def generate_hexagons():
    mesh_data = bpy.data.meshes.new("hexagon_data")
    mesh_data.from_pydata(verts, edges, faces)

    mesh_obj = bpy.data.objects.new("hexagon_object", mesh_data)

    mesh_obj.location.x += l
    mesh_obj.location.y += (sqrt(3)*l)/2

    bpy.context.collection.objects.link(mesh_obj)
    
    boolean_modifier = mesh_obj.modifiers.new(name="My Boolean", type='BOOLEAN')
    boolean_modifier.operation = 'UNION'
    boolean_modifier.operand_type = 'COLLECTION'
    boolean_modifier.collection = bpy.data.collections[filename + ".svg"]
    
    bpy.ops.object.modifier_apply(modifier="My Boolean")
    
def import_svg_and_extrude(svg_file):
    # Import SVG as curves
     bpy.ops.import_curve.svg(filepath=svg_file)

    # Select all curves
     bpy.ops.object.select_all(action='DESELECT')
     bpy.ops.object.select_by_type(type='CURVE')

     # Check if any curves are selected
     if bpy.context.selected_objects:
         # Join the selected curves into one object
         bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
         bpy.ops.object.join()
         obj = bpy.context.active_object
         obj.location = bpy.context.scene.cursor.location
         bpy.context.object.data.extrude = 0.0252
         
         obj.location.y += 0.02
         obj.location.x += 0.02
                 
         scale = 79.45
         obj.scale.x *= scale
         obj.scale.y *= scale
         obj.scale.z *= scale
         bpy.ops.object.convert(target='MESH')

         bpy.context.active_object.select_set(False)

def export_to_stl():
    context = bpy.context
    scene = context.scene
    viewlayer = context.view_layer


    obs = [o for o in scene.objects if o.type == 'MESH']
    bpy.ops.object.select_all(action='DESELECT')    

    for ob in obs:
        print(ob.name)
        viewlayer.objects.active = ob
        if ob.name == "hexagon_object":
            ob.select_set(True)
            bpy.ops.export_mesh.stl(
                    filepath=str(stl),
                    use_selection=True)
            ob.select_set(False)

def remove_all():
    scene = bpy.context.scene
    bpy.data.scenes.new("Scene")
    bpy.data.scenes.remove(scene, do_unlink=True)
  
import_svg_and_extrude(svg)
generate_hexagons()      
export_to_stl()
#remove_all()
