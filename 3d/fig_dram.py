"""第 13 章：DRAM 1T1C 存储单元（正交 3D，电容做成开口剖切）。

思路：圆柱电容整颗画出来，里面的电极永远看不见。所以把它做成
「少了前壁的杯子」——左壁、右壁、后壁、底，前面敞开，一眼看到内电极。

运行：
  /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup \
      --python 3d/fig_dram.py -- 输出.png [输出.glb]
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
D = kit.mat("dark", kit.PALETTE["dark"], rough=0.55)

kit.box("sub", (3.2, 2.0, 0.28), (0, 0, 0.14), S, bevel=0.02)
# 沟槽比字线略大、略低，避免共面导致 z-fighting
kit.box("wl_trench", (2.96, 0.5, 0.2), (0, -0.52, 0.2), D, bevel=0.005)
kit.box("wl", (2.9, 0.32, 0.1), (0, -0.52, 0.24), G, bevel=0.012)

kit.box("sd_l", (0.34, 0.42, 0.1), (-0.62, -0.15, 0.33), N, bevel=0.01)
kit.box("sd_r", (0.34, 0.42, 0.1), (0.62, -0.15, 0.33), N, bevel=0.01)
kit.box("gate", (0.26, 0.5, 0.16), (0, -0.15, 0.37), G, bevel=0.01)

kit.cyl("plug", 0.075, 0.30, (0.62, -0.15, 0.53), M, verts=24)
kit.cyl("bl_plug", 0.07, 0.4, (-0.62, 0.4, 0.56), M, verts=24)

# 位线放到后面，避免在视觉上挡住晶体管和电容
kit.box("bl", (2.7, 0.16, 0.08), (0, 0.62, 0.72), M, bevel=0.012)

CX, CY, CZ = 0.62, -0.15, 0.98
R, T, Hh, DEP = 0.46, 0.075, 0.62, 0.62

kit.box("cap_l", (T, DEP, Hh), (CX - R + T / 2, CY, CZ + Hh / 2), G, bevel=0.012)
kit.box("cap_r", (T, DEP, Hh), (CX + R - T / 2, CY, CZ + Hh / 2), G, bevel=0.012)
kit.box("cap_b", (2 * R, T, Hh), (CX, CY + DEP / 2 - T / 2, CZ + Hh / 2), G, bevel=0.012)
kit.box("cap_f", (2 * R, DEP, T), (CX, CY, CZ + T / 2), G, bevel=0.012)

kit.cyl("cap_inner", 0.13, Hh * 0.78, (CX, CY, CZ + T + Hh * 0.39), M, verts=32)
kit.cyl("cap_contact", 0.06, 0.18, (CX, CY, CZ - 0.07), M, verts=20)

kit.ortho_camera(loc=(4.4, -6.0, 3.7), target=(0.35, -0.15, 0.72), scale=4.6)
kit.lights()
kit.render(OUT, 1400, 1000)

if len(argv) > 1 and argv[1].endswith(".glb"):
    bpy.ops.export_scene.gltf(filepath=argv[1], export_format="GLB",
                              export_apply=True, export_yup=True)
    print("EXPORTED", argv[1])
