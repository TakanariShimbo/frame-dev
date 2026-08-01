# featured.json（長岡花火）の生成。解説の文字数を山の解説と同じ枠に収める:
#   ja long 60〜80字 / ja short 25〜50字 / en long 140〜270字 / en short 45〜160字
# 協賛社名は aliases に入れて検索ヒットさせる。
# 使い方: python3 scripts/generate-featured.py && node scripts/check-featured.mjs
import json, re

LAT, LON = 37.4463, 138.8367
BASE = dict(latitude=LAT, longitude=LON, elevation_m=2026, prefecture="長岡花火")
URL = "https://nagaokamatsuri.com/"

# (日, 時刻, 種別, タイトル, 協賛)
P2 = [
 ("2","19:25","ナイアガラ超大型スターマイン","カノン～この先に続く道(ミライ)に向かって～","オンヨネ＆エヌ・シィ・ティ"),
 ("2","19:25","ベスビアス超大型スターマイン","純金箔24K 黄金の輝き","トーア"),
 ("2","19:25","超大型スーパーベスビアス","ガラスが拓く未来のとびら","ミクロ技術研究所長岡事業所"),
 ("2","19:25","ベスビアス大スターマイン","大河の恵み～水が生む紙の物語","北越コーポレーション・北越グループ"),
 ("2","19:25","10号72発","誰かのために！72年の感謝報恩","ソリマチテックグループ"),
 ("2","19:25","超大型スーパーベスビアス","米百俵の心","中越興業グループ"),
 ("2","19:25","ベスビアス超大型スターマイン","長岡から世界へ、希望の花束","イートラスト"),
 ("2","19:45","ベスビアス超大型スターマイン","ともに歩んだ80年、明日へ届ける感謝の響き","越後製菓"),
 ("2","19:45","超大型スーパーベスビアス","真夏のイルミネーション","ユニオンツール"),
 ("2","19:45","ベスビアス大スターマイン","人が想い描く未来、その先へ","クレスコ"),
 ("2","19:45","ベスビアス超大型スターマイン","心ひとつに","TeNYテレビ新潟"),
 ("2","19:45","10号20発・20号3発","未来へ～平和を願って～","リバーサイド千秋・アピタ長岡店・JTB"),
 ("2","20:00","超大型ワイドスターマイン","ふるさとの四季","岩塚製菓グループ"),
 ("2","20:00","超大型スーパーベスビアス","福田グループスピリット～100年先も誠実～","福田グループ"),
 ("2","20:00","ベスビアス超大型スターマイン","感謝の絆、未来への輝き","日産サティオ新潟西"),
 ("2","20:00","スペシャルスターマイン","すべての『いのち』にありがとう","長岡市仏教会・立正佼成会長岡教会"),
 ("2","20:00","超大型スーパーベスビアス","AIRMANスパーキング","AIRMAN"),
 ("2","20:15","花火","故郷はひとつ","協賛企業一同"),
 ("2","20:15","ベスビアス大スターマイン","インプレッション・トリップ","クラブツーリズム"),
 ("2","20:15","超大型スーパーベスビアス","光差す明日へ","伊藤建設グループ・宮下電設"),
 ("2","20:15","ベスビアス大スターマイン","挑戦の精神","カナデビア・カナデビアE&E"),
 ("2","20:15","超大型スーパーベスビアス","夜空に輝くプレミアム","セブン-イレブン・セブン銀行"),
 ("2","20:30","ベスビアス超大型スターマイン","エコの華","ナンバグループ"),
 ("2","20:30","超大型スーパーベスビアス","光ある美しく豊かな世界へ","トクサイ"),
 ("2","20:30","ベスビアス大スターマイン","夏の思い出","コメリ"),
 ("2","20:40","超大型ミラクルスターマイン","スプラッシュファイヤー炎の舞","ワタナベグループ"),
 ("2","20:40","ベスビアス大スターマイン","ホテルニューオータニ長岡感謝の大輪","ホテルニューオータニ長岡"),
 ("2","20:45","超大型スーパーベスビアス","長岡とともに技大、感謝の50年","長岡技術科学大学開学50周年記念花火協賛者一同"),
 ("2","20:45","超大型スーパーベスビアス","クリーンエナジー","石油資源開発"),
 ("2","20:45","超大型スーパーベスビアス","つながり","ネクスコ東日本長岡管理事務所グループ"),
 ("2","21:00","超大型スーパーベスビアス","鉄にいのち、ひとに未来","北越メタル"),
 ("2","21:00","ベスビアス大スターマイン","龍華～未来へ続く日の光～","目崎グループ"),
 ("2","21:00","超大型スーパーベスビアス","感謝","SBFグループ・三共土地開発"),
 ("2","21:00","超大型スーパーベスビアス","皆さまへ創業百周年の感謝を込めて","ジェスクホリウチ"),
 ("2","21:25","サプライズ花火","君と花火と約束と","映画製作委員会"),
]
P3 = [
 ("3","19:25","ナイアガラ超大型スターマイン","カノン～この先に続く道(ミライ)に向かって～","JTB＆エヌ・シィ・ティ"),
 ("3","19:25","ベスビアス超大型スターマイン","上場記念花火アリガトウナガオカ","フラー"),
 ("3","19:25","超大型スーパーベスビアス","マンマのフルーツカーニバル","北陸学園"),
 ("3","19:25","スペシャルスターマイン","水とともに","前澤工業ほか"),
 ("3","19:25","超大型スーパーベスビアス","つながれ！～モノづくりの未来へ～","シマキュウグループ"),
 ("3","19:25","ベスビアス超大型スターマイン","千人鮮色、ありがとうの花","高田建築事務所と愉快な仲間たち"),
 ("3","19:25","ベスビアス大スターマイン","インプレッション・トリップ","クラブツーリズム"),
 ("3","19:45","花火","この空の花","協賛企業一同"),
 ("3","19:45","ベスビアス大スターマイン","燃ゆる華心","コロナ"),
 ("3","19:45","超大型スーパーベスビアス","アルプスアルパイン・シャイニングスター","アルプスアルパイングループ"),
 ("3","19:45","スターマイン","信濃川の夕涼み","イオン長岡店・専門店街Well"),
 ("3","19:45","超大型スーパーベスビアス","あなたとずっとこの空と","岡三にいがた証券"),
 ("3","19:45","ベスビアス超大型スターマイン","金燦、銀燦","伊丹自動車ほか"),
 ("3","20:00","超大型ワイドスターマイン","安心と感動に満ちた世界と未来のために","日本精機グループ"),
 ("3","20:00","ベスビアス超大型スターマイン","太陽の輝き","太陽工機"),
 ("3","20:00","超大型スーパーベスビアス","子供たちの未来のために","スプリックス"),
 ("3","20:00","ベスビアス超大型スターマイン","ともに創る未来へ","ヤマト運輸長岡主管支店"),
 ("3","20:00","10号28発","酔火連発 尺玉の響","酔火連"),
 ("3","20:15","花火","HOPE TO THE FUTURE～未来へ~","協賛企業一同"),
 ("3","20:15","スターマイン","輝け愛花火","崇徳厚生事業団職員有志一同"),
 ("3","20:15","ベスビアス超大型スターマイン","天空華宴","大石組"),
 ("3","20:15","ベスビアス大スターマイン","mirai","扉-tobira-"),
 ("3","20:15","10号60連発＆ベスビアス大スターマイン","駆け抜ける丙午 60-60","長岡高校昭和60年卒還暦花火の会"),
 ("3","20:30","ベスビアス超大型スターマイン","No Attack,No Chance","ピカイチ・INSIGHT LAB"),
 ("3","20:30","スペシャルスターマイン","平和への誓い","創価学会"),
 ("3","20:30","ベスビアス超大型スターマイン","夜空に感謝の花束","明治安田"),
 ("3","20:40","超大型ミラクルスターマイン","世界への躍動","ヨネックス"),
 ("3","20:40","ベスビアス超大型スターマイン","大河の夕景","高野不動産グループ"),
 ("3","20:45","超大型スーパーベスビアス","99年分のありがとうを込めて","ナカザワグループ"),
 ("3","20:45","超大型スーパーベスビアス","ラブラブファイヤー2026","アークベルグループ長岡ベルナール"),
 ("3","20:45","超大型スーパーベスビアス","アイデアと技術の宝石箱","大森機械工業長岡工場"),
 ("3","21:00","7号12発・10号12発","未来飛翔","長岡市共同受注グループ「けやき」"),
 ("3","21:00","ベスビアス超大型スターマイン","新潟の未来を見つめ続けて","ダイア建設新潟"),
 ("3","21:00","スターマイン","パラダイス・イン・ザ・スカイ","スーパーセンタームサシ長岡店"),
 ("3","21:00","ベスビアス大スターマイン","支社開設60周年 感謝を空へ 安心を未来へ","日本生命"),
]

