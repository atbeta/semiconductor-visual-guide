"""兼容层：把老的 3d/*.py 里的 kit.* 转发到 fabkit。

引擎默认 Cycles（可用 FAB_ENGINE=EEVEE 临时切回），采样数用 FAB_SAMPLES 调。
"""
import os
import sys

FABKIT = os.path.expanduser("~/Projects/fabkit")
if FABKIT not in sys.path:
    sys.path.insert(0, FABKIT)

import fabkit as _fk  # noqa: E402
from fabkit.core import (  # noqa: E402,F401
    srgb, mat, box, cyl, tube, ortho_camera, lights, world,
)

ENGINE = os.environ.get("FAB_ENGINE", "CYCLES")
SAMPLES = int(os.environ.get("FAB_SAMPLES", "48"))

# 老脚本用 kit.PALETTE[...]，这里保持同样的键和 sRGB 取值
PALETTE = {
    "substrate": (0.62, 0.66, 0.76, 1),
    "silicon":   (0.42, 0.55, 0.72, 1),
    "nplus":     (0.22, 0.74, 0.97, 1),
    "gate":      (0.96, 0.62, 0.04, 1),
    "oxide":     (0.13, 0.83, 0.93, 1),
    "sheet":     (0.38, 0.65, 0.98, 1),
    "metal":     (0.78, 0.80, 0.85, 1),
    "dark":      (0.20, 0.23, 0.28, 1),
}


def reset():
    return _fk.reset(theme="schematic", engine=ENGINE, samples=SAMPLES)


def render(path, w=1600, h=1000):
    return _fk.render(path, w, h)


def ground_shadow(size=20):
    return _fk.ground_shadow(size)
