"""第 20 章：引线键合 vs 倒装芯片，正交 3D 剖面对比。

左边：裸片正放，金线从焊盘打弧到基板，外面是半透明塑封。
右边：裸片翻过来，凸块阵列直接焊在基板上，缝隙填底部填充。

运行：
  /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup \
      --python 3d/fig_packaging.py -- 输出.png [输出.glb]
"""
import bpy
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[0] if argv else os.path.abspath("assets/3d/packaging.png")

kit.reset()
S = kit.mat("substrate", kit.PALETTE["substrate"], rough=0.6)
D = kit.mat("die", (0.33, 0.45, 0.62, 1), rough=0.45)
AU = kit.mat("gold", (0.95, 0.72, 0.25, 1), rough=0.22, metal=0.9)
B = kit.mat("bump", (0.92, 0.62, 0.18, 1), rough=0.28, metal=0.6)
M = kit.mat("mold", (0.72, 0.66, 0.92, 1), rough=0.4, alpha=0.22)
U = kit.mat("underfill", (0.35, 0.8, 0.85, 1), rough=0.3, alpha=0.16)
BALL = kit.mat("ball", (0.78, 0.82, 0.88, 1), rough=0.25, metal=0.7)

SUB_W, SUB_D, SUB_H = 2.4, 1.7, 0.16


def substrate(x):
    kit.box("sub", (SUB_W, SUB_D, SUB_H), (x, 0, SUB_H / 2), S, bevel=0.02)


def balls(x):
    """基板底部的锡球：放在边缘，从侧上方能看到一半。"""
    for bx in (-1.0, -0.5, 0, 0.5, 1.0):
        for by in (-0.72, 0.72):
            kit.cyl("ball", 0.1, 0.12, (x + bx, by, -0.06), BALL, verts=24, bevel=0.014)


# ---------------- 左：引线键合 ----------------
X = -2.1
substrate(X)
DY = 0.25   # 裸片高度
kit.box("die", (1.0, 1.0, DY), (X, 0, SUB_H + DY / 2), D, bevel=0.015)

# 焊盘
pads = [-0.36, -0.12, 0.12, 0.36]
for px in pads:
    kit.box("pad", (0.1, 0.1, 0.03), (X + px, -0.42, SUB_H + DY + 0.015), AU, bevel=0.004)
    kit.box("pad_s", (0.12, 0.12, 0.03), (X + px * 2.4, -0.66, SUB_H + 0.015), AU, bevel=0.004)

# 金线：从裸片焊盘打弧到基板焊盘
for px in pads:
    p0 = (X + px, -0.42, SUB_H + DY + 0.03)
    p1 = (X + px * 2.4, -0.66, SUB_H + 0.03)
    mid = ((p0[0] + p1[0]) / 2, -0.56, SUB_H + DY + 0.42)
    kit.tube("wire", [p0, mid, p1], 0.016, AU)

# 塑封（半透明）
kit.box("mold", (2.0, 1.5, 0.72), (X, -0.05, SUB_H + 0.36), M, bevel=0.03)

# ---------------- 右：倒装芯片 ----------------
X = 2.1
substrate(X)
balls(X)

DY2 = 0.3
z_die_bot = SUB_H + 0.22
kit.box("die_fc", (1.0, 1.0, DY2), (X, 0, z_die_bot + DY2 / 2), D, bevel=0.015)

# 凸块阵列（裸片底部到基板之间）
for gx in (-0.36, -0.12, 0.12, 0.36):
    for gy in (-0.36, -0.12, 0.12, 0.36):
        kit.cyl("bump", 0.058, 0.24, (X + gx, gy, SUB_H + 0.12), AU, verts=20, bevel=0.012)

# 底部填充（很薄的一层，包住凸块）
kit.box("underfill", (1.06, 1.06, 0.18), (X, 0, SUB_H + 0.1), U, bevel=0.008)

kit.ortho_camera(loc=(2.0, -12.5, 6.2), target=(0, 0, 0.36), scale=7.1)
kit.lights()
kit.render(OUT, 1700, 900)

if len(argv) > 1 and argv[1].endswith(".glb"):
    bpy.ops.export_scene.gltf(filepath=argv[1], export_format="GLB",
                              export_apply=True, export_yup=True)
    print("EXPORTED", argv[1])
