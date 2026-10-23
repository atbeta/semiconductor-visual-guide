"""第 19 章：晶圆探针测试（CP）装置，正交 3D 渲染。

晶圆吸在卡盘上，探针卡从上方压下来，一排探针落在焊盘上。
运行：
  /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup \
      --python 3d/fig_cp.py -- 输出.png [输出.glb]
"""
import bpy
import sys
import os
import math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[0] if argv else os.path.abspath("assets/3d/cp-test.png")

kit.reset()
S = kit.mat("chuck", kit.PALETTE["substrate"], rough=0.6)
W = kit.mat("wafer", (0.55, 0.66, 0.88, 1), rough=0.22, metal=0.5)
D = kit.mat("die", (0.30, 0.42, 0.60, 1), rough=0.45)
PCB = kit.mat("pcb", (0.30, 0.55, 0.48, 1), rough=0.45, alpha=0.30)
AU = kit.mat("needle", (0.92, 0.72, 0.28, 1), rough=0.25, metal=0.9)

# 卡盘
kit.cyl("chuck", 2.5, 0.5, (0, 0, 0.25), S, verts=72, bevel=0.04)

# 晶圆（薄圆片）
kit.cyl("wafer", 2.2, 0.07, (0, 0, 0.535), W, verts=96, bevel=0.01)

# 晶圆上的裸片阵列（只做中间一小块，避免太密）
d = 0.34
for i in range(-3, 4):
    for j in range(-3, 4):
        if math.hypot(i * d, j * d) < 1.75:
            kit.box("die", (d * 0.86, d * 0.86, 0.02),
                    (i * d, j * d, 0.578), D, bevel=0.004)

# 探针卡（PCB 圆盘）
kit.cyl("pcb", 1.45, 0.12, (0, 0, 2.05), PCB, verts=72, bevel=0.02)
# 探针卡下方的加强环
kit.cyl("ring", 1.3, 0.05, (0, 0, 1.96), S, verts=72, bevel=0.01)

# 探针：从卡片下表面斜向下，聚到晶圆中心区域
import mathutils
for k in range(4):
    ang = math.radians(45 + k * 90)
    for m in range(3):
        rr = 0.30 + m * 0.55
        x0, y0 = math.cos(ang) * rr, math.sin(ang) * rr
        kit.tube("probe",
                 [(x0, y0, 1.92), (x0 * 0.99, y0 * 0.99, 1.3), (x0 * 0.9, y0 * 0.9, 0.596)],
                 0.024, AU)

# 顶部接口
kit.box("head", (0.9, 0.9, 0.26), (0, 0, 2.24), S, bevel=0.03)

kit.ortho_camera(loc=(6.2, -8.0, 6.6), target=(0, 0, 0.95), scale=7.8)
kit.lights()
kit.render(OUT, 1500, 1100)

if len(argv) > 1 and argv[1].endswith(".glb"):
    bpy.ops.export_scene.gltf(filepath=argv[1], export_format="GLB",
                              export_apply=True, export_yup=True)
    print("EXPORTED", argv[1])