TYPE_FILL = {
 "ナイアガラ超大型スターマイン": "大手大橋の光の滝とスターマインの共演が見どころ。",
 "ベスビアス超大型スターマイン": "湧き上がる光の奔流が夜空を焦がす伝統の型。",
 "超大型スーパーベスビアス": "ベスビアス最大級の打上げ規模を誇る演目。",
 "ベスビアス大スターマイン": "連射の花火が大きな光の柱を夜空に描く。",
 "超大型ワイドスターマイン": "横一線に広がる光のパノラマが見どころ。",
 "超大型ミラクルスターマイン": "変化に富んだ多彩な演出が楽しめる。",
 "スペシャルスターマイン": "テーマに沿った音楽と色彩の演出が光る。",
 "スターマイン": "速射連発の花火が途切れなく夜空を彩る。",
 "花火": "多数の協賛により打ち上げられる特別演目。",
 "サプライズ花火": "映画とタイアップした特別演出の一幕。",
}
TYPE_EN = {
 "ナイアガラ超大型スターマイン": "a Niagara cascade pouring from the Ohte Bridge paired with a super-wide starmine",
 "ベスビアス超大型スターマイン": "a traditional Vesuvius super starmine, a volcanic torrent of light",
 "超大型スーパーベスビアス": "the largest class of Vesuvius starmine, filling the whole field of view",
 "ベスビアス大スターマイン": "a traditional Vesuvius-style grand starmine",
 "超大型ワイドスターマイン": "a super-wide starmine spread across a broad launch front",
 "超大型ミラクルスターマイン": "a super-size starmine with varied, theatrical effects",
 "スペシャルスターマイン": "a themed starmine staged with music and color",
 "スターマイン": "a rapid-fire starmine",
 "花火": "a special program supported by many sponsors",
 "サプライズ花火": "a surprise display tied to a feature film",
}
PADS = ["信濃川の夜空を彩る演目の一つ。", "慰霊と復興の祈りを受け継ぐ大会を彩る。", "会場を沸かせる夏の夜の一幕。"]

