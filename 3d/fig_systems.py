"""第 23 章：工厂系统如何指挥晶圆流转。

四台设备排成一排，天车在头顶轨道上搬 FOUP；地面上用发光路径标出
「软件决定的路线」，说明晶圆走哪一站不是人决定的，是系统决定的。

运行：
  /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup \
      --python 3d/fig_systems.py -- 输出.png [输出.glb]
"""
import bpy
import sys
import os
import math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[0] if argv else os.path.abspath("assets/3d/fab-route.png")

kit.reset()
F = kit.mat("floor", (0.70, 0.74, 0.80, 1), rough=0.7)
EQ = kit.mat("tool", (0.86, 0.88, 0.92, 1), rough=0.45)
ACC = kit.mat("accent", kit.PALETTE["nplus"], rough=0.35)
AMB = kit.mat("amber", kit.PALETTE["gate"], rough=0.3, metal=0.2)
ROUTE = kit.mat("route", (0.95, 0.68, 0.18, 1), rough=0.45, emit=0.55)
PIPE = kit.mat("pipe", (0.60, 0.64, 0.70, 1), rough=0.35, metal=0.6)
GLASS = kit.mat("glass", (0.78, 0.88, 0.96, 1), rough=0.15, alpha=0.3)

# 地面
kit.box("floor", (8.0, 4.2, 0.16), (0, 0, 0.08), F, bevel=0.02)

TOOLS = [-2.7, -0.9, 0.9, 2.7]
PORT_Y = -1.05
for i, tx in enumerate(TOOLS):
    kit.box("tool", (0.95, 1.25, 1.1), (tx, 0.15, 0.71), EQ, bevel=0.035)
    # 装载口
    kit.box("port", (0.55, 0.26, 0.3), (tx, PORT_Y, 0.78), AMB, bevel=0.018)
    # 状态灯
    kit.cyl("lamp", 0.05, 0.12, (tx + 0.45, 0.6, 1.45), ACC, verts=16)

# 天车轨道
kit.box("rail", (8.0, 0.14, 0.12), (0, 0.95, 2.55), PIPE, bevel=0.02)

# 两辆天车 + FOUP
for hx, hz in [(-1.8, 2.35), (1.4, 2.35)]:
    kit.box("oht", (0.4, 0.34, 0.26), (hx, 0.95, hz), EQ, bevel=0.02)
    kit.box("hoist", (0.06, 0.06, 0.42), (hx, 0.95, hz - 0.32), PIPE, bevel=0.01)
    kit.box("foup", (0.5, 0.48, 0.34), (hx, 0.95, hz - 0.72), GLASS, bevel=0.03)
    for k in range(3):
        kit.box("wafer", (0.4, 0.38, 0.012), (hx, 0.95, hz - 0.84 + k * 0.075), ACC, bevel=0.002)

# ---------- 软件决定的路径：地面上发光的折线 ----------
def seg(p0, p1, r=0.028):
    vec = (p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2])
    length = math.sqrt(sum(v * v for v in vec))
    mid = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, (p0[2] + p1[2]) / 2)
    if abs(vec[0]) > abs(vec[1]):
        size = (length, r * 2, r * 2)
    else:
        size = (r * 2, length, r * 2)
    kit.box("route", size, mid, ROUTE, bevel=0.01)

z = 0.18
pts = [(-3.6, -1.62), (-2.7, -1.62), (-2.7, -1.32)]
for i, tx in enumerate(TOOLS):
    pts.append((tx, -1.32))
    if i + 1 < len(TOOLS):
        pts.append((tx, -1.62))
        pts.append((TOOLS[i + 1], -1.62))
pts.append((2.7, -1.95))
for a, b in zip(pts, pts[1:]):
    seg((a[0], a[1], z), (b[0], b[1], z))

# 队列里等待的 FOUP（地面上）
for qx in (-3.4, -3.05):
    kit.box("foup_q", (0.26, 0.26, 0.2), (qx, -1.75, z + 0.1), GLASS, bevel=0.02)

kit.ortho_camera(loc=(6.8, -9.6, 5.6), target=(0, 0.1, 1.05), scale=10.4)
kit.lights()
kit.render(OUT, 1700, 900)

if len(argv) > 1 and argv[1].endswith(".glb"):
    bpy.ops.export_scene.gltf(filepath=argv[1], export_format="GLB",
                              export_apply=True, export_yup=True)
    print("EXPORTED", argv[1])
