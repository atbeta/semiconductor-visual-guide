"""第 13 章：DRAM 1T1C 存储单元，正交 3D 渲染。

运行：
  /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup \
      --python 3d/fig_dram.py -- 输出.png
"""
import bpy
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[0] if argv else os.path.abspath("assets/3d/dram-cell.png")

kit.reset()
S = kit.mat("substrate", kit.PALETTE["substrate"], rough=0.55)
N = kit.mat("nplus", kit.PALETTE["nplus"], rough=0.4)
G = kit.mat("gate", kit.PALETTE["gate"], rough=0.3, metal=0.2)
M = kit.mat("metal", kit.PALETTE["metal"], rough=0.25, metal=0.6)
C = kit.mat("cap_glass", kit.PALETTE["gate"], rough=0.25, metal=0.1, alpha=0.34)
D = kit.mat("dark", kit.PALETTE["dark"], rough=0.6)

# 衬底
kit.box("sub", (3.0, 1.9, 0.3), (0, 0, 0.15), S, bevel=0.03)

# 埋入式字线（横穿衬底的一条沟槽）
kit.box("wl", (3.5, 0.34, 0.14), (0, -0.42, 0.33), D, bevel=0.02)
kit.box("wl_cap", (3.5, 0.3, 0.03), (0, -0.42, 0.41), G, bevel=0.01)

# 源/漏区
kit.box("sd_l", (0.36, 0.4, 0.1), (-0.55, -0.1, 0.35), N, bevel=0.01)
kit.box("sd_r", (0.36, 0.4, 0.1), (0.55, -0.1, 0.35), N, bevel=0.01)

# 存储节点接触
kit.cyl("contact", 0.09, 0.34, (0.55, -0.1, 0.55), M, verts=32)

# 圆柱电容：外电极 + 内电极
kit.cyl("cap_out", 0.42, 0.95, (0.55, -0.1, 1.1), C, verts=48, bevel=0.02)
kit.cyl("cap_in", 0.3, 0.8, (0.55, -0.1, 1.13), D, verts=48, bevel=0.01)
kit.cyl("cap_hole", 0.18, 0.84, (0.55, -0.1, 1.14), S, verts=48, bevel=0.01)

# 位线
kit.cyl("bl_contact", 0.09, 0.5, (-0.55, -0.1, 0.6), M, verts=32)
kit.box("bl", (2.4, 0.2, 0.1), (-0.25, -0.78, 0.95), M, bevel=0.02)

# 电容顶部电极（横跨）
kit.box("plate", (1.5, 0.9, 0.08), (0.35, -0.1, 1.74), M, bevel=0.02)

kit.ortho_camera(loc=(5.2, -6.8, 4.6), target=(0.0, -0.15, 0.8), scale=5.4)
kit.lights()
kit.render(OUT, 1400, 900)
