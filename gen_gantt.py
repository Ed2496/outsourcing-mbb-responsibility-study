# -*- coding: utf-8 -*-
"""S1–S8 階段甘特圖產生器（斷裂時間軸版）：
X 軸 1990–2023 壓縮至左 1/4，2023–2031 展開至右 3/4（斷軸記號在 2023）。
Y 軸監控專案、上軸 S1–S8 模型帶。階段分界多為研究推估（年/半年精度）。"""
import html

X0, X1 = 1990, 2031          # 時間範圍（年）
BREAK = 2023                 # 斷軸點
W, LEFT, RIGHT = 1560, 190, 30
TOP_MODEL, TOP_AXIS, ROW_H, GROUP_H = 92, 46, 34, 30
NOW = 2026 + 9 / 12 + 10 / 365  # 2026-10-11 ≈ 2026.775
PLOT = W - LEFT - RIGHT

STAGES = {
    "S1": ("潛伏進行", "#9aa0a6"),
    "S2": ("爆發",     "#d93025"),
    "S3": ("高峰對質", "#f29900"),
    "S4": ("制度回應", "#1a73e8"),
    "S5": ("疲勞靜默", "#673ab7"),
    "S6": ("切割處分", "#8d5524"),
    "S7": ("敘事逆轉結案", "#188038"),
    "S8": ("長程遺留", "#009688"),
}

GROUPS = [
    ("A｜進行中（S3–S5）", [
        ("行政—立法憲政對抗", "高峰慢性化", [("S2", 2024.38, 2024.55), ("S3", 2024.55, NOW)], 2024.4, "now"),
        ("EZ WAY 收費與檢討報告", "關貿爭議", [("S1", 2020.29, 2026.58), ("S2", 2026.58, 2026.67), ("S4", 2026.67, NOW)], 2026.58, "now"),
        ("資遣通報黑數", "本輪 2026 中", [("S2", 2026.4, 2026.5), ("S4", 2026.5, NOW)], 2026.42, "now"),
        ("中聯毒油食安案", "2026/7/1 曝光", [("S1", 2026.25, 2026.5), ("S2", 2026.5, 2026.58), ("S3", 2026.58, 2026.67), ("S4", 2026.67, NOW)], 2026.5, "now"),
        ("F-16V 交機延期", "2019 建案", [("S1", 2019.0, 2026.2), ("S2", 2026.2, 2026.4), ("S4", 2026.4, NOW)], 2026.25, "now"),
        ("潛艦國造海鯤艦", "2016 啟動", [("S1", 2016.0, 2025.3), ("S2", 2025.3, 2025.75), ("S3", 2025.75, 2026.45), ("S4", 2026.45, 2026.72), ("S6", 2026.72, NOW)], 2025.3, "now"),
        ("徐佳青濫用公務資源案", "2026/10/7 請辭", [("S2", 2026.66, 2026.77), ("S6", 2026.77, NOW)], 2026.68, "now"),
        ("吳乃仁案 1.7 億追償", "2002 售地案", [("S1", 2002.0, 2005.5), ("S2", 2005.5, 2006.5), ("S3", 2006.5, 2014.0), ("S4", 2014.0, 2026.45), ("S5", 2026.45, NOW)], 2005.5, "now"),
        ("個保會組織法", "2023/5 三讀卡關", [("S2", 2023.38, 2023.5), ("S4", 2023.5, 2025.0), ("S5", 2025.0, NOW)], 2023.4, "now"),
        ("福麥炸藥採購案", "室內裝修得標", [("S2", 2025.9, 2026.0), ("S3", 2026.0, 2026.55), ("S5", 2026.55, NOW)], 2025.95, "now"),
    ]),
    ("B｜已結案／敘事化（S7–S8，觀察中）", [
        ("台電累虧與電價公式", "711 億撥補敘事", [("S1", 2022.0, 2023.0), ("S2", 2023.0, 2023.25), ("S3", 2023.25, 2024.0), ("S4", 2024.0, 2025.0), ("S7", 2025.0, NOW)], 2023.05, "now"),
        ("國艦國造／彈藥弊案", "監院糾正後無聲", [("S1", 2021.0, 2025.0), ("S2", 2025.0, 2025.25), ("S3", 2025.25, 2025.5), ("S6", 2025.5, 2025.65), ("S7", 2025.65, NOW)], 2025.05, "now"),
        ("數位中介法", "2023 暫緩擱置", [("S2", 2022.45, 2022.7), ("S3", 2022.7, 2023.0), ("S4", 2023.0, 2023.4), ("S7", 2023.4, NOW)], 2022.5, "now"),
        ("高端疫苗採購", "2026/8 出口越南", [("S1", 2021.35, 2021.55), ("S2", 2021.55, 2021.75), ("S3", 2021.75, 2023.0), ("S4", 2023.0, 2025.0), ("S7", 2025.0, 2026.55), ("S8", 2026.55, NOW)], 2021.55, "now"),
        ("進口雞蛋（對照組）", "2024 專辦解散", [("S1", 2023.2, 2023.68), ("S2", 2023.68, 2023.75), ("S3", 2023.75, 2024.0), ("S4", 2024.0, 2024.15), ("S6", 2024.15, 2024.3), ("S7", 2024.3, 2024.5)], 2023.7, "done"),
    ]),
    ("C｜歷史樣本（長程標本）", [
        ("陳水扁貪污案", "21 年樣本", [("S2", 2005.5, 2006.5), ("S3", 2006.5, 2015.5), ("S5", 2015.5, 2022.5), ("S7", 2022.5, 2023.85), ("S8", 2023.85, NOW)], 2005.5, "now"),
        ("拉法葉艦購案", "35 年樣本", [("S1", 1991.65, 1993.9), ("S2", 1993.9, 1997.0), ("S3", 1997.0, 2003.0), ("S4", 2003.0, 2010.4), ("S7", 2010.4, 2012.0), ("S6", 2015.0, 2016.0), ("S8", 2022.0, 2030.0)], 1993.9, "plan"),
    ]),
]

