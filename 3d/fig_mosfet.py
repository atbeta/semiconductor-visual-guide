"""第 2 章：MOSFET 的立体透视（栅极半透明，露出沟道）。

和 2D 剖面不同的地方：栅极做成半透明，能看见它下面的沟道到底有多长、
源漏之间隔着什么。

运行：
  /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup \
      --python 3d/fig_mosfet.py -- 输出.png [输出.glb]
"""
import bpy
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[0] if argv else os.path.abspath("assets/3d/mosfet.png")

kit.reset()
SUB = kit.mat("sub", (0.60, 0.66, 0.76, 1), rough=0.6)
SD = kit.mat("sd", kit.PALETTE["nplus"], rough=0.35)
CH = kit.mat("chan", (0.45, 0.70, 0.95, 1), rough=0.35, emit=0.9)
OX = kit.mat("ox", kit.PALETTE["oxide"], rough=0.15, alpha=0.28)
G = kit.mat("gate", kit.PALETTE["gate"], rough=0.25, metal=0.15, alpha=0.22)
MET = kit.mat("metal", (0.80, 0.84, 0.90, 1), rough=0.25, metal=0.8)

H = 0.42          # 衬底高度
W, D = 3.0, 1.9

# 衬底
kit.box("sub", (W, D, H), (0, 0, H / 2), SUB, bevel=0.03)

# 源 / 漏：顶面比衬底高一点点（0.004），避免共面产生摩尔纹
for name, x0, x1 in [("sd_l", -1.15, -0.55), ("sd_r", 0.55, 1.15)]:
    kit.box(name, (x1 - x0, 1.1, 0.13), ((x0 + x1) / 2, 0, H - 0.061), SD, bevel=0.012)

# 沟道：两源漏之间，表面薄薄一层，略高于源漏
kit.box("chan", (1.1, 0.9, 0.06), (0, 0, H - 0.02), CH, bevel=0.008)

# 栅氧化层（很薄，半透明）
kit.box("ox", (1.26, 0.98, 0.03), (0, 0, H + 0.04), OX, bevel=0.004)

# 栅极（半透明，能看见底下的沟道）
kit.box("gate", (1.1, 0.86, 0.2), (0, 0, H + 0.155), G, bevel=0.015)

# 源漏上的接触金属
for xc in (-0.85, 0.85):
    kit.box("contact", (0.32, 0.5, 0.05), (xc, 0, H + 0.03), MET, bevel=0.008)

kit.ortho_camera(loc=(4.6, -6.2, 4.4), target=(0, 0, 0.32), scale=3.9)
kit.lights()
kit.render(OUT, 1500, 1000)

if len(argv) > 1 and argv[1].endswith(".glb"):
    bpy.ops.export_scene.gltf(filepath=argv[1], export_format="GLB",
                              export_apply=True, export_yup=True)
    print("EXPORTED", argv[1])
