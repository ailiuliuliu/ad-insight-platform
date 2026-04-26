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

# 快手橙 + 深色配色
C_BG      = '#0f0f0f'      # 全局背景
C_ORANGE  = '#FF6200'      # 快手橙（主色）
C_ORANGE2 = '#FF8C42'      # 浅橙（副标题/描述）
C_ORANGE3 = '#3a1a00'      # 橙色区域填充
C_CARD    = '#1a1a1a'      # 卡片背景
C_CARD2   = '#242424'      # 卡片内层
C_LABEL   = '#FF6200'      # 左侧层标签
C_WHITE   = '#f0f0f0'
C_GRAY    = '#888888'
C_BLUE    = '#4a9eff'      # 外部信息源强调
C_PURPLE  = '#b57aff'      # 内部信息源强调

fig, ax = plt.subplots(figsize=(16, 13))
fig.patch.set_facecolor(C_BG)
ax.set_facecolor(C_BG)
ax.set_xlim(0, 16)
ax.set_ylim(0, 13)
ax.axis('off')

def box(x, y, w, h, fc, ec, r=0.3, lw=2.0, z=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={r}",
        facecolor=fc, edgecolor=ec, linewidth=lw, zorder=z))

def T(x, y, s, size=10, color=C_WHITE, bold=False, ha='center', va='center', z=5):
    ax.text(x, y, s, color=color, ha=ha, va=va, zorder=z,
            fontproperties=fp(size, bold))

def arr(x1, y1, x2, y2, color=C_ORANGE, lw=2.0, rad=0.0):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw,
                                connectionstyle=f'arc3,rad={rad}'), zorder=8)

# ─── 标题 ─────────────────────────────────────────────────────
T(8.0, 12.55, 'AI 驱动商业化洞察平台  /  系统架构', 14, C_ORANGE, bold=True)

# ─── 左侧层标签 ───────────────────────────────────────────────
for label, cy in [('输出 / 交互层', 10.3), ('AI 智能执行层', 7.15), ('信息层', 3.4)]:
    T(1.05, cy, label, 10.5, C_ORANGE, bold=True, ha='center')

# 分隔线
for y in [5.55, 8.75]:
    ax.plot([1.9, 15.6], [y, y], color='#333333', lw=1.2, zorder=3, linestyle='--')

# ══════════════════════════════════════════════════════════════
#  输出 / 交互层
# ══════════════════════════════════════════════════════════════
box(2.0, 8.9, 13.4, 3.6, '#1c0d00', C_ORANGE, r=0.4, lw=2.2)

# 网站卡片
box(2.4, 9.3, 5.8, 2.8, C_ORANGE3, C_ORANGE2, r=0.3, lw=1.5)
T(5.3, 11.75, '网站：商业化洞察平台', 11.5, C_ORANGE2, bold=True)
T(5.3, 11.2,  '最全资讯 & 洞察信息', 10, C_WHITE)
T(5.3, 10.75, '报告库查询', 10, C_WHITE)
# 小图标装饰
ax.plot([3.5, 3.5], [10.45, 11.95], color=C_ORANGE, lw=3, zorder=6)

# KIM 卡片
box(8.7, 9.3, 6.3, 2.8, C_ORANGE3, C_ORANGE2, r=0.3, lw=1.5)
T(11.85, 11.75, 'KIM 机器人：超级小李', 11.5, C_ORANGE2, bold=True)
T(11.85, 11.2,  '资讯洞察主动推送', 10, C_WHITE)
T(11.85, 10.75, '报告问答查询', 10, C_WHITE)
ax.plot([9.8, 9.8], [10.45, 11.95], color=C_ORANGE, lw=3, zorder=6)

# ══════════════════════════════════════════════════════════════
#  AI 智能执行层
# ══════════════════════════════════════════════════════════════
box(2.0, 5.7, 13.4, 2.85, '#1c0d00', C_ORANGE, r=0.4, lw=2.2)