def x(y):
    """斷裂時間軸：1990–2023 → 左 1/4；2023–2031 → 右 3/4。"""
    if y <= BREAK:
        return LEFT + (y - X0) / (BREAK - X0) * PLOT * 0.25
    return LEFT + PLOT * 0.25 + (y - BREAK) / (X1 - BREAK) * PLOT * 0.75

def ticks():
    """產生 (年, 是否主刻度, 是否標字)"""
    out = []
    for yr in range(X0, BREAK + 1):
        out.append((yr, yr % 5 == 0, yr % 5 == 0))
    for yr in range(BREAK + 1, X1 + 1):
        out.append((yr, True, True))
    return out

n_rows = sum(len(g[1]) for g in GROUPS)
n_groups = len(GROUPS)
H = TOP_MODEL + TOP_AXIS + n_rows * ROW_H + n_groups * GROUP_H + 60

svg = []
svg.append(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="Microsoft JhengHei, PingFang TC, sans-serif">')

# ===== 上軸：S1–S8 模型帶 =====
band_w = PLOT / 8
for i, (code, (name, color)) in enumerate(STAGES.items()):
    bx = LEFT + i * band_w
    svg.append(f'<rect x="{bx:.1f}" y="14" width="{band_w:.1f}" height="40" fill="{color}" fill-opacity="0.16" stroke="{color}" stroke-opacity="0.5"/>')
    svg.append(f'<text x="{bx + band_w/2:.1f}" y="32" text-anchor="middle" font-size="14" font-weight="700" fill="{color}">{code}</text>')
    svg.append(f'<text x="{bx + band_w/2:.1f}" y="48" text-anchor="middle" font-size="11.5" fill="#444">{name}</text>')
svg.append(f'<text x="{LEFT}" y="10" font-size="11" fill="#888">上軸：S1–S8 階段模型（生命週期相對位置，非日曆區間）</text>')

# ===== 時間軸（主 X 軸，斷裂式） =====
axis_y = TOP_MODEL + TOP_AXIS
for yr, major, label in ticks():
    xx = x(yr)
    svg.append(f'<line x1="{xx:.1f}" y1="{axis_y - (10 if major else 5)}" x2="{xx:.1f}" y2="{H - 40}" stroke="#{"000" if major else "ccc"}" stroke-opacity="{0.9 if major else 0.5}" stroke-width="{1 if major else 0.5}"/>')
    if label:
        svg.append(f'<text x="{xx:.1f}" y="{axis_y - 16}" text-anchor="middle" font-size="11.5" font-weight="600" fill="#333">{yr}</text>')

# 斷軸記號（2023 處）
bx23 = x(BREAK)
for yy in range(axis_y - 14, H - 42, 16):
    svg.append(f'<line x1="{bx23 - 7:.1f}" y1="{yy + 7}" x2="{bx23 + 1:.1f}" y2="{yy - 1}" stroke="#999" stroke-width="1.6"/>')
svg.append(f'<text x="{bx23:.1f}" y="{H - 26}" text-anchor="middle" font-size="11" fill="#999">// 2023 斷軸：前 33 年壓縮至 1/4 寬</text>')

# 今日線
nx = x(NOW)
svg.append(f'<line x1="{nx:.1f}" y1="{axis_y}" x2="{nx:.1f}" y2="{H - 40}" stroke="#d93025" stroke-width="1.6" stroke-dasharray="6 4"/>')
svg.append(f'<text x="{nx + 5:.1f}" y="{axis_y + 14}" font-size="11.5" font-weight="700" fill="#d93025">今日 2026-10-11</text>')

# ===== 專案列 =====
y_cursor = axis_y
for gname, rows in GROUPS:
    y_cursor += GROUP_H
    svg.append(f'<text x="10" y="{y_cursor - 10}" font-size="13.5" font-weight="700" fill="#1a1a1a">{gname}</text>')
    svg.append(f'<line x1="{LEFT}" y1="{y_cursor - 16}" x2="{W - RIGHT}" y2="{y_cursor - 16}" stroke="#ddd" stroke-width="0.8"/>')
    for name, note, segs, burst, end in rows:
        bar_y = y_cursor + (ROW_H - 18) / 2
        for code, s, e in segs:
            color = STAGES[code][1]
            sx, ex = x(s), x(e)
            svg.append(f'<rect x="{sx:.1f}" y="{bar_y:.1f}" width="{max(ex - sx, 2):.1f}" height="18" fill="{color}" fill-opacity="0.75" rx="2"/>')
            if ex - sx > 34:
                svg.append(f'<text x="{(sx + ex) / 2:.1f}" y="{bar_y + 13:.1f}" text-anchor="middle" font-size="10.5" font-weight="700" fill="#fff">{code}</text>')
        bx = x(burst)
        cy = bar_y + 9
        svg.append(f'<path d="M {bx:.1f} {cy - 12} L {bx + 6:.1f} {cy} L {bx:.1f} {cy + 12} L {bx - 6:.1f} {cy} Z" fill="#1a1a1a"/>')
        ex_end = x(segs[-1][2])
        if end == "now":
            svg.append(f'<path d="M {ex_end:.1f} {cy} l 12 -6 v 12 Z" fill="#d93025"/>')
        elif end == "done":
            svg.append(f'<circle cx="{ex_end:.1f}" cy="{cy}" r="4.5" fill="#188038"/>')
        elif end == "plan":
            svg.append(f'<line x1="{x(2016):.1f}" y1="{bar_y + 9:.1f}" x2="{x(2022):.1f}" y2="{bar_y + 9:.1f}" stroke="#999" stroke-dasharray="3 4" stroke-width="1.4"/>')
        svg.append(f'<text x="12" y="{cy + 4:.1f}" font-size="12.5" font-weight="600" fill="#222">{html.escape(name)}</text>')
        svg.append(f'<text x="{x(X1) + 4:.1f}" y="{cy + 4:.1f}" font-size="10.5" fill="#888">{html.escape(note)}</text>')
        y_cursor += ROW_H

# 底軸年份
for yr, major, label in ticks():
    if label:
        svg.append(f'<text x="{x(yr):.1f}" y="{H - 10}" text-anchor="middle" font-size="10.5" fill="#666">{yr}</text>')
svg.append(f'<text x="{LEFT}" y="{H + 6}" font-size="11" fill="#888">◆ 黑色菱形＝爆發點　▶ 紅箭頭＝進行中　● 綠點＝已結案　色塊＝S1–S8 階段（分界為研究推估，半年精度）</text>')

svg.append("</svg>")
svg_doc = "\n".join(svg)

page = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>S1–S8 階段甘特圖｜監控專案長程追蹤（2026-10-11，斷裂時間軸）</title>
<style>
  body {{ font-family: "Microsoft JhengHei", "PingFang TC", sans-serif; margin: 0; background: #fafafa; color: #222; }}
  main {{ max-width: 1600px; margin: 0 auto; padding: 24px 20px 48px; }}
  h1 {{ font-size: 22px; margin: 0 0 4px; }}
  .meta {{ font-size: 13px; color: #777; margin-bottom: 6px; }}
  .box {{ background: #fff; border: 1px solid #e3e3e3; border-radius: 10px; padding: 16px; overflow-x: auto; }}
  .legend {{ display: flex; flex-wrap: wrap; gap: 10px 18px; font-size: 13px; margin: 12px 0 16px; }}
  .legend span {{ display: inline-flex; align-items: center; gap: 6px; }}
  .chip {{ width: 14px; height: 14px; border-radius: 3px; display: inline-block; }}
  ol {{ font-size: 14px; line-height: 1.85; padding-left: 22px; }}
  footer {{ margin-top: 20px; font-size: 12px; color: #999; }}
</style>
</head>
<body>
<main>
<h1>S1–S8 階段甘特圖：15 個監控專案＋2 個歷史樣本的長程位置</h1>
<div class="meta">產出：2026-10-11｜X 軸＝斷裂年月軸（1990–2023 壓縮至 1/4 寬，2023–2031 展開至 3/4 寬）｜Y 軸＝監控專案（三組）｜上軸＝S1–S8 模型帶｜資料基準：研究報告總綱第三節</div>
<div class="legend">{"".join(f'<span><span class="chip" style="background:{c};opacity:.8"></span>{k} {n}</span>' for k, (n, c) in STAGES.items())}</div>
<div class="box">
{svg_doc}
</div>
<h2 style="font-size:16px;margin-top:20px;">圖上可直接讀出的四件事</h2>
<ol>
<li><b>越長的 bar，S5（紫）與 S7（綠）佔比越高。</b>吳乃仁（24 年）S4 長達 12 年後直接滑入 S5；陳水扁 S5 凍結 7 年後由 S7 無罪＋S8 重燃收尾——長案不是被解決，是被時間稀釋。</li>
<li><b>S4→S5 的交界是本研究的黃金監控窗。</b>目前海鯤艦、吳乃仁、個保會、福麥四案正站在或已滑過交界；歷史樣本顯示滑過後 6–12 個月內若無具名進度，通常以 S6/S7 敘事收斂。</li>
<li><b>拉法葉的 2016–2022 白色真空帶</b>（刑事熄滅後、再生意化前）是「完全靜默期」的實形——35 年 bar 中整整 6 年無任何階段活動，卻也無人宣布結案。</li>
<li><b>已結案組（B 組）全部以 S7 綠色收尾，但沒有一案的綠色段出現過「制度修正」標記</b>——對照組雞蛋反而走過完整 S1–S7。結案與修正脫鉤，是本圖對「消失結案」最直接的量化呈現。</li>
</ol>
<footer>階段分界為研究推估（半年精度），精確月分以各案原始時序為準；斷軸比例可於 gen_gantt.py 的 x() 調整。新增專案時在 GROUPS 陣列加列後重新執行即可。</footer>
</main>
</body>
</html>
"""

out = r"C:\Users\ed249\Documents\kimi\tasks\2026-10-08\20-20-26-0f3511d0\S1-S8階段甘特圖_20261011.html"
with open(out, "w", encoding="utf-8") as f:
    f.write(page)
print("written:", out)
