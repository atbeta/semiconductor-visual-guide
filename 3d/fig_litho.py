"""第 4 章：光刻机的光路（正交 3D）。

从上到下：光源 → 照明透镜 → 掩模版 → 投影物镜 → 晶圆。
光路做成半透明的琥珀色柱，只在穿过掩模开口的地方变细。

运行：
  /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup \
      --python 3d/fig_litho.py -- 输出.png [输出.glb]
"""
import bpy
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[0] if argv else os.path.abspath("assets/3d/litho-column.png")

kit.reset()
MET = kit.mat("metal", (0.74, 0.78, 0.86, 1), rough=0.4, metal=0.5)
BARREL = kit.mat("barrel", (0.62, 0.68, 0.78, 1), rough=0.15, alpha=0.30)
LENS = kit.mat("lens", (0.55, 0.82, 0.95, 1), rough=0.1, alpha=0.42)
BEAM = kit.mat("beam", (0.98, 0.74, 0.25, 1), rough=0.5, alpha=0.16, emit=0.6)
MASK = kit.mat("mask", (0.30, 0.36, 0.46, 1), rough=0.5)
HOLE = kit.mat("hole", (0.98, 0.86, 0.55, 1), rough=0.4, emit=0.8)
WAF = kit.mat("wafer", (0.58, 0.68, 0.86, 1), rough=0.2, metal=0.5)
BASE = kit.mat("base", (0.62, 0.66, 0.74, 1), rough=0.6)

# 机台底座与晶圆台
kit.box("stage_base", (2.6, 2.6, 0.3), (0, 0, 0.15), BASE, bevel=0.03)
kit.cyl("wafer", 0.95, 0.05, (0, 0, 0.33), WAF, verts=64, bevel=0.008)

# 光路（贯穿的柱子）
kit.cyl("beam", 0.4, 3.05, (0, 0, 1.87), BEAM, verts=48, bevel=0.0)

# 投影物镜：一个大镜筒 + 两片透镜
kit.cyl("barrel", 0.62, 1.0, (0, 0, 1.35), BARREL, verts=48, bevel=0.02)
kit.cyl("lens1", 0.5, 0.09, (0, 0, 1.12), LENS, verts=48, bevel=0.01)
kit.cyl("lens2", 0.5, 0.09, (0, 0, 1.58), LENS, verts=48, bevel=0.01)

# 掩模版（带开口）
kit.box("mask", (1.5, 1.5, 0.05), (0, 0, 2.05), MASK, bevel=0.008)
for gx in (-0.3, 0.0, 0.3):
    kit.box("hole", (0.16, 0.5, 0.06), (gx, 0, 2.06), HOLE, bevel=0.004)

# 照明系统
kit.cyl("illum", 0.55, 0.55, (0, 0, 2.55), BARREL, verts=48, bevel=0.02)
kit.cyl("lens3", 0.45, 0.09, (0, 0, 2.32), LENS, verts=48, bevel=0.01)

# 光源
kit.cyl("source", 0.34, 0.4, (0, 0, 3.15), MET, verts=32, bevel=0.02)
kit.cyl("lamp", 0.24, 0.12, (0, 0, 3.36), kit.mat("lamp", (1.0, 0.85, 0.45, 1), rough=0.3, emit=3.0), verts=32)

# 三根支柱，让整台机器有结构感
for ang in (0.6, 2.7, 4.8):
    import math
    x, y = math.cos(ang) * 1.05, math.sin(ang) * 1.05
    kit.cyl("post", 0.06, 2.2, (x, y, 1.4), MET, verts=16)

kit.ortho_camera(loc=(5.2, -7.6, 4.6), target=(0, 0, 1.7), scale=4.8)
kit.lights()
kit.render(OUT, 1300, 1100)

if len(argv) > 1 and argv[1].endswith(".glb"):
    bpy.ops.export_scene.gltf(filepath=argv[1], export_format="GLB",
                              export_apply=True, export_yup=True)
    print("EXPORTED", argv[1])