def split_sponsors(s):
    parts = [p for p in re.split(r"[・、＆&,]| と ", s) if len(p) >= 2]
    out = []
    for p in [s] + parts:
        if p not in out:
            out.append(p)
    return out

def ja_long(days, time, typ, sponsor):
    fill = TYPE_FILL.get(typ, "大輪の尺玉が連続して夜空に開く。")
    for sp in (sponsor, split_sponsors(sponsor)[1] + "ほか" if len(split_sponsors(sponsor)) > 1 else sponsor):
        base = f"長岡花火（{days} {time}頃）で打ち上げられる{sp}協賛の{typ}。"
        for tail in (fill + PADS[0], fill + PADS[1], fill + PADS[2], fill, PADS[0] + PADS[1], PADS[1], PADS[0], ""):
            t = base + tail
            if 60 <= len(t) <= 80:
                return t
    base = f"長岡花火（{days} {time}頃）で打ち上げられる{typ}。"
    for tail in (fill + PADS[0], fill + PADS[1], fill, PADS[0] + PADS[1], PADS[1], PADS[0], ""):
        t = base + tail
        if 60 <= len(t) <= 80:
            return t
    raise ValueError(f"ja_long adjust failed: {days} {typ} {sponsor}")

def ja_short(days, time, typ, sponsor):
    typs = typ if len(typ) <= 14 else "超大型スターマイン"
    cands = [
        f"{days} {time}頃打上げ。{sponsor}協賛の{typs}。",
        f"{days} {time}頃打上げ。{split_sponsors(sponsor)[1] if len(split_sponsors(sponsor))>1 else sponsor}ほか協賛の{typs}。",
        f"{days} {time}頃打上げの{typs}。長岡花火の演目の一つ。",
        f"{days} {time}頃に打ち上げられる{typs}。",
    ]
    for t in cands:
        if 25 <= len(t) <= 50:
            return t
    raise ValueError(f"ja_short adjust failed: {days} {typ} {sponsor}")

