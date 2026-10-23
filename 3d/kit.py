"""共用的小工具：材质、基本体、正交相机、三点光。

风格对齐站点：冷灰底 + 琥珀/天蓝强调色，正交投影（平行线不发散），
透明背景，方便深浅两套主题都放得下。
"""
import bpy
import math
import os
from mathutils import Vector

def srgb(c):
    """sRGB → 线性。调色板按 sRGB 写，渲染是线性的，最后再统一转回 sRGB。"""
    def f(x):
        return x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4
    return (f(c[0]), f(c[1]), f(c[2]), 1)


PALETTE = {
    "substrate": (0.56, 0.63, 0.72, 1),
    "silicon":   (0.42, 0.55, 0.72, 1),
    "nplus":     (0.22, 0.74, 0.97, 1),
    "gate":      (0.96, 0.62, 0.04, 1),
    "oxide":     (0.13, 0.83, 0.93, 1),
    "sheet":     (0.38, 0.65, 0.98, 1),
    "metal":     (0.78, 0.82, 0.88, 1),
    "dark":      (0.12, 0.15, 0.2, 1),
}


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_EEVEE"
    sc.render.film_transparent = True
    sc.render.resolution_percentage = 100
    sc.eevee.taa_render_samples = 64
    # 关键：不做 filmic/AgX 色调映射，颜色按 sRGB 原样输出
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    return sc


def mat(name, color, rough=0.45, metal=0.0, alpha=1.0, emit=0.0):
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = srgb(color) if len(color) == 4 and max(color[:3]) <= 1 else color
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    b.inputs["Alpha"].default_value = alpha
    if emit:
        b.inputs["Emission Color"].default_value = color
        b.inputs["Emission Strength"].default_value = emit
    if alpha < 1:
        m.surface_render_method = "BLENDED"
        m.use_backface_culling = False
    return m


def box(name, size, loc, material, bevel=0.02, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    o.scale = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        b = o.modifiers.new("bev", "BEVEL")
        b.width = bevel
        b.segments = 3
        b.harden_normals = True
        bpy.ops.object.shade_smooth()
    o.data.materials.append(material)
    return o


def cyl(name, r, h, loc, material, verts=64, rot=(0, 0, 0), bevel=0.01):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=h, location=loc,
                                        rotation=rot, vertices=verts)
    o = bpy.context.object
    o.name = name
    if bevel:
        b = o.modifiers.new("bev", "BEVEL")
        b.width = bevel
        b.segments = 3
    bpy.ops.object.shade_smooth()
    o.data.materials.append(material)
    return o


def ortho_camera(loc, target, scale):
    """正交相机，自动看向 target。"""
    bpy.ops.object.camera_add(location=loc)
    cam = bpy.context.object
    cam.data.type = "ORTHO"
    cam.data.ortho_scale = scale
    d = Vector(target) - Vector(loc)
    cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    bpy.context.scene.camera = cam
    return cam


def lights():
    """三点光：主光在右上，补光在左下，轮廓光在背后。"""
    def area(name, loc, rot, energy, size, color=(1, 1, 1)):
        bpy.ops.object.light_add(type="AREA", location=loc, rotation=rot)
        l = bpy.context.object
        l.name = name
        l.data.energy = energy
        l.data.size = size
        l.data.color = color
        return l

    area("key", (4, -4, 6), (math.radians(45), 0, math.radians(45)), 420, 6)
    area("fill", (-5, -3, 2.5), (math.radians(70), 0, math.radians(-55)), 110, 7,
         color=(0.8, 0.88, 1))
    area("rim", (0, 5, 4), (math.radians(120), 0, math.radians(180)), 180, 5,
         color=(1, 0.95, 0.9))


def render(path, w=1600, h=1000):
    sc = bpy.context.scene
    sc.render.resolution_x = w
    sc.render.resolution_y = h
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA"
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print("RENDERED", path)


def tube(name, points, radius, material, resolution=4):
    """用曲线生成一根圆管，用来画金线、光纤之类的细长弯曲结构。"""
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = radius
    cu.bevel_resolution = resolution
    cu.resolution_u = 12
    sp = cu.splines.new("BEZIER")
    sp.bezier_points.add(len(points) - 1)
    for i, p in enumerate(points):
        bp = sp.bezier_points[i]
        bp.co = p
        bp.handle_left_type = "AUTO"
        bp.handle_right_type = "AUTO"
    ob = bpy.data.objects.new(name, cu)
    bpy.context.collection.objects.link(ob)
    ob.data.materials.append(material)
    return ob


def world(hdri_path, strength=1.0):
    """用 HDRI 当环境光。EEVEE 下也能提供柔和的反射与补光。"""
    if not os.path.exists(hdri_path):
        return None
    w = bpy.data.worlds.new("HDRI")
    bpy.context.scene.world = w
    w.use_nodes = True
    nt = w.node_tree
    bg = nt.nodes.get("Background")
    env = nt.nodes.new("ShaderNodeTexEnvironment")
    env.image = bpy.data.images.load(hdri_path)
    nt.links.new(env.outputs["Color"], bg.inputs["Color"])
    bg.inputs["Strength"].default_value = strength
    return w