# CodeFlicker 卡片
box(2.4, 6.05, 6.1, 2.15, '#2a1500', C_ORANGE, r=0.25, lw=1.5)
T(3.3, 7.75, 'CodeFlicker', 11, C_ORANGE, bold=True, ha='left')
T(5.45, 7.3,  '网站内容更新', 9.5, C_WHITE, ha='center')
T(5.45, 6.9,  '报告管理（标签、分类）', 9.5, C_WHITE, ha='center')
T(5.45, 6.5,  '知识沉淀与结构化', 9.5, C_WHITE, ha='center')

# Luigi 卡片
box(9.0, 6.05, 6.0, 2.15, '#2a1500', C_ORANGE, r=0.25, lw=1.5)
T(9.95, 7.75, 'Luigi  /  快手 AI 平台', 11, C_ORANGE, bold=True, ha='left')
T(12.0, 7.3,  '外部信息检索与评分', 9.5, C_WHITE, ha='center')
T(12.0, 6.9,  '意图识别与任务路由', 9.5, C_WHITE, ha='center')
T(12.0, 6.5,  '内部报告语义检索', 9.5, C_WHITE, ha='center')

# ══════════════════════════════════════════════════════════════
#  信息层
# ══════════════════════════════════════════════════════════════
box(2.0, 0.35, 13.4, 5.1, '#0a0a14', C_BLUE, r=0.4, lw=2.2)

# 外部信息源
box(2.4, 0.7, 6.1, 4.4, '#0d1829', C_BLUE, r=0.3, lw=1.5)
T(5.45, 4.75, '外部信息源', 11.5, C_BLUE, bold=True)
items_ext = [
    ('信息源 Tier 1－4 分层体系', C_WHITE),
    ('官方课程平台 · 公众号 · 行业媒体', '#93c5fd'),
    ('资讯评分排序规则', C_WHITE),
    ('信息核实验证规则', C_WHITE),
    ('时效性递进策略  7 / 14 / 30 天', '#93c5fd'),
]
for i, (txt, col) in enumerate(items_ext):
    T(5.45, 4.2 - i*0.67, txt, 9.5, col)

# 内部信息源
box(9.0, 0.7, 6.0, 4.4, '#160a2a', C_PURPLE, r=0.3, lw=1.5)
T(12.0, 4.75, '内部信息源', 11.5, C_PURPLE, bold=True)
items_int = [
    ('商业化行研报告库', C_WHITE),
    ('BGE-large-zh 向量索引', '#c4b5fd'),
    ('语义检索  ·  Top-N 召回', C_WHITE),
    ('标签分类体系', C_WHITE),
    ('商业化知识库', '#c4b5fd'),
]
for i, (txt, col) in enumerate(items_int):
    T(12.0, 4.2 - i*0.67, txt, 9.5, col)

# ══════════════════════════════════════════════════════════════
#  层间箭头
# ══════════════════════════════════════════════════════════════
# 信息层 → 执行层
arr(5.45, 5.1,  5.45, 5.7,  C_BLUE,   lw=2.2)
arr(12.0, 5.1,  12.0, 5.7,  C_PURPLE, lw=2.2)
# 执行层 → 交互层
arr(5.45, 8.2,  5.45, 8.9,  C_ORANGE, lw=2.2)
arr(12.0, 8.2,  12.0, 8.9,  C_ORANGE, lw=2.2)

# ══════════════════════════════════════════════════════════════
#  底部
# ══════════════════════════════════════════════════════════════
T(8.0, 0.12, 'Embedding: BGE-large-zh    |    AI 平台: Luigi (快手内部)    |    '
             'IDE: CodeFlicker    |    部署: GitHub Pages + KIM Robot',
  8, C_GRAY)

plt.tight_layout(pad=0.3)
plt.savefig('/Users/litianyu6/Documents/超级小李/ad-insight-arch2.png',
            dpi=180, bbox_inches='tight',
            facecolor=C_BG, edgecolor='none')
print('已保存：ad-insight-arch2.png')