def en_pair(title, days_en, time, typ, sponsor):
    ten = TYPE_EN.get(typ, "a program of large shells")
    long = f'"{title}" is {ten}, launched around {time} on {days_en} at the Nagaoka Festival Grand Fireworks Show, sponsored by {sponsor}.'
    if len(long) < 140:
        long = long[:-1] + " over the Shinano River."
    if len(long) < 140:
        long += " The display lights up the summer night sky."
    if len(long) > 270:
        long = f'"{title}" is {ten}, launched around {time} on {days_en} at the Nagaoka Festival Grand Fireworks Show over the Shinano River.'
    assert 140 <= len(long) <= 270, (title, len(long))
    short = f"{ten[0].upper() + ten[1:]} at the Nagaoka Fireworks Show ({days_en}, around {time})."
    assert 45 <= len(short) <= 160, (title, len(short))
    return long, short

# --- 主要演目（手書き解説） ---
def curated(id, name, kana, en, aliases, priority, ja_l, ja_s, en_l, en_s, tags_ja, tags_en, prefecture="長岡花火"):
    return {
        "id": id, "name": name, "name_kana": kana, "name_en": en,
        "aliases": [{"name": a} for a in aliases],
        **{**BASE, "prefecture": prefecture}, "priority": priority,
        "description": {
            "title_ja": name, "title_en": en,
            "description_ja_long": ja_l, "description_ja_short": ja_s,
            "description_en_long": en_l, "description_en_short": en_s,
            "tags_ja": tags_ja, "tags_en": tags_en, "quality": "good", "url": URL,
        },
    }

