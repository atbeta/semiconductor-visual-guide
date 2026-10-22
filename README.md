# 半导体制造 · 可视化阅读

把 [chenwei810/Semiconductor_Manufacturing_Introduction](https://github.com/chenwei810/Semiconductor_Manufacturing_Introduction)
（25 章 × 5 语言，CC BY-NC-SA 4.0）里「静态文字最说不清」的部分，做成可以点、可以拖的页面。

**现在有 4 章**：02 晶体管、04 光刻、12 先进结构、22 可靠性。纯静态站点，无构建步骤、无外部依赖。

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
│   ├── 02-transistor.html              栅极电压滑块 → 沟道形成；NMOS/PMOS 切换
│   ├── 04-lithography.html             摄影↔光刻对照、7 步剖面动画、对准误差拖动、波长台阶
│   ├── 12-advanced-transistors.html    平面/FinFET/GAA 切换，看栅极包覆 1/3/4 面
│   └── 22-reliability.html             浴缸曲线三段可点，老化筛选开关
├── assets/
│   ├── styles.css                      共享设计系统（深浅色、卡片、表格、翻页）
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
- **深链**：`?theme=light`、`?step=4`（光刻）、`?v=2.4&mode=pmos`（晶体管）、`?s=gaa`、`?z=2&burn=1`（可靠性），方便截图和分享某个状态。
- **零依赖**：没有构建、没有框架。一个 `<script>`，几张 SVG。

## 已知取舍

- 目前只有简体中文；原书五语同构，但页面文案需要按语种写，不是自动翻译能解决的。
- 「晶圆位置」导航（前一站/这一站/下一站）还没做成组件，只在光刻章里以步骤条呈现。
- 术语表、搜索、阅读进度都还没做。

## 下一步

1. 把 25 章铺满（组件已经稳定，每章 0.5–1 天）。
2. 补第 03 章「从沙子到晶圆」（CZ 长晶剖面）、第 11 章（CMOS 全流程时间轴）、第 16 章（晶圆图 → 用上游现成的 `16-wafer-map-patterns.svg` 做交互）。
3. 把这 4 张 SVG 按上游 `images/README.md` 的清单格式整理，提 PR。
4. 部署到 101（Traefik + cloudflared），加自定义域名。

---

内容改编自上述仓库，遵循 CC BY-NC-SA 4.0；本项目同样非商用、同协议共享。
