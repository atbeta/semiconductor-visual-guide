"""第 21 章：2.5D 封装（中介层 + 逻辑 die + HBM 堆叠）的正交 3D 渲染。

运行：
  /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup \
      --python 3d/fig_advpack.py -- 输出.png [输出.glb]
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
OUT = argv[0] if argv else os.path.abspath("assets/3d/advpack.png")

kit.reset()
S = kit.mat("substrate", kit.PALETTE["substrate"], rough=0.6)
I = kit.mat("interposer", (0.62, 0.5, 0.86, 1), rough=0.35, alpha=0.45)
D = kit.mat("die", (0.33, 0.45, 0.62, 1), rough=0.4)
H = kit.mat("hbm", (0.25, 0.42, 0.58, 1), rough=0.4)
B = kit.mat("bump", kit.PALETTE["gate"], rough=0.3, metal=0.4)
T = kit.mat("tsv", kit.PALETTE["oxide"], rough=0.25, metal=0.5)

# 封装基板
kit.box("pkg_sub", (5.6, 3.6, 0.3), (0, 0, 0.15), S, bevel=0.03)

# 中介层
kit.box("interposer", (4.8, 2.9, 0.22), (0, 0, 0.41), I, bevel=0.02)

# 逻辑 die
kit.box("logic", (2.1, 2.3, 0.5), (-0.75, 0, 0.77), D, bevel=0.02)

# 三组 HBM：每组 4 层薄片
for i, hx in enumerate((0.95, 1.65, 2.35)):
    for j in range(4):
        kit.box(f"hbm{i}_{j}", (0.56, 1.9, 0.085),
                (hx, 0, 0.57 + j * 0.1), H, bevel=0.006)

# 中介层上的微凸块（逻辑 die 四周）
for gx in (-1.75, -0.75, 0.25):
    for gy in (-1.0, 0, 1.0):
        kit.cyl("bump", 0.055, 0.06, (gx, gy, 0.55), B, verts=20, bevel=0.004)

# 中介层内的 TSV（中介层半透明，能看见）
for gx in (-1.6, -0.4, 0.8, 2.0):
    for gy in (-1.05, 0, 1.05):
        kit.cyl("tsv", 0.045, 0.24, (gx, gy, 0.42), T, verts=16, bevel=0.003)

# 中介层到基板的焊球
for gx in (-1.6, -0.4, 0.8, 2.0):
    for gy in (-1.05, 1.05):
        kit.cyl("ball", 0.085, 0.1, (gx, gy, 0.28), B, verts=20, bevel=0.012)

kit.ortho_camera(loc=(7.0, -8.8, 8.4), target=(0.1, 0, 0.5), scale=7.6)
kit.lights()
kit.render(OUT, 1600, 1000)

if len(argv) > 1 and argv[1].endswith(".glb"):
    bpy.ops.export_scene.gltf(filepath=argv[1], export_format="GLB",
                              export_apply=True, export_yup=True)
    print("EXPORTED", argv[1])
