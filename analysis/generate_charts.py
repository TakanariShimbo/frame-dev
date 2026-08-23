# /// script
# dependencies = ["matplotlib"]
# ///
import csv, re
from collections import Counter
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
font_manager.fontManager.addfont(FONT)
plt.rcParams["font.family"] = font_manager.FontProperties(fname=FONT).get_name()

BG, PANEL, INK, MUTED, GOLD, GOLD_STRONG = "#070708", "#0d0d0f", "#f2efe7", "#8a867c", "#d8b672", "#e8cd93"
COLLECTED = "2026-08-01"  # 収集日（昨日/時刻のみ表記の基準）

rows = list(csv.DictReader(open("analysis/yamaframe_x_posts_2026-08-01.csv", encoding="utf-8-sig")))

def day_of(s):
    m = re.match(r"(\d+)月(\d+)日", s)
    if m: return f"{int(m.group(1))}/{int(m.group(2))}"
    if "昨日" in s: return "7/31"
    if re.match(r"\d+:\d+", s): return "8/1"
    return None

def style_ax(ax):
    ax.set_facecolor(BG)
    for s in ax.spines.values(): s.set_visible(False)
    ax.tick_params(colors=MUTED, labelsize=10, length=0)
    ax.yaxis.grid(False); ax.xaxis.grid(False)

def savefig(fig, name):
    fig.savefig(f"analysis/{name}", dpi=150, facecolor=BG, bbox_inches="tight")
    plt.close(fig)

# 1) 日別投稿数
days = [f"7/{d}" for d in range(23, 32)] + ["8/1"]
counts = Counter(d for r in rows if (d := day_of(r["posted_at"])))
vals = [counts.get(d, 0) for d in days]
fig, ax = plt.subplots(figsize=(9, 4.2), facecolor=BG)
bars = ax.bar(days, vals, color=GOLD, width=0.62, zorder=3)
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width()/2, v + 0.3, str(v), ha="center", color=INK, fontsize=10)
style_ax(ax); ax.set_yticks([])
ax.set_title("日別ポスト数（リリース 7/23 〜 収集 8/1 朝）", color=INK, fontsize=13, pad=14, loc="left")
savefig(fig, "chart_posts_per_day.png")

# 2) いいね数トップ10
top = sorted(rows, key=lambda r: -int(r["likes"] or 0))[:10][::-1]
labels = [f"{r['account_name'].split()[0] if r['account_name'] else r['handle']}｜{r['text'][:16]}…" for r in top]
likes = [int(r["likes"]) for r in top]
fig, ax = plt.subplots(figsize=(9, 5.2), facecolor=BG)
bars = ax.barh(labels, likes, color=[GOLD_STRONG if i == len(top)-1 else GOLD for i in range(len(top))], height=0.6, zorder=3)
for b, v in zip(bars, likes):
    ax.text(v + 12, b.get_y() + b.get_height()/2, f"{v:,}", va="center", color=INK, fontsize=10)
style_ax(ax); ax.set_xticks([])
ax.tick_params(axis="y", labelcolor=INK)
ax.set_xlim(0, max(likes) * 1.12)
ax.set_title("いいね数トップ10", color=INK, fontsize=13, pad=14, loc="left")
savefig(fig, "chart_top_likes.png")

# 3) クラスタ構成（full_report.md の分類に基づく）
clusters = [("要望・指摘", 3), ("ネタ・#間違った使い方", 7), ("用途の拡張発見", 8),
            ("感想・絶賛", 18), ("運営アナウンス", 27), ("作品・山行記録", 28)]
names, sizes = zip(*clusters)
fig, ax = plt.subplots(figsize=(9, 4.6), facecolor=BG)
bars = ax.barh(names, sizes, color=GOLD, height=0.6, zorder=3)
for b, v in zip(bars, sizes):
    ax.text(v + 0.4, b.get_y() + b.get_height()/2, f"{v}件", va="center", color=INK, fontsize=10)
style_ax(ax); ax.set_xticks([])
ax.tick_params(axis="y", labelcolor=INK)
ax.set_xlim(0, max(sizes) * 1.14)
ax.set_title("投稿クラスタの構成（94件）", color=INK, fontsize=13, pad=14, loc="left")
savefig(fig, "chart_clusters.png")

print("done")
