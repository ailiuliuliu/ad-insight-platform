#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib import font_manager

FONT = '/System/Library/Fonts/STHeiti Medium.ttc'
def fp(size, bold=False):
    return font_manager.FontProperties(fname=FONT, size=size,
                                       weight='bold' if bold else 'normal')

fig, ax = plt.subplots(figsize=(22, 11))
fig.patch.set_facecolor('#0d1117')
ax.set_facecolor('#0d1117')
ax.set_xlim(0, 22)
ax.set_ylim(0, 11)
ax.axis('off')

def box(x, y, w, h, fc, ec, r=0.3, lw=1.8, alpha=1.0, z=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={r}",
        facecolor=fc, edgecolor=ec, linewidth=lw, alpha=alpha, zorder=z))

def T(x, y, s, size=9, color='white', bold=False, ha='center', va='center', z=5):
    ax.text(x, y, s, color=color, ha=ha, va=va, zorder=z,
            fontproperties=fp(size, bold))

def arr(x1, y1, x2, y2, color, lw=1.6, rad=0.0):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw,
                                connectionstyle=f'arc3,rad={rad}'), zorder=7)

# ── 标题 ──────────────────────────────────────────────────────
T(11.0, 10.6, 'AI 驱动商业化洞察平台  /  系统架构', 13, '#e2e8f0', bold=True)

# ══════════════════════════════════════════════════════════════
#  区域背景
# ══════════════════════════════════════════════════════════════
box(0.3,  6.5, 6.4, 3.9, '#091929', '#4a9eff', r=0.45, lw=2)   # 外部信息源
T(3.5, 10.15, '外部信息源', 10, '#4a9eff', bold=True)

box(7.3,  6.5, 6.4, 3.9, '#130a26', '#a855f7', r=0.45, lw=2)   # 内部知识库
T(10.5, 10.15, '内部知识库', 10, '#a855f7', bold=True)

box(0.3,  0.7, 6.4, 5.5, '#011a0a', '#22c55e', r=0.45, lw=2)   # Agent 1
T(3.5,  5.95, 'Agent 1  /  定时播报', 10, '#22c55e', bold=True)

box(7.3,  0.7, 6.4, 5.5, '#1a0e00', '#f59e0b', r=0.45, lw=2)   # Agent 2
T(10.5, 5.95, 'Agent 2  /  用户问答', 10, '#f59e0b', bold=True)

box(14.4, 0.7, 7.2, 9.7, '#1a0505', '#ef4444', r=0.45, lw=2)   # 输出层
T(18.0, 10.15, '输出层', 10, '#ef4444', bold=True)

# ══════════════════════════════════════════════════════════════
#  外部信息源节点
# ══════════════════════════════════════════════════════════════
for title, sub, cy in [
    ('Tier 1  官方课程平台', '巨量学 · 腾讯营销学堂 · 蒲公英帮助中心', 9.45),
    ('Tier 2  官方公众号',   '巨量引擎营销观察 · 巨量千川 · 腾讯广告',  8.4),
    ('Tier 4  行业媒体',     '36氪 · 虎嗅 · 钛媒体 · 界面新闻 · 21财经', 7.35),
]:
    box(0.65, cy-0.42, 5.75, 0.82, '#0d2b4a', '#4a9eff', r=0.2)
    T(3.52, cy,      title, 8.5, '#7dd3fc')
    T(3.52, cy-0.3,  sub,   7.5, '#93c5fd')

# ══════════════════════════════════════════════════════════════
#  内部知识库节点
# ══════════════════════════════════════════════════════════════
for title, sub, cy in [
    ('内部行研报告',             '飞书文档  /  共享盘',             9.45),
    ('BGE-large-zh  Embedding', '中文语义向量化',                   8.4),
    ('向量数据库',               '语义检索索引  ·  Top-N 召回',    7.35),
]:
    box(7.65, cy-0.42, 5.75, 0.82, '#221050', '#a855f7', r=0.2)
    T(10.52, cy,      title, 8.5, '#c4b5fd')
    T(10.52, cy-0.3,  sub,   7.5, '#ddd6fe')

arr(10.52, 9.03, 10.52, 8.98, '#a855f7')
arr(10.52, 7.98, 10.52, 7.93, '#a855f7')

# ══════════════════════════════════════════════════════════════
#  Agent 1 步骤
# ══════════════════════════════════════════════════════════════
a1 = [
    ('定时触发',       '每周一 / 周四  11:00',                   5.25),
    ('分层递进搜集',   'Tier1 → Tier2 → Tier4 → Tier5 兜底',    4.2),
    ('fetch_web 验证', '关键数据原文核实  ·  剔除过期信息',      3.15),
    ('生成结构化播报', '今日洞察 x3  ·  竞对动态  ·  行业赛道', 2.1),
]
for title, sub, cy in a1:
    box(0.65, cy-0.42, 5.75, 0.82, '#052e16', '#22c55e', r=0.2)
    T(3.52, cy,      title, 8.5, '#86efac')
    T(3.52, cy-0.3,  sub,   7.5, '#bbf7d0')

