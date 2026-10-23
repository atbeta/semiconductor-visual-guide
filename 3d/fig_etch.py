"""第 6 章：等离子刻蚀腔的 3D 剖面。

腔壁透明，能看见里面：顶部电极 + 气体喷淋头、中间发光的等离子体、
下方电极上的晶圆，以及底部的抽气口。

运行：
  /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup \
      --python 3d/fig_etch.py -- 输出.png [输出.glb]
"""
import bpy
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[0] if argv else os.path.abspath("assets/3d/etch-chamber.png")

kit.reset()
WALL = kit.mat("wall", (0.55, 0.65, 0.78, 1), rough=0.15, alpha=0.10)
MET = kit.mat("metal", (0.72, 0.76, 0.84, 1), rough=0.35, metal=0.55)
ELEC = kit.mat("elec", (0.46, 0.52, 0.62, 1), rough=0.4, metal=0.3)
PL = kit.mat("plasma", (0.78, 0.42, 1.0, 1), rough=0.5, alpha=0.20, emit=1.1)
WAF = kit.mat("wafer", (0.58, 0.68, 0.86, 1), rough=0.2, metal=0.5)
GAS = kit.mat("gas", (0.42, 0.85, 0.72, 1), rough=0.4, alpha=0.45)

R = 1.5   # 腔体半径

# 腔壁（透明圆筒）
kit.cyl("chamber", R, 2.4, (0, 0, 1.45), WALL, verts=64, bevel=0.0)
# 顶盖与底盘
kit.cyl("lid", R + 0.12, 0.12, (0, 0, 2.68), MET, verts=64, bevel=0.02)
kit.cyl("base", R + 0.12, 0.14, (0, 0, 0.20), MET, verts=64, bevel=0.02)

# 气体入口 + 喷淋头
kit.cyl("inlet", 0.14, 0.5, (0, 0, 2.95), MET, verts=24, bevel=0.01)
kit.cyl("shower", 1.15, 0.12, (0, 0, 2.36), ELEC, verts=64, bevel=0.01)
for gx in (-0.6, -0.3, 0.0, 0.3, 0.6):
    for gy in (-0.3, 0.0, 0.3):
        kit.cyl("hole", 0.035, 0.14, (gx, gy, 2.35), GAS, verts=12, bevel=0.002)

# 等离子体（发光柱）
kit.cyl("plasma", 1.05, 0.8, (0, 0, 1.85), PL, verts=64, bevel=0.0)

# 下电极 + 晶圆
kit.cyl("lower", 1.2, 0.22, (0, 0, 1.10), ELEC, verts=64, bevel=0.02)
kit.cyl("wafer", 0.95, 0.05, (0, 0, 1.235), WAF, verts=64, bevel=0.006)

# 抽气口
kit.cyl("exhaust", 0.22, 0.45, (1.15, 0, 0.42), MET, verts=24, bevel=0.01)

kit.ortho_camera(loc=(4.6, -7.2, 4.0), target=(0, 0, 1.45), scale=4.3)
kit.lights()
kit.render(OUT, 1400, 1100)

if len(argv) > 1 and argv[1].endswith(".glb"):
    bpy.ops.export_scene.gltf(filepath=argv[1], export_format="GLB",
                              export_apply=True, export_yup=True)
    print("EXPORTED", argv[1])