entries = [
    curated(9000001, "長岡花火", "ながおかはなび", "Nagaoka Fireworks",
        ["長岡まつり大花火大会", "花火"], 1000,
        "毎年8月2日・3日に信濃川河川敷で開かれる日本三大花火の一つ。長岡空襲からの復興と慰霊、平和への祈りを受け継ぎ、正三尺玉やフェニックスが夜空を彩る。",
        "8月2日・3日開催の日本三大花火の一つ。慰霊と復興の祈りを込めた大輪が信濃川の夜空を彩る。",
        "The Nagaoka Festival Grand Fireworks Show is held on August 2nd and 3rd along the Shinano River. One of Japan's three greatest displays, it carries a prayer for peace and recovery born from the 1945 air raid, crowned by giant shells and the Phoenix.",
        "One of Japan's three greatest fireworks festivals, held August 2nd and 3rd on the Shinano River in Nagaoka.",
        ["花火", "夏", "新潟県", "祭り"], ["Fireworks", "Summer", "Niigata", "Festival"], prefecture="新潟県"),
    curated(9000002, "復興祈願花火フェニックス", "ふっこうきがんはなびふぇにっくす", "Phoenix",
        ["フェニックス", "フェニックス花火協賛者一同"], 999,
        "中越地震からの復興を祈って2005年に誕生した、長岡花火を象徴する超大型スターマイン。全長約2kmの打上げ幅から音楽に乗せて光のパノラマが広がる。",
        "復興祈願で2005年に誕生。全長約2kmの光のパノラマが音楽とともに広がる名物スターマイン。",
        "The Phoenix is Nagaoka's signature super-wide starmine, first launched in 2005 as a prayer for recovery from the Chuetsu Earthquake, filling a front of about two kilometers along the Shinano River in sync with music.",
        "Nagaoka's signature two-kilometer starmine, born in 2005 as a prayer for earthquake recovery.",
        ["花火", "長岡花火", "復興祈願"], ["Fireworks", "Nagaoka", "Phoenix"]),
    curated(9000003, "正三尺玉", "しょうさんじゃくだま", "Shosanjakudama",
        ["三尺玉", "吉乃川", "越後交通", "原信", "INPEX"], 998,
        "直径約90cmの巨大な玉を上空約600mへ打ち上げ、直径約650mの大輪を咲かせる長岡名物。開花とともに腹に響く轟音が信濃川の会場全体を包み込む。",
        "直径約90cmの玉が上空約600mで約650mの大輪に開く、長岡名物の巨大花火。",
        "The Shosanjakudama is Nagaoka's iconic giant shell, about 90 centimeters across, fired some 600 meters up to bloom roughly 650 meters wide, its thunderous report rolling across the Shinano River venue.",
        "Nagaoka's iconic giant shell, blooming about 650 meters across high above the Shinano River.",
        ["花火", "長岡花火", "三尺玉"], ["Fireworks", "Nagaoka", "Giant shell"]),
    curated(9000004, "白菊", "しらぎく", "Shiragiku",
        ["慰霊の白菊", "嘉瀬煙火工業", "長岡花火財団"], 997,
        "白一色で静かに開く慰霊の花火。花火師・嘉瀬誠次氏がシベリア抑留の戦友に捧げたことに始まり、戦災と災害の犠牲者への祈りとして大会の冒頭を飾る。",
        "白一色で開く慰霊の花火。犠牲者への鎮魂を込め、大会の冒頭に静かに打ち上げられる。",
        "The Shiragiku is a pure-white memorial shell first fired by pyrotechnician Seiji Kase in mourning for comrades lost in Siberian internment. It now opens the festival as a prayer for all victims of war and disaster.",
        "A pure-white memorial shell that opens the festival as a silent prayer for victims of war and disaster.",
        ["花火", "長岡花火", "慰霊"], ["Fireworks", "Nagaoka", "Memorial"]),
    curated(9000005, "天地人花火", "てんちじんはなび", "Tenchijin Fireworks",
        ["天地人", "天地人花火協賛企業一同"], 996,
        "長岡ゆかりの武将・直江兼続を描いた大河ドラマ「天地人」を記念する音楽付きスターマイン。義と愛の物語を思わせる勇壮な花火が信濃川の夜空を駆ける。",
        "大河ドラマ「天地人」を記念した音楽付きスターマイン。直江兼続の物語を花火で描く。",
        "The Tenchijin Fireworks are a musical starmine commemorating the taiga drama about Naoe Kanetsugu, the samurai of loyalty and love tied to the Nagaoka region, sweeping gallantly across the night sky over the river.",
        "A musical starmine honoring the taiga drama Tenchijin and the local samurai Naoe Kanetsugu.",
        ["花火", "長岡花火", "天地人"], ["Fireworks", "Nagaoka", "Tenchijin"]),
    curated(9000006, "米百俵花火・尺玉100連発", "こめひゃっぴょうはなびしゃくだまひゃくれんぱつ", "Kome Hyappyo 100 Shells",
        ["米百俵花火", "尺玉100連発", "TDKラムダ", "NNCエンジニアリング"], 995,
        "戊辰戦争後、米百俵を売って学校を建てた長岡藩の精神にちなむ演目。上空約330mで開く尺玉100発を、息つく間もなく連続で打ち上げる圧巻の構成。",
        "「米百俵の精神」にちなみ尺玉100発を連続打上げ。大会屈指の迫力を誇る演目。",
        "Honoring the Kome Hyappyo spirit of investing in the future, one hundred giant shells are fired in relentless succession, each blooming about 330 meters up, making one of the festival's most powerful programs.",
        "One hundred giant shells fired in relentless succession, honoring Nagaoka's Kome Hyappyo spirit.",
        ["花火", "長岡花火", "米百俵"], ["Fireworks", "Nagaoka", "Kome Hyappyo"]),
    curated(9000007, "ナイアガラ", "ないあがら", "Niagara",
        ["ナイアガラ大瀑布", "植木組", "朝日山"], 994,
        "信濃川に架かる大手大橋から、滝のように光が流れ落ちる大仕掛けの花火。川面に映る金色のカーテンが美しく、プログラム中盤の見どころの一つ。",
        "大手大橋から滝のように流れ落ちる光のカーテン。川面に映る金色が美しい仕掛け花火。",
        "The Niagara is a set-piece cascade of golden sparks pouring from the Ohte Bridge over the Shinano River, its falling curtain of light mirrored on the water as one of the highlights of the mid-program.",
        "A golden cascade of sparks pouring from the Ohte Bridge, mirrored on the Shinano River.",
        ["花火", "長岡花火", "ナイアガラ"], ["Fireworks", "Nagaoka", "Niagara"]),
    curated(9000008, "ベスビアス超大型スターマイン", "べすびあすちょうおおがたすたーまいん", "Vesuvius Starmine",
        ["ベスビアス"], 993,
        "火山ベスビオの噴火にたとえられる長岡伝統の超大型スターマイン。広い打上げ幅から何百発もの花火が湧き上がり、光の奔流が夜空を焦がす主力演目。",
        "火山の噴火にたとえられる長岡伝統の超大型スターマイン。光の奔流が夜空を焦がす。",
        "Named for the eruption of Mount Vesuvius, this traditional Nagaoka super starmine sends hundreds of shells surging upward like a torrent of fire, staged several times through the festival by its sponsors.",
        "Nagaoka's traditional super starmine, a volcanic torrent of light staged throughout the festival.",
        ["花火", "長岡花火", "スターマイン"], ["Fireworks", "Nagaoka", "Starmine"]),
    curated(9000009, "匠の花火", "たくみのはなび", "Takumi Fireworks",
        ["匠"], 992,
        "長岡花火財団が贈る、花火師の技を主役にした演目。色の変化や開きの正確さ、消え際の美しさなど、一発ごとの完成度をじっくり味わえる通好みの時間。",
        "花火師の技を主役に、一発ごとの色・開き・消え際の完成度を味わう通好みの演目。",
        "Presented by the Nagaoka Fireworks Foundation, Takumi puts the pyrotechnician's craft itself center stage, savoring each shell for its color shifts, the precision of its bloom, and the beauty of its fade.",
        "A connoisseur's program devoted to the artisan's craft, one carefully judged shell at a time.",
        ["花火", "長岡花火", "花火師"], ["Fireworks", "Nagaoka", "Artisan"]),
]
have_names = {e["name"] for e in entries}

