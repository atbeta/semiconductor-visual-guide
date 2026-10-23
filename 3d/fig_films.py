"""第 5 章：同一道沟槽上，CVD / PVD / ALD 的覆盖差异。

三个面板并排，沟槽尺寸相同，只有薄膜厚度分布不同：
  PVD  顶面厚、侧壁薄、底部薄（方向性差）
  CVD  处处接近等厚（保形）
  ALD  极薄且完全等厚（一层一层长）

运行：
  /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup \
      --python 3d/fig_films.py -- 输出.png
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
OUT = argv[0] if argv else os.path.abspath("assets/3d/films.png")

kit.reset()
S = kit.mat("substrate", kit.PALETTE["substrate"], rough=0.55)
F = kit.mat("film", kit.PALETTE["oxide"], rough=0.3)
F2 = kit.mat("film2", kit.PALETTE["nplus"], rough=0.3)

# 沟槽尺寸
TW, TD, TH = 1.05, 0.9, 0.62      # 宽 / 深（Y）/ 高
BASE_W, BASE_D = 2.5, 1.2


def panel(x0, thickness, color_mat):
    """在 x0 处建一个带沟槽的基底，并按 (top, side, bottom) 厚度铺膜。"""
    top_t, side_t, bot_t = thickness

    # 基底：左块 + 右块 + 槽底
    left_w = (BASE_W - TW) / 2
    kit.box("base_l", (left_w, BASE_D, TH + 0.28),
            (x0 - TW / 2 - left_w / 2, 0, (TH + 0.28) / 2), S, bevel=0.02)
    kit.box("base_r", (left_w, BASE_D, TH + 0.28),
            (x0 + TW / 2 + left_w / 2, 0, (TH + 0.28) / 2), S, bevel=0.02)
    kit.box("base_b", (TW, BASE_D, 0.28), (x0, 0, 0.14), S, bevel=0.02)

    z_top = TH + 0.28          # 基底顶面
    z_bot = 0.28               # 槽底面

    # 顶面膜（两侧台面）
    if top_t > 0:
        kit.box("f_top_l", (left_w, BASE_D, top_t),
                (x0 - TW / 2 - left_w / 2, 0, z_top + top_t / 2), color_mat, bevel=0.008)
        kit.box("f_top_r", (left_w, BASE_D, top_t),
                (x0 + TW / 2 + left_w / 2, 0, z_top + top_t / 2), color_mat, bevel=0.008)

    # 侧壁膜
    if side_t > 0:
        h = TH
        kit.box("f_sw_l", (side_t, BASE_D, h),
                (x0 - TW / 2 + side_t / 2, 0, z_bot + h / 2), color_mat, bevel=0.005)
        kit.box("f_sw_r", (side_t, BASE_D, h),
                (x0 + TW / 2 - side_t / 2, 0, z_bot + h / 2), color_mat, bevel=0.005)

    # 底部膜
    if bot_t > 0:
        kit.box("f_bt", (TW, BASE_D, bot_t),
                (x0, 0, z_bot + bot_t / 2), color_mat, bevel=0.005)


# 三个面板：PVD 方向性强 → 顶厚、侧薄、底薄
panel(-3.1, (0.16, 0.035, 0.05), F)
panel(0.0,  (0.10, 0.095, 0.09), F)
panel(3.1,  (0.045, 0.042, 0.04), F)

kit.ortho_camera(loc=(2.2, -13.0, 8.2), target=(0, 0, 0.45), scale=10.6)
kit.lights()
kit.render(OUT, 1800, 720)
