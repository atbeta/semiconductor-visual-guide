"""PVD vs CVD：两种沉积腔里，材料是怎么到晶圆上的。

左 PVD：靶材在上，原子被轰出来直线飞向晶圆 → 方向性强，台阶侧壁盖不住。
右 CVD：气体从喷淋头下来，在表面反应成膜 → 到处都能长，保形。

  blender -b --factory-startup --python 3d/fig_deposition.py -- 输出.png
"""
import bpy
import sys
import os
import random

FABKIT = os.path.expanduser("~/Projects/fabkit")
if FABKIT not in sys.path:
    sys.path.insert(0, FABKIT)
import fabkit as fk  # noqa: E402
fk.configure(engine="CYCLES", samples=96)

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[0] if argv else os.path.abspath("assets/3d/deposition.png")

fk.reset()
M = fk.materials()
ATOM = fk.mat("atom", (0.85, 0.72, 0.45, 1), rough=0.35, metal=0.4)
GAS = fk.mat("gas", (0.45, 0.85, 0.75, 1), rough=0.4, emit=0.5)

SUB_W, SUB_H = 1.6, 0.62
TRENCH_W, TRENCH_D = 0.34, 0.46


def trench_substrate(prefix, x, y, z_top):
    """带一条通道的衬底：左右两块 + 低一层的槽底。z_top 是衬底上表面。"""
    left = (SUB_W - TRENCH_W) / 2
    bottom = z_top - SUB_H
    fk.box(f"{prefix}_l", (left, 0.9, SUB_H),
           (x - TRENCH_W / 2 - left / 2, y, bottom + SUB_H / 2), M["substrate"], bevel=0.01)
    fk.box(f"{prefix}_r", (left, 0.9, SUB_H),
           (x + TRENCH_W / 2 + left / 2, y, bottom + SUB_H / 2), M["substrate"], bevel=0.01)
    floor_h = SUB_H - TRENCH_D
    fk.box(f"{prefix}_b", (TRENCH_W, 0.9, floor_h),
           (x, y, bottom + floor_h / 2), M["substrate"], bevel=0.008)
    return z_top


def film(prefix, x, y, z_top, top_t, side_t, bot_t, mat):
    """在通道上铺膜：顶面 / 侧壁 / 槽底三个厚度分别控制。"""
    left = (SUB_W - TRENCH_W) / 2
    fk.box(f"{prefix}_top_l", (left, 0.92, top_t),
           (x - TRENCH_W / 2 - left / 2, y, z_top + top_t / 2), mat, bevel=0.004)
    fk.box(f"{prefix}_top_r", (left, 0.92, top_t),
           (x + TRENCH_W / 2 + left / 2, y, z_top + top_t / 2), mat, bevel=0.004)
    fk.box(f"{prefix}_sw_l", (side_t, 0.9, TRENCH_D - bot_t),
           (x - TRENCH_W / 2 + side_t / 2, y, z_top - (TRENCH_D - bot_t) / 2), mat, bevel=0.003)
    fk.box(f"{prefix}_sw_r", (side_t, 0.9, TRENCH_D - bot_t),
           (x + TRENCH_W / 2 - side_t / 2, y, z_top - (TRENCH_D - bot_t) / 2), mat, bevel=0.003)
    fk.box(f"{prefix}_bot", (TRENCH_W, 0.9, bot_t),
           (x, y, z_top - TRENCH_D + bot_t / 2), mat, bevel=0.003)


# ---------------- 左：PVD ----------------
X = -1.45
fk.modules.chamber("pvd", (X, 0, 0.05), M, r=0.95, h=1.9)
for o in bpy.data.objects:
    if o.name.startswith("pvd_wall"): o.data.materials[0] = fk.mat("glass_thin", (0.86, 0.92, 0.98, 1), rough=0.1, alpha=0.13)
top = trench_substrate("pvd_sub", X, 0, 0.62)
film("pvd_f", X, 0, top, 0.10, 0.012, 0.04, M["metal"])
# 靶材
fk.cyl("pvd_target", 0.55, 0.10, (X, 0, 2.10), M["alum"], verts=48, bevel=0.01)
# 方向性原子：一束窄的、向下的小球
random.seed(3)
for i in range(26):
    px = X + random.uniform(-0.35, 0.35)
    py = random.uniform(-0.25, 0.25)
    pz = random.uniform(1.0, 1.95)
    fk.sphere(f"pvd_atom{i}", 0.028, (px, py, pz), ATOM, segs=10, rings=8)

# ---------------- 右：CVD ----------------
X = 1.45
fk.modules.chamber("cvd", (X, 0, 0.05), M, r=0.95, h=1.9)
for o in bpy.data.objects:
    if o.name.startswith("cvd_wall"): o.data.materials[0] = fk.mat("glass_thin", (0.86, 0.92, 0.98, 1), rough=0.1, alpha=0.13)
top = trench_substrate("cvd_sub", X, 0, 0.62)
film("cvd_f", X, 0, top, 0.075, 0.075, 0.075, M["oxide"])
# 喷淋头
fk.cyl("cvd_shower", 0.62, 0.09, (X, 0, 2.05), M["metal"], verts=48, bevel=0.008)
for gx in (-0.3, -0.1, 0.1, 0.3):
    for gy in (-0.2, 0.0, 0.2):
        fk.cyl("cvd_hole", 0.03, 0.10, (X + gx, gy, 2.03), GAS, verts=10, bevel=0.002)
# 气体分子：充满整个腔体
random.seed(11)
for i in range(40):
    px = X + random.uniform(-0.75, 0.75)
    py = random.uniform(-0.6, 0.6)
    pz = random.uniform(0.75, 1.95)
    fk.sphere(f"cvd_mol{i}", 0.022, (px, py, pz), GAS, segs=10, rings=8)

fk.ortho_camera((2.4, -9.4, 2.6), target=(0, 0, 1.05), scale=6.0)
fk.lights("studio")
fk.render(OUT, 1700, 1000)
