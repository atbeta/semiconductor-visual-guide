/* 半导体制造 · 可视化 —— 共享导航与主题 */
(function () {
  const CHAPTERS = [
    { n: '00', t: '半导体制造全景', f: '00-overview.html' },
    { n: '01', t: '晶圆厂如何运行', f: '01-how-a-fab-works.html' },
    { n: '02', t: '从物理到晶体管', f: '02-transistor.html' },
    { n: '03', t: '从沙子到晶圆', f: '03-sand-to-wafer.html' },
    { n: '04', t: '光刻', f: '04-lithography.html' },
    { n: '05', t: '薄膜', f: '05-thin-films.html' },
    { n: '06', t: '刻蚀', f: '06-etching.html' },
    { n: '07', t: '离子注入与热处理', f: '07-ion-implantation.html' },
    { n: '08', t: 'CMP', f: '08-cmp.html' },
    { n: '09', t: '清洗与污染控制', f: '09-cleaning.html' },
    { n: '10', t: '金属化', f: '10-metallization.html' },
    { n: '11', t: '完整的 CMOS 流程', f: null },
    { n: '12', t: '先进晶体管结构', f: '12-advanced-transistors.html' },
    { n: '13', t: '存储器工艺', f: null },
    { n: '14', t: '「几纳米」是什么意思', f: null },
    { n: '15', t: '测量与检测', f: null },
    { n: '16', t: '良率与失效分析', f: null },
    { n: '17', t: '工艺控制', f: null },
    { n: '18', t: '异常处理与工程变更', f: null },
    { n: '19', t: '晶圆测试', f: null },
    { n: '20', t: '封装', f: null },
    { n: '21', t: '先进封装', f: null },
    { n: '22', t: '最终测试与可靠性', f: '22-reliability.html' },
    { n: '23', t: '工厂如何被系统管理', f: null },
    { n: '24', t: '工艺如何影响固件', f: null }
  ];
  window.SMI_CHAPTERS = CHAPTERS;

  const inChapters = location.pathname.includes('/chapters/');
  const base = inChapters ? '' : 'chapters/';
  const here = location.pathname.split('/').pop() || 'index.html';

  /* 主题（head 里的内联脚本已先设好，这里只兜底） */
  if (!document.documentElement.dataset.theme) {
    const saved = localStorage.getItem('smi-theme');
    document.documentElement.dataset.theme = saved ||
      (matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark');
  }

  const btn = document.getElementById('themeBtn');
  if (btn) btn.addEventListener('click', () => {
    const next = document.documentElement.dataset.theme === 'light' ? 'dark' : 'light';
    document.documentElement.dataset.theme = next;
    localStorage.setItem('smi-theme', next);
  });

  /* 章节下拉 */
  const sel = document.getElementById('chapJump');
  if (sel) {
    const done = CHAPTERS.filter(c => c.f);
    sel.innerHTML = done.map(c =>
      `<option value="${base}${c.f}">${c.n} · ${c.t}</option>`
    ).join('');
    const cur = done.find(c => c.f === here);
    if (cur) sel.value = base + cur.f;
    sel.addEventListener('change', () => { if (sel.value) location.href = sel.value; });
  }

  /* 上一章 / 下一章 */
  const done = CHAPTERS.filter(c => c.f);
  const i = done.findIndex(c => c.f === here);
  const prev = i > 0 ? done[i - 1] : null;
  const next = i >= 0 && i < done.length - 1 ? done[i + 1] : null;
  const pager = document.querySelector('.pager');
  if (pager) {
    if (prev && pager.querySelector('.prev')) {
      pager.querySelector('.prev').href = base + prev.f;
      pager.querySelector('.prev').textContent = `← ${prev.n} ${prev.t}`;
    }
    if (next && pager.querySelector('.next')) {
      pager.querySelector('.next').href = base + next.f;
      pager.querySelector('.next').textContent = `${next.n} ${next.t} →`;
    }
  }
})();