# --- プログラム演目（テンプレート生成・同名は両日統合） ---
merged = {}
for day, time, typ, title, sponsor in P2 + P3:
    m = merged.setdefault(title, {"days": [], "time": time, "types": [], "sponsors": []})
    m["days"].append(day)
    if typ not in m["types"]: m["types"].append(typ)
    if sponsor not in m["sponsors"]: m["sponsors"].append(sponsor)

nid = 9000101
for title, m in merged.items():
    if title in have_names: continue
    typ = m["types"][0]
    both = set(m["days"]) == {"2", "3"}
    days = "8月2日・3日" if both else f"8月{m['days'][0]}日"
    days_en = "August 2nd and 3rd" if both else f"August {m['days'][0]}"
    sponsor = "・".join(m["sponsors"])
    aliases = [{"name": a} for a in split_sponsors(sponsor)] + [{"name": typ}]
    en_l, en_s = en_pair(title, days_en, m["time"], typ, sponsor)
    entries.append({
        "id": nid, "name": title, "aliases": aliases, **BASE, "priority": 900,
        "description": {
            "title_ja": title, "title_en": title,
            "description_ja_long": ja_long(days, m["time"], typ, sponsor),
            "description_ja_short": ja_short(days, m["time"], typ, sponsor),
            "description_en_long": en_l, "description_en_short": en_s,
            "tags_ja": ["花火", "長岡花火"], "tags_en": ["Fireworks", "Nagaoka"],
            "quality": "good", "url": URL,
        },
    })
    nid += 1

json.dump(entries, open("public/data/featured.json", "w"), ensure_ascii=False, indent=2)
print(f"{len(entries)} entries written")
