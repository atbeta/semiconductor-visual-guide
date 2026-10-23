"""第 1 章：晶圆厂剖面（FFU 送风 / 天车搬运 / 洁净室地面 / 地板下管线）。

做成「切开的建筑」：地面只铺到一半，露出下面的回风空间与管线，
这样才能同时看到三层是怎么叠起来的。

运行：
  /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup \
      --python 3d/fig_fab.py -- 输出.png [输出.glb]
"""
import bpy
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[0] if argv else os.path.abspath("assets/3d/fab-section.png")

kit.reset()
F = kit.mat("floor", (0.72, 0.76, 0.82, 1), rough=0.65)
W = kit.mat("wall", (0.58, 0.64, 0.72, 1), rough=0.7)
EQ = kit.mat("tool", (0.86, 0.88, 0.92, 1), rough=0.45)
ACC = kit.mat("accent", kit.PALETTE["nplus"], rough=0.35)
AMB = kit.mat("amber", kit.PALETTE["gate"], rough=0.35, metal=0.2)
PIPE = kit.mat("pipe", (0.62, 0.66, 0.72, 1), rough=0.35, metal=0.6)
PIPE2 = kit.mat("pipe2", (0.55, 0.62, 0.70, 1), rough=0.35, metal=0.5)
GLASS = kit.mat("glass", (0.75, 0.85, 0.95, 1), rough=0.15, alpha=0.25)

# ---------- 楼板与结构 ----------
# 下层地板（回风空间底）
kit.box("base", (7.0, 4.6, 0.18), (0, 0, 0.09), W, bevel=0.02)

# 洁净室地面：只铺左半边（切面），右半边敞开露出下层
kit.box("floor", (4.3, 4.6, 0.16), (-1.35, 0, 1.30), F, bevel=0.015)
# 地面切口处的加强边
kit.box("floor_edge", (0.14, 4.6, 0.22), (0.79, 0, 1.28), W, bevel=0.01)

# 天花板做成半透明：既看得到送风口，又不会挡住室内
FOG = kit.mat("ceil_glass", (0.86, 0.90, 0.96, 1), rough=0.2, alpha=0.16)
kit.box("ceil", (7.0, 4.6, 0.06), (0, 0, 3.34), FOG, bevel=0.01)
for gx in (-2.6, -1.3, 0.0, 1.3, 2.6):
    for gy in (-1.4, 0.0, 1.4):
        kit.box("ffu", (0.95, 0.95, 0.1), (gx, gy, 3.22), EQ, bevel=0.01)

# 侧墙（只留后墙，做出剖切感）
kit.box("wall", (7.0, 0.16, 2.0), (0, 2.2, 2.2), W, bevel=0.01)

# ---------- 设备（洁净室地面上的三台） ----------
for i, (ex, h) in enumerate([(-2.4, 1.15), (-1.0, 1.0), (0.35, 1.25)]):
    kit.box("tool", (0.9, 1.1, h), (ex, -0.2, 1.38 + h / 2), EQ, bevel=0.03)
    # 前端操作面板
    kit.box("panel", (0.5, 0.06, 0.4), (ex, -0.78, 1.38 + h * 0.55), ACC, bevel=0.01)
    # load port
    kit.box("port", (0.5, 0.3, 0.22), (ex, -0.95, 1.38 + 0.5), AMB, bevel=0.012)

# ---------- 天车轨道 + FOUP ----------
kit.box("rail", (7.0, 0.16, 0.12), (0, -1.35, 2.62), PIPE, bevel=0.02)
# 小车
kit.box("oht", (0.4, 0.34, 0.26), (-0.32, -1.35, 2.44), EQ, bevel=0.02)
# 吊带
kit.box("hoist", (0.07, 0.07, 0.45), (-0.32, -1.35, 2.14), PIPE2, bevel=0.01)
# FOUP（半透明，能看见里面叠着的晶圆）
kit.box("foup", (0.62, 0.6, 0.4), (-0.32, -1.35, 1.70), GLASS, bevel=0.035)
for k in range(4):
    kit.box("wafer_in", (0.5, 0.48, 0.014), (-0.32, -1.35, 1.56 + k * 0.085), ACC, bevel=0.002)

# ---------- 地板下的回风空间：管线与泵 ----------
# 沿 X 方向的长管线（不同高度与位置）
for py, pz, r in [(-0.9, 0.55, 0.11), (-0.9, 0.88, 0.09), (0.35, 0.62, 0.12)]:
    kit.cyl("pipe", r, 2.5, (2.1, py, pz), PIPE, verts=24, rot=(0, 1.5708, 0))
for py in (-0.9, 0.35):
    kit.cyl("riser", 0.09, 1.0, (1.0, py, 0.62), PIPE2, verts=20)
kit.box("pump", (0.55, 0.45, 0.4), (2.7, -0.9, 0.4), EQ, bevel=0.03)
kit.box("panel2", (0.5, 0.08, 0.28), (2.4, 0.2, 0.42), ACC, bevel=0.01)

kit.ortho_camera(loc=(7.6, -12.0, 3.6), target=(0, 0, 1.55), scale=9.8)
kit.lights()
kit.render(OUT, 1700, 1050)

if len(argv) > 1 and argv[1].endswith(".glb"):
    bpy.ops.export_scene.gltf(filepath=argv[1], export_format="GLB",
                              export_apply=True, export_yup=True)
    print("EXPORTED", argv[1])
