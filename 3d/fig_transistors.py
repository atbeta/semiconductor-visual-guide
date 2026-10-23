"""第 12 章：平面 / FinFET / GAA 三代结构，正交 3D 渲染。

运行：
  /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup \
      --python 3d/fig_transistors.py -- 输出路径.png
"""
import bpy
import sys
import os

FABKIT = os.path.expanduser("~/Projects/fabkit")
if FABKIT not in sys.path:
    sys.path.insert(0, FABKIT)
import fabkit as kit  # noqa: E402
kit.configure(engine="CYCLES", samples=96)

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[0] if argv else os.path.abspath("assets/3d/transistors.png")

kit.reset()
S = kit.mat("substrate", kit.PALETTE["substrate"], rough=0.55)
N = kit.mat("nplus", kit.PALETTE["nplus"], rough=0.4)
G = kit.mat("gate", kit.PALETTE["gate"], rough=0.32, metal=0.2)
GX = kit.mat("gate_glass", kit.PALETTE["gate"], rough=0.25, alpha=0.35)
OX = kit.mat("oxide", kit.PALETTE["oxide"], rough=0.2, alpha=0.85)
SH = kit.mat("sheet", kit.PALETTE["sheet"], rough=0.35)

W, D, H = 1.6, 1.15, 0.32
Z = H


def base(x):
    kit.box("sub", (W, D, H), (x, 0, H / 2), S, bevel=0.025)


# ---------- 1. 平面 ----------
x = -2.6
base(x)
kit.box("sd_l", (0.34, 0.66, 0.14), (x - 0.44, 0, Z + 0.07), N)
kit.box("sd_r", (0.34, 0.66, 0.14), (x + 0.44, 0, Z + 0.07), N)
kit.box("ox", (0.54, 0.54, 0.03), (x, 0, Z + 0.15), OX, bevel=0.005)
kit.box("gate", (0.5, 0.5, 0.18), (x, 0, Z + 0.255), G, bevel=0.015)

# ---------- 2. FinFET ----------
x = 0
base(x)
# 鳍沿 Y 方向立起来，两端是源漏
kit.box("fin", (0.12, 1.15, 0.58), (x, 0, Z + 0.29), SH, bevel=0.015)
# 栅极横跨鳍的中段（像一个桥），盖住鳍的上半部，两端露出鳍
kit.box("gate", (0.62, 0.3, 0.5), (x, 0, Z + 0.42), G, bevel=0.015)

# ---------- 3. GAA ----------
x = 2.6
base(x)
for i, z in enumerate((0.20, 0.38, 0.56)):
    kit.box(f"sheet{i}", (0.92, 0.74, 0.06), (x, 0, Z + z), SH, bevel=0.015)
kit.box("gaa_gate", (1.04, 0.86, 0.56), (x, 0, Z + 0.38), GX, bevel=0.02)

kit.ortho_camera(loc=(6.4, -8.4, 5.6), target=(0, 0, 0.32), scale=7.9)
kit.lights()
kit.render(OUT, 1800, 640)

# 同时导出 glb，供 three.js 网页用
if len(argv) > 1 and argv[1].endswith(".glb"):
    bpy.ops.export_scene.gltf(filepath=argv[1], export_format="GLB",
                              export_apply=True, export_yup=True)
    print("EXPORTED", argv[1])