for i in range(len(a1)-1):
    arr(3.52, a1[i][2]-0.42, 3.52, a1[i+1][2]+0.40, '#22c55e')

# ══════════════════════════════════════════════════════════════
#  Agent 2 步骤
# ══════════════════════════════════════════════════════════════
a2 = [
    ('用户提问',           'KIM 群  @机器人',                       5.25),
    ('意图识别',           '洞察类  /  调研类  /  报告检索类',      4.2),
    ('外部信息搜集',       'Tier1→2→4→5  ·  时效性递进 7/14/30天', 3.15),
    ('触发内部报告库检索', '语义匹配 → 原文标题超链接 + 摘要',     2.1),
]
for title, sub, cy in a2:
    box(7.65, cy-0.42, 5.75, 0.82, '#291900', '#f59e0b', r=0.2)
    T(10.52, cy,      title, 8.5, '#fcd34d')
    T(10.52, cy-0.3,  sub,   7.5, '#fde68a')

for i in range(len(a2)-1):
    arr(10.52, a2[i][2]-0.42, 10.52, a2[i+1][2]+0.40, '#f59e0b')

# ══════════════════════════════════════════════════════════════
#  输出层节点
# ══════════════════════════════════════════════════════════════
out = [
    ('KIM 机器人',       'KIM Robot Webhook  ·  统一发送 API',           9.15, '#ef4444', '#3d0a0a'),
    ('商业化洞察平台',   'GitHub Pages  ·  ailiuliuliu.github.io',        7.7,  '#ef4444', '#3d0a0a'),
    ('开机 / 唤醒补推',  '.last_push_date 防重入  ·  漏推自动补发',      6.25, '#f59e0b', '#291900'),
    ('DeepSeek V3 摘要', '报告摘要提炼  ·  核心结论  ·  快手启示',       4.8,  '#a855f7', '#221050'),
    ('防幻觉约束',       '标题原样输出  ·  禁止改写  ·  无摘要则提示',   3.35, '#4a9eff', '#0d2b4a'),
]
for title, sub, cy, ec, fc in out:
    box(14.75, cy-0.55, 6.5, 1.05, fc, ec, r=0.2)
    T(18.0, cy,      title, 9,   'white', bold=True)
    T(18.0, cy-0.37, sub,   7.5, '#d1d5db')

# ══════════════════════════════════════════════════════════════
#  连接箭头
# ══════════════════════════════════════════════════════════════
# 信息源 → Agent1
arr(3.52, 6.5, 3.52, 6.2, '#4a9eff')
# 信息源 → Agent2
ax.annotate('', xy=(10.52, 6.2), xytext=(6.4, 8.4),
            arrowprops=dict(arrowstyle='->', color='#4a9eff', lw=1.6,
                            connectionstyle='arc3,rad=-0.15'), zorder=7)
# 向量库 → Agent2 检索
ax.annotate('', xy=(13.4, 2.1), xytext=(13.4, 6.93),
            arrowprops=dict(arrowstyle='->', color='#a855f7', lw=1.6,
                            connectionstyle='arc3,rad=0.0'), zorder=7)

# Agent1 → KIM
ax.annotate('', xy=(14.75, 8.9), xytext=(6.7, 3.5),
            arrowprops=dict(arrowstyle='->', color='#22c55e', lw=1.5,
                            connectionstyle='arc3,rad=-0.12'), zorder=7)
# Agent1 → 洞察平台
ax.annotate('', xy=(14.75, 7.5), xytext=(6.7, 2.5),
            arrowprops=dict(arrowstyle='->', color='#22c55e', lw=1.5,
                            connectionstyle='arc3,rad=0.0'), zorder=7)
# Agent2 → KIM
ax.annotate('', xy=(14.75, 9.3), xytext=(13.7, 4.5),
            arrowprops=dict(arrowstyle='->', color='#f59e0b', lw=1.5,
                            connectionstyle='arc3,rad=0.2'), zorder=7)
# Agent2 → DeepSeek
arr(13.7, 2.1, 14.75, 4.8, '#a855f7')

# 补推 → KIM
arr(18.0, 6.25-0.55, 18.0, 7.7+0.5, '#f59e0b')

# ══════════════════════════════════════════════════════════════
#  底部图例
# ══════════════════════════════════════════════════════════════
box(0.3, 0.05, 21.4, 0.55, '#111827', '#374151', r=0.25)
T(11.0, 0.33,
  'Embedding: BGE-large-zh    |    摘要模型: DeepSeek V3    |    '
  '防重推: .last_push_date    |    部署: GitHub Pages + KIM Robot',
  7.8, '#9ca3af')

plt.savefig('/Users/litianyu6/Documents/超级小李/ad-insight-arch.png',
            dpi=180, bbox_inches='tight',
            facecolor='#0d1117', edgecolor='none')
print('已保存：/Users/litianyu6/Documents/超级小李/ad-insight-arch.png')
