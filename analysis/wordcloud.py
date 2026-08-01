# /// script
# dependencies = ["wordcloud", "janome", "numpy", "pillow"]
# ///
import csv, re, random
import numpy as np
from janome.tokenizer import Tokenizer
from wordcloud import WordCloud
from PIL import Image, ImageDraw

CSV = "/home/ai-workshop/work/frame-dev/analysis/yamaframe_x_posts_2026-08-01.csv"
OUT = "/home/ai-workshop/work/frame-dev/analysis"
FONT = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"

texts = []
with open(CSV, encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        t = row["text"]
        t = re.sub(r"https?://\S+|pic\.x\.com/\S+|x\.com/\S+|yamaframe\.com|#\S+|@\w+", " ", t)
        texts.append(t)

STOP = set("""こと よう これ それ ところ ため 感じ 自分 今日 昨日 明日 皆様 みなさん たち さん くん ちゃん 僕 私 あと ここ そこ どこ もの やつ 的 中 後 前 度 回 日 月 年 時 分 版 枚 座 山 写真 アプリ フォト 投稿 使い方 一枚 ヤマ フレーム ヤマフレーム""".split())

tok = Tokenizer()
freq = {}
for t in texts:
    for token in tok.tokenize(t):
        pos = token.part_of_speech.split(",")
        w = token.base_form if token.base_form != "*" else token.surface
        if pos[0] == "名詞" and pos[1] in ("一般", "固有名詞") and len(w) > 1 and w not in STOP and not re.fullmatch(r"[0-9a-zA-Z_]+|[ぁ-ん]+", w):
            freq[w] = freq.get(w, 0) + 1

freq = {w: c for w, c in freq.items() if c >= 1}
print(sorted(freq.items(), key=lambda x: -x[1])[:20])

GOLDS = ["#d8b672", "#e8cd93", "#f2efe7", "#b3945c", "#c9a86a", "#a08050"]
def color_fn(word, font_size, position, orientation, random_state=None, **kw):
    r = random.Random(hash(word))
    return GOLDS[0] if font_size > 80 else r.choice(GOLDS)

common = dict(font_path=FONT, background_color="#070708", color_func=color_fn,
              prefer_horizontal=0.95, max_words=120, margin=6, random_state=42)

# 1) normal
WordCloud(width=1600, height=900, **common).generate_from_frequencies(freq)\
    .to_file(f"{OUT}/wordcloud_normal.png")

# 2) mountain mask
W, H = 1600, 1000
img = Image.new("L", (W, H), 255)
d = ImageDraw.Draw(img)
d.polygon([(0, H), (0, H*0.72), (W*0.18, H*0.38), (W*0.30, H*0.55), (W*0.52, H*0.10),
           (W*0.68, H*0.42), (W*0.80, H*0.30), (W, H*0.68), (W, H)], fill=0)
mask = np.array(img)
WordCloud(mask=mask, **common).generate_from_frequencies(freq)\
    .to_file(f"{OUT}/wordcloud_mountain.png")
print("done")
