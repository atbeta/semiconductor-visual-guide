"""第 23 章：工厂系统如何指挥晶圆流转（用 fabkit 模块拼装）。

四个工位：设备柜体 + 装载口 + HMI + 警示灯，天车在新轨道上搬 FOUP。
地面发光的折线是「系统决定的路线」。

  blender -b --factory-startup --python 3d/fig_systems.py -- 输出.png [输出.glb]
"""
import bpy
import sys
import os
import math

FABKIT = os.path.expanduser("~/Projects/fabkit")
if FABKIT not in sys.path:
    sys.path.insert(0, FABKIT)
import fabkit as fk  # noqa: E402
fk.configure(engine="CYCLES", samples=96)

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[0] if argv else os.path.abspath("assets/3d/fab-route.png")

fk.reset()
M = fk.materials()
ROUTE = fk.mat("route", (0.95, 0.68, 0.18, 1), rough=0.45, emit=0.55)

# 地面
fk.box("floor", (8.0, 4.2, 0.16), (0, 0, 0.08), M["panel"], bevel=0.02)

TOOLS = [-2.7, -0.9, 0.9, 2.7]
for i, tx in enumerate(TOOLS):
    fk.modules.tool_body(f"t{i}", (tx, 0.15, 0.16), M, w=1.0, d=1.3, h=1.1)
    fk.modules.load_port(f"lp{i}", (tx, -0.72, 0.16), M)
    fk.modules.hmi(f"hmi{i}", (tx + 0.62, -0.42, 1.0), M)
    fk.modules.stack_light(f"sl{i}", (tx + 0.36, 0.55, 1.32), M)
    fk.modules.cable_tray(f"ct{i}", (tx, 0.85, 1.52), 0.9, M)

# 天车轨道 + 两个 FOUP
fk.box("rail", (8.6, 0.14, 0.12), (0, 1.15, 2.35), M["metal"], bevel=0.02)
for i, hx in enumerate((-1.3, 1.4)):
    fk.box(f"oht{i}", (0.34, 0.30, 0.22), (hx, 1.15, 2.18), M["panel"], bevel=0.02)
    fk.box(f"hoist{i}", (0.06, 0.06, 0.36), (hx, 1.15, 1.90), M["metal"], bevel=0.008)
    fk.modules.foup(f"foup{i}", (hx, 1.15, 1.55), M)

# 发光路径：沿装载口前方走一条折线
def seg(p0, p1, r=0.028):
    vec = (p1[0]-p0[0], p1[1]-p0[1]); length = math.hypot(*vec)
    mid = ((p0[0]+p1[0])/2, (p0[1]+p1[1])/2, 0.18)
    size = (length, r*2, r*2) if abs(vec[0]) > abs(vec[1]) else (r*2, length, r*2)
    fk.box("route", size, mid, ROUTE, bevel=0.01)

z = 0.18
pts = [(-3.6, -1.55), (-2.7, -1.55), (-2.7, -1.30)]
for i, tx in enumerate(TOOLS):
    pts.append((tx, -1.30))
    if i + 1 < len(TOOLS):
        pts.append((tx, -1.55)); pts.append((TOOLS[i+1], -1.55))
pts.append((2.7, -1.9))
for a, b in zip(pts, pts[1:]):
    seg((a[0], a[1]), (b[0], b[1]))

fk.ortho_camera((6.8, -9.6, 5.6), target=(0, 0.1, 1.05), scale=10.4)
fk.lights()
fk.render(OUT, 1700, 900)

if len(argv) > 1 and argv[1].endswith(".glb"):
    bpy.ops.export_scene.gltf(filepath=argv[1], export_format="GLB",
                              export_apply=True, export_yup=True)
    print("EXPORTED", argv[1])
