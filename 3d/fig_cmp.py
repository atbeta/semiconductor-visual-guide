"""第 8 章：CMP 抛光台（正交 3D）。

大盘是抛光盘与抛光垫，上面的承片头把晶圆正面朝下压上去；
旁边有修整器（diamond conditioner）随时把垫面刮毛。

运行：
  /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup \
      --python 3d/fig_cmp.py -- 输出.png [输出.glb]
"""
import bpy
import sys
import os
import math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[0] if argv else os.path.abspath("assets/3d/cmp-platen.png")

kit.reset()
BASE = kit.mat("base", (0.50, 0.55, 0.63, 1), rough=0.6)
PAD = kit.mat("pad", (0.62, 0.58, 0.50, 1), rough=0.75)
HEAD = kit.mat("head", (0.72, 0.76, 0.84, 1), rough=0.35, metal=0.5)
HEADX = kit.mat("head_x", (0.72, 0.78, 0.88, 1), rough=0.15, alpha=0.32)
WAF = kit.mat("wafer", (0.58, 0.68, 0.86, 1), rough=0.2, metal=0.55)
SLURRY = kit.mat("slurry", (0.55, 0.85, 0.75, 1), rough=0.3, alpha=0.55)
COND = kit.mat("cond", (0.82, 0.84, 0.88, 1), rough=0.3, metal=0.7)
ARM = kit.mat("arm", (0.60, 0.64, 0.72, 1), rough=0.4, metal=0.4)

# 机台底座
kit.cyl("base", 2.5, 0.3, (0, 0, 0.15), BASE, verts=72, bevel=0.02)
# 抛光盘 + 抛光垫
kit.cyl("platen", 2.1, 0.18, (0, 0, 0.39), HEAD, verts=72, bevel=0.015)
kit.cyl("pad", 2.0, 0.08, (0, 0, 0.52), PAD, verts=72, bevel=0.01)

# 晶圆（面朝下，压在垫上）
kit.cyl("wafer", 0.85, 0.045, (0.55, 0, 0.585), WAF, verts=64, bevel=0.006)
# 承片头
kit.cyl("head", 0.92, 0.28, (0.55, 0, 0.75), HEADX, verts=64, bevel=0.02)
kit.cyl("head_top", 0.55, 0.12, (0.55, 0, 0.95), HEAD, verts=48, bevel=0.015)
# 驱动轴
kit.cyl("shaft", 0.14, 0.75, (0.55, 0, 1.35), HEAD, verts=24, bevel=0.01)

# 修整器：一根横臂 + 一个小圆盘压在垫上
kit.box("arm", (1.7, 0.16, 0.12), (-0.75, -1.35, 0.95), ARM, bevel=0.015)
kit.cyl("cond", 0.34, 0.12, (-1.4, -1.35, 0.62), COND, verts=32, bevel=0.01)

# 浆料：几滴在垫面上
for ang, rr in [(0.4, 1.5), (1.9, 1.2), (3.4, 1.65), (5.0, 1.1)]:
    x, y = math.cos(ang) * rr, math.sin(ang) * rr
    kit.cyl("drop", 0.13, 0.03, (x, y, 0.575), SLURRY, verts=24, bevel=0.004)

kit.ortho_camera(loc=(5.6, -7.4, 4.6), target=(0, 0, 0.75), scale=6.2)
kit.lights()
kit.render(OUT, 1500, 1000)

if len(argv) > 1 and argv[1].endswith(".glb"):
    bpy.ops.export_scene.gltf(filepath=argv[1], export_format="GLB",
                              export_apply=True, export_yup=True)
    print("EXPORTED", argv[1])
