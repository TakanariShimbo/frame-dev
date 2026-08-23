# /// script
# dependencies = ["matplotlib", "numpy"]
# ///
import csv, re
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
font_manager.fontManager.addfont(FONT)
plt.rcParams["font.family"] = font_manager.FontProperties(fname=FONT).get_name()

BG, INK, MUTED = "#070708", "#f2efe7", "#8a867c"
PALETTE = {
    "作品・山行記録":       "#d8b672",
    "運営アナウンス":       "#8fa3b8",
    "感想・絶賛":           "#a3b18a",
    "用途の拡張発見":       "#c98a6a",
    "ネタ・#間違った使い方": "#b39ddb",
    "要望・指摘":           "#f2efe7",
}

rows = list(csv.DictReader(open("analysis/yamaframe_x_posts_2026-08-01.csv", encoding="utf-8-sig")))

def classify(r):
    t, h = r["text"], r["handle"]
    if re.search(r"間違った使い方|グラビア|山頂超え|大喜利|猫動画", t): return "ネタ・#間違った使い方"
    if re.search(r"線は消えない|桜島|改行できると嬉しい", t): return "要望・指摘"
    if re.search(r"キャンプ|温泉|ツーリング|海沿い|猫写真|動物写真|日常でも|YAMAPのトップ|カバー写真|Exif", t): return "用途の拡張発見"
    if h == "@r_outdoor_photo" and re.search(r"ユーザー数|リリース|アップデート|更新しました|開催|協賛|検討中|皆様|認知|フック|サイクル", t): return "運営アナウンス"
    if re.search(r"楽しい|たのしい|神アプリ|オシャレ|おしゃれ|すごい|スゴ|凄い|感動|最高|いいぞ|良いわ|めっちゃ|なぜ無料|流行", t): return "感想・絶賛"
    return "作品・山行記録"

labels = [classify(r) for r in rows]

# クラスタごとに中心を置き、黄金角スパイラルで点を配置（サイズ＝いいね数）
CENTERS = {
    "作品・山行記録":       (0.0, 0.0),
    "運営アナウンス":       (3.4, 1.6),
    "感想・絶賛":           (-3.0, 2.2),
    "用途の拡張発見":       (-3.2, -2.2),
    "ネタ・#間違った使い方": (3.6, -2.3),
    "要望・指摘":           (0.6, -4.1),
}
GA = np.pi * (3 - np.sqrt(5))
counters = {k: 0 for k in CENTERS}
xy = np.zeros((len(rows), 2))
for i, l in enumerate(labels):
    k = counters[l]; counters[l] += 1
    r_ = 0.34 * np.sqrt(k + 0.6)
    th = k * GA
    cx, cy = CENTERS[l]
    xy[i] = (cx + r_ * np.cos(th), cy + r_ * np.sin(th))

fig, ax = plt.subplots(figsize=(10, 7.5), facecolor=BG)
ax.set_facecolor(BG)
for s in ax.spines.values(): s.set_visible(False)
ax.set_xticks([]); ax.set_yticks([])
for name, color in PALETTE.items():
    idx = [i for i, l in enumerate(labels) if l == name]
    sizes = [60 + min(int(rows[i]["likes"] or 0), 300) for i in idx]
    ax.scatter(xy[idx, 0], xy[idx, 1], s=sizes, c=color, label=None,
               alpha=0.85, edgecolors=BG, linewidths=1.5, zorder=3)
for name, (cx, cy) in CENTERS.items():
    n = sum(1 for l in labels if l == name)
    rad = 0.34 * np.sqrt(n + 0.6) + 0.55
    ax.annotate(f"{name}（{sum(1 for l in labels if l == name)}件）", (cx, cy - rad), ha="center", va="top", color=MUTED, fontsize=10.5)
for i, r in enumerate(rows):
    if int(r["likes"] or 0) >= 80:
        ax.annotate(r["text"][:12] + "…", (xy[i, 0], xy[i, 1]), xytext=(0, 12),
                    textcoords="offset points", ha="center", color=INK, fontsize=9)
ax.set_title("投稿内容のクラスタマップ（94件 / 点の大きさ＝いいね数）",
             color=INK, fontsize=13, pad=14, loc="left")
ax.margins(0.10)
ax.set_ylim(bottom=xy[:,1].min() - 1.6)
fig.savefig("analysis/chart_cluster_map.png", dpi=150, facecolor=BG, bbox_inches="tight")
print("done")
