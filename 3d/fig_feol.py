"""第 11 章：FEOL 完成后的 CMOS 立体剖面。

做法：把一张 2D 截面「沿 Y 方向挤出」——每个矩形都是一个有厚度的块。
正面读起来是剖面图，斜着看又有体积，正好说明「每一层都嵌在前一层里」。

运行：
  /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup \
      --python 3d/fig_feol.py -- 输出.png [输出.glb]
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
OUT = argv[0] if argv else os.path.abspath("assets/3d/feol-stack.png")

kit.reset()
SUB = kit.mat("sub", (0.62, 0.68, 0.78, 1), rough=0.6)
PW = kit.mat("pwell", (0.42, 0.38, 0.62, 1), rough=0.55)
NW = kit.mat("nwell", (0.30, 0.45, 0.62, 1), rough=0.55)
STI = kit.mat("sti", (0.28, 0.62, 0.58, 1), rough=0.5)
SD = kit.mat("sd", kit.PALETTE["nplus"], rough=0.35)
N_LDD = kit.mat("ldd", (0.34, 0.78, 0.98, 1), rough=0.4)
GATE = kit.mat("gate", kit.PALETTE["gate"], rough=0.3, metal=0.2)
OX = kit.mat("oxide", kit.PALETTE["oxide"], rough=0.2)
SP = kit.mat("spacer", (0.78, 0.80, 0.86, 1), rough=0.45)
SIL = kit.mat("silicide", (0.72, 0.76, 0.84, 1), rough=0.35, metal=0.65)

Y0, Y1 = -0.26, 0.26
DEPTH = Y1 - Y0

def slab(name, x0, x1, z0, z1, m, y0=Y0, y1=Y1, bevel=0.006, step=0):
    """step>0 时给对象名加 stN_ 前缀，网页端按步骤逐个显示。"""
    full = f"st{step}_{name}" if step else name
    kit.box(full, (x1 - x0, y1 - y0, z1 - z0),
            ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2), m, bevel=bevel)

# ---------- 衬底：P 阱（左）/ N 阱（右），中间夹 STI ----------
H = 0.42
TOP = 0.16          # 顶层（含源漏）厚度

SD_RANGES = [(-1.05, -0.62), (-0.40, -0.18), (0.18, 0.40), (0.62, 1.05)]

# 阱的下半部（整块）
slab("pwell", -1.30, -0.06, 0, H - TOP, PW)
slab("nwell", 0.06, 1.30, 0, H - TOP, NW)

# 顶层：按源漏位置切成几段，中间留缺口给源漏
def top_segments(x0, x1, rngs, depth, mat):
    cur = x0
    for a, b in rngs:
        if a > cur:
            slab("top", cur, a, H - TOP, H, mat)
        cur = max(cur, b)
    if cur < x1:
        slab("top", cur, x1, H - TOP, H, mat)

top_segments(-1.30, -0.06, [(a, b) for a, b in SD_RANGES if b <= -0.06], TOP, PW)
top_segments(0.06, 1.30, [(a, b) for a, b in SD_RANGES if a >= 0.06], TOP, NW)

# 源漏：正好填进缺口，顶面与衬底齐平
for name, (x0, x1) in zip(["sd1", "sd2", "sd3", "sd4"], SD_RANGES):
    slab(name, x0, x1, H - TOP + 0.001, H, SD, y0=Y0 + 0.004, y1=Y1 - 0.004, bevel=0.003, step=6)

# LDD：栅极两侧的浅掺杂延伸（第 5 步）
for xc in (-0.55, 0.55):
    slab("ldd_l", xc - 0.30, xc - 0.17, H - 0.03, H, N_LDD, y0=Y0 + 0.006, y1=Y1 - 0.006, bevel=0.002, step=5)
    slab("ldd_r", xc + 0.17, xc + 0.30, H - 0.03, H, N_LDD, y0=Y0 + 0.006, y1=Y1 - 0.006, bevel=0.002, step=5)

# STI：略高于表面，表示浅浅的沟槽隔离
slab("sti_mid", -0.08, 0.08, 0, H + 0.02, STI, step=1)
slab("sti_l", -1.42, -1.30, 0, H + 0.02, STI, step=1)
slab("sti_r", 1.30, 1.42, 0, H + 0.02, STI, step=1)

# ---------- 栅极堆栈 ----------
for xc in (-0.55, 0.55):
    slab("gox", xc - 0.18, xc + 0.18, H + 0.012, H + 0.03, OX, bevel=0.002, step=2)
    slab("gate", xc - 0.17, xc + 0.17, H + 0.03, H + 0.24, GATE, step=3)
    # 侧墙（两侧的小三角块用薄板代替）
    slab("sp_l", xc - 0.20, xc - 0.17, H + 0.03, H + 0.17, SP, bevel=0.002, step=4)
    slab("sp_r", xc + 0.17, xc + 0.20, H + 0.03, H + 0.17, SP, bevel=0.002, step=4)
    # 金属硅化物（栅极顶面）
    slab("sil", xc - 0.16, xc + 0.16, H + 0.24, H + 0.27, SIL, bevel=0.003, step=7)

# 源漏顶部直接做金属化（不再叠一块硅化物，避免共面闪烁）

kit.ortho_camera(loc=(4.2, -6.6, 4.0), target=(0, 0, 0.30), scale=3.5)
kit.lights()
kit.render(OUT, 1600, 900)

if len(argv) > 1 and argv[1].endswith(".glb"):
    bpy.ops.export_scene.gltf(filepath=argv[1], export_format="GLB",
                              export_apply=True, export_yup=True)
    print("EXPORTED", argv[1])
