# 半导体制造 · 可视化阅读

把 [chenwei810/Semiconductor_Manufacturing_Introduction](https://github.com/chenwei810/Semiconductor_Manufacturing_Introduction)
（25 章 × 5 语言，CC BY-NC-SA 4.0）里「静态文字最说不清」的部分，做成可以点、可以拖的页面。

**现在有 19 章**（按书的顺序）：00 全景、01 晶圆厂、02 晶体管、03 沙子到晶圆、04 光刻、
05 薄膜、06 刻蚀、07 离子注入、08 CMP、09 清洗、10 金属化、11 CMOS 流程、12 先进结构、
13 存储器、14 几纳米、15 测量与检测、16 良率、17 工艺控制、22 可靠性。
纯静态站点，无构建步骤、无外部依赖。

- 线上：<https://semi.pbeta.dev>　（备用：<https://semiconductor-visual-guide.vercel.app>）
- 源码：<https://github.com/atbeta/semiconductor-visual-guide>

推 `main` 即触发 Vercel 生产部署（Git 已连接）；也可手动 `vercel deploy --prod`。

## 怎么打开

```bash
cd ~/Projects/smi-viz
python3 -m http.server 4173
# → http://127.0.0.1:4173
```

也可以直接双击 `index.html`（全部用相对路径，`file://` 也能跑）。

## 结构

```
smi-viz/
├── index.html                          首页：封面 + 全文目录 + 阅读路径
├── chapters/
│   ├── 00-overview.html                八站旅程（可点）+ 晶圆能切多少颗（可算）
│   ├── 01-how-a-fab-works.html         厂房三层剖面 + 洁净度切换（微粒落片）
│   ├── 02-transistor.html              栅极电压滑块 → 沟道形成；NMOS/PMOS 切换
│   ├── 03-sand-to-wafer.html           纯度阶梯 + CZ 长晶动画（可播放/切 200·300 mm）
│   ├── 04-lithography.html             摄影↔光刻对照、7 步剖面动画、对准误差拖动、波长台阶
│   ├── 05-thin-films.html              四种沉积在同一个沟槽里的覆盖对比
│   ├── 06-etching.html                 各向异性滑块（侧蚀/CD）、终点检测曲线
│   ├── 07-ion-implantation.html        能量/剂量 → 深度分布，沟道效应与退火
│   ├── 08-cmp.html                     磨平前后对比滑块、Dishing / Erosion
│   ├── 09-cleaning.html                四类污染 × 四种药液（点选去除）
│   ├── 10-metallization.html           双大马士革 7 步动画 + 多层金属剖面
│   ├── 11-cmos-process-flow.html       FEOL 七步剖面 + 三段分工 + 工艺循环
│   ├── 13-memory.html                  DRAM 单元剖面 + 3D NAND 层数滑块 + HBM/TSV
│   ├── 14-process-nodes.html           节点 vs 实际 CPP/MMP，密度可切换
│   ├── 15-metrology.html               缺陷检测四步：扫描 → 比对 → 标记 → SEM 复检
│   ├── 16-yield-analysis.html          三段良率相乘、六种晶圆图形态、裸片大小 vs 良率
│   ├── 17-process-control.html         控制图四情景（规则判定）、Cpk 可调
│   ├── 12-advanced-transistors.html    平面/FinFET/GAA 切换，看栅极包覆 1/3/4 面
│   └── 22-reliability.html             浴缸曲线三段可点，老化筛选开关
├── assets/
│   ├── styles.css                      共享设计系统（深浅色、卡片、表格、翻页）
│   ├── site.js                         章节下拉、上一章/下一章、主题切换
│   ├── cover.png                       ComfyUI 生成的封面
│   ├── smi-ch04-hero.png               ComfyUI 生成的光刻章首图
│   └── figures/                        PR-ready 的图示（语言中性，只用数字编号）
│       ├── 02-mosfet.svg
│       ├── 04-litho-flow.svg
│       ├── 12-transistor-evolution.svg
│       └── 22-bathtub.svg
├── scripts/gen_image.py                调 103 ComfyUI 的最小脚本
├── content/                            上游仓库的浅克隆（只读，供查证原文）
└── preview*.png                        各页截图
```

## 设计上的几个决定

- **图 vs 生成图**：剖面、结构、曲线全部手写 SVG。扩散模型画不准几何，也写不了中文，而且上游规范要求「图上不放字、只用编号」——SVG 才满足。
- **生成图只做氛围**：封面和章首图来自 103 的 flux1-dev-fp8，只承担情绪，不承担信息。
- **图示语言中性**：`assets/figures/*.svg` 里没有文字，只有 ①②③ 编号，标题说明写在页面的 `<figcaption>` 里。这样同一张图能同时给 en / zh-TW / zh-CN / ja / ko 五个语种用，也能直接提 PR 回上游。
- **深链**：`?theme=light`、`?step=4`（光刻）、`?v=2.4&mode=pmos`（晶体管）、`?s=gaa`、`?z=2&burn=1`（可靠性）、`?d=200`（晶棒直径）、`?len=0.7`（长晶进度），方便截图和分享某个状态。
- **零依赖**：没有构建、没有框架。一个 `<script>`，几张 SVG。

## 已知取舍

- 目前只有简体中文；原书五语同构，但页面文案需要按语种写，不是自动翻译能解决的。
- 「晶圆位置」导航（前一站/这一站/下一站）还没做成组件，只在光刻章里以步骤条呈现。
- 术语表、搜索、阅读进度都还没做。

## 下一步

1. 按顺序继续：05 薄膜、06 刻蚀、07 离子注入、08 CMP……
2. 第 11 章（CMOS 全流程时间轴）、第 16 章（晶圆图交互，上游已有 `16-wafer-map-patterns.svg`）。
3. 把 `assets/figures/` 的 SVG 按上游 `images/README.md` 的清单格式整理，提 PR 回 `chenwei810`。
4. 五语种：页面文案目前只有简体中文，原书 en / zh-TW / ja / ko 同构，可以按语种复制页面。

---

内容改编自上述仓库，遵循 CC BY-NC-SA 4.0；本项目同样非商用、同协议共享。
