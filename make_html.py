# -*- coding: utf-8 -*-
"""Convert the three Markdown reports to styled standalone HTML."""
import re, html, os, base64, mimetypes
from markdown_it import MarkdownIt

md = MarkdownIt("gfm-like", {"linkify": False}).enable("table")

CSS = """
:root { --ink:#1c2833; --accent:#1F618D; --red:#B03A2E; --line:#d5dbdb; }
* { box-sizing: border-box; }
body { font-family: "Microsoft JhengHei","Noto Sans CJK TC",sans-serif; color:var(--ink);
       line-height:1.85; margin:0; background:#f7f8fa; }
main { max-width:960px; margin:0 auto; padding:48px 28px 80px; background:#fff;
       box-shadow:0 0 24px rgba(0,0,0,.06); }
h1 { font-size:1.65rem; border-bottom:4px solid var(--accent); padding-bottom:.4em; line-height:1.5;}
h2 { font-size:1.3rem; margin-top:2.2em; border-left:6px solid var(--accent); padding-left:.55em; }
h3 { font-size:1.12rem; margin-top:1.8em; color:var(--accent); }
p  { margin:1em 0; text-align:justify; }
strong { color:#111; }
table { border-collapse:collapse; width:100%; margin:1.4em 0; font-size:.92rem; }
th,td { border:1px solid var(--line); padding:.5em .7em; vertical-align:top; }
th { background:#eef3f7; }
tr:nth-child(even) td { background:#fafcfd; }
blockquote { border-left:4px solid var(--red); background:#fdf6f5; margin:1.2em 0;
             padding:.6em 1.1em; color:#4d3b39; }
img { max-width:100%; height:auto; display:block; margin:1.4em auto;
      border:1px solid var(--line); border-radius:6px; }
hr { border:none; border-top:2px solid var(--line); margin:2.4em 0; }
sup.cite { color:var(--red); font-size:.72em; }
nav.toc { background:#f2f6f9; border:1px solid var(--line); border-radius:8px;
          padding:1em 1.4em; margin:1.6em 0; font-size:.92rem; }
nav.toc ul { margin:.3em 0; padding-left:1.2em; }
nav.toc a { color:var(--accent); text-decoration:none; }
nav.toc a:hover { text-decoration:underline; }
details.sources { margin-top:3em; background:#fbfbf6; border:1px solid var(--line);
                  border-radius:8px; padding:1em 1.4em; font-size:.88rem; }
details.sources ol li { margin:.35em 0; }
details.sources a { color:var(--accent); word-break:break-all; }
footer { text-align:center; color:#888; font-size:.8rem; margin-top:3em; }
code { background:#f0f2f4; padding:.1em .35em; border-radius:4px; }
"""

SOURCES = {
 1:("台股法說會資料庫：關貿(6183) 2025Q3 法說會簡報","https://finmoconf.diveinvest.net/presentation/6899db43a2ef6df0422b28fe"),
 2:("富邦券商：關貿(6183) 董監事經理人持股明細","https://fubon-ebrokerdj.fbs.com.tw/z/zc/zck/zck_6183.djhtm"),
 3:("關貿網路官網：股東專欄","https://www.trade-van.com/investor/index.do?act=stockholder&type=11"),
 4:("富果直送：關貿法說會重點備忘錄（2026-08-11）","https://blog.fugle.tw/post/earnings-call-6183-2026-08-11"),
 5:("ctwant：關貿股權報導","https://www.ctwant.com/article/491864/"),
 6:("中時：財政部持股關貿36.11%（2026-08-04）","https://www.chinatimes.com/realtimenews/20260804002976-260407"),
 7:("中央社：關貿股利相關報導（2026-06-27）","https://www.cna.com.tw/news/afe/202606270040.aspx"),
 8:("pchome股市：關貿董事改選公告（2026-06-26）","https://pchome.megatime.com.tw/m/news/cat2/20260626/9700006183202606262.html"),
 9:("LINE TODAY：羅廷瑋質詢發言（2026-08-04）","https://today.line.me/tw/v3/article/JPnvl1y"),
 10:("東森新聞：EZ WAY解密——759萬人註冊（2026-08-03）","https://news.ebc.net.tw/news/living/564443"),
 11:("壹蘋新聞網：關貿網路背景（2026-08-04）","https://news.nextapple.com/finance/20260804/93388976E32AAE97C7D8BC1770E47702"),
 12:("Threads：關貿官股民營背景整理","https://www.threads.com/@shuen.nein/post/DbmF_DUEie5"),
 13:("MapleFeather（夜羽凌）：EZ WAY 個資與三途徑完整查證（2026-09-20）","https://maplefeather.com/article/ezway-personal-data-customs-2026"),
 14:("Yahoo奇摩新聞／鏡週刊：掌握全台75%進口報單（2026-08-04）","https://tw.news.yahoo.com/%E6%8E%8C%E6%8F%A1%E5%85%A8%E5%8F%B075-%E9%80%B2%E5%8F%A3%E5%A0%B1%E5%96%AE-%E9%97%9C%E8%B2%BF%E6%B0%91%E7%87%9F%E8%83%8C%E6%99%AF%E6%9B%9D%E5%85%89-020800064.html"),
 15:("ETtoday：30年資服老兵躺槍（2026-08-03）","https://finance.ettoday.net/news/3212529"),
 16:("經濟日報：EZ WAY 向民眾收費？關務署三大澄清（2026-08-03）","https://money.udn.com/money/story/7307/9667776"),
 17:("東森新聞(knews)：EZ Way爆個資與收費爭議（2026-08-03）","https://www.knews.com.tw/news/EDD8E56FE24563755F24F9A054928362"),
 18:("民報：EZ WAY是私企經營還要收費？（2026-08-03）","https://www.peoplenews.tw/articles/lifestyle/47577"),
 19:("Yahoo奇摩新聞：EZWay遭控釀觸法，關務署承諾3個月檢討（2026-07-29）","https://tw.news.yahoo.com/ez-way%E9%81%AD%E6%8E%A7%E9%87%80%E8%A7%B8%E6%B3%95-%E8%BD%89%E5%AB%81%E6%94%B6%E8%B2%BB-%E9%97%9C%E5%8B%99%E7%BD%B2%E6%89%BF%E8%AB%BE3%E5%80%8B%E6%9C%88%E5%85%A7%E6%8F%90%E6%AA%A2%E8%A8%8E%E5%A0%B1%E5%91%8A-065841587.html"),
 20:("蕃新聞：林岱樺揭EZ WAY轉嫁收費亂象（2026-07-29）","https://n.yam.com/Article/20260729828269"),
 21:("中央社：EZ Way個資監管，關務署將實地查核（2026-08-06）","https://www.cna.com.tw/news/afe/202608060356.aspx"),
 22:("財政部：海關對 EZ Way APP 相關議題之說明（2026-08-06）","https://www.mof.gov.tw/singlehtml/384fb3077bb349ea973e7fc6f13b6974?cntId=2af82ae85bca4fdca08cba85f0ba08bd"),
 23:("三立新聞：關務署承諾3個月內提最終檢討報告（2026-08-07）","https://www.setn.com/news/1885489"),
 24:("關務署：簡介與操作說明（快遞收貨人實名認證）","https://web.customs.gov.tw/singlehtml/3150?cntId=cus1_3150_3150_1471"),
 25:("國發會：鬆綁招商文件（2020年收費說明會紀錄）","https://ws.ndc.gov.tw/Download.ashx?u=LzAwMS9hZG1pbmlzdHJhdG9yLzEwL3JlbGZpbGUvNzEzMC8zNTA4Mi9jNzMyM2E5Ny1jYmI1LTQ0YTctYTQyZC0xYWZiMDY1YzBmYTcucGRm"),
 26:("遠傳 FETnet：EZ Way一定要用嗎？（2026-01）","https://www.fetnet.net/content/cbu/tw/lifecircle/tech/2026/01/ezway.html"),
 27:("好悠他提：日本集運包稅與EZ WAY（2026-03）","https://goyoutati.com/blogs/shipping/japan-forwarding-tax-included-2026"),
 28:("雪倫想想：2026 BuyandShip 教學終極版（2026-07）","https://sharonisthinking.com/buyandship-ultimate-guide-for-beginner/"),
 29:("NINIYCC：易利委 EZway 設定教學","https://niniycc.com/ezway/"),
 30:("選物日寄：2026 海外網購新制與 EZ WAY 教學（2026-08）","https://www.mypickdiary.com/blogs/taiwan-overseas-shopping-ezway-2026"),
 31:("好運器：海外購物免稅額與2026/3/1預先委任（2026-10-01）","https://0523.tw/cross-border-import-tax-rules-taiwan"),
 32:("好運器：EZWay 忘記密碼與FAQ（2026-05）","https://0523.tw/ezway-forgot-password"),
 33:("Mobile01：集運倉選擇討論串","https://www.mobile01.com/topicdetail.php?f=393&t=6948696"),
 34:("phongnhaexplorer：淘寶一定要用EZWAY嗎","https://zh.phongnhaexplorer.com/zh/%e5%b0%8f%e6%8a%80%e5%b7%a7/%e6%b7%98%e5%ae%9d%e4%b8%80%e5%ae%9a%e8%a6%81%e7%94%a8ezway%e5%97%8e%ef%bc%9f.html"),
 35:("汎宇電商官網：通關網路服務","https://www.universalec.com/service/customs_clearance.html"),
 36:("公視新聞網 PNN：EZ WAY實名認證爭議（2026-08-04）","https://news.pts.org.tw/article/820783"),
 37:("行政院全球資訊網：數位發展部8月27日成立","https://www.ey.gov.tw/Page/9277F759E41CCD91/1fe80b2b-0439-400f-bd52-e2a9a76e182b"),
 38:("findit 政策資料庫：數發部2022/8/27掛牌","https://findit.org.tw/Files/ResArticleAttachedFile/0a7b7dbd-c537-4237-982b-948a343850de.pdf"),
 39:("中央社：卓榮泰拍板不副署財劃法（2025-12-15）","https://www.cna.com.tw/news/aipl/202512150171.aspx"),
 40:("Yahoo奇摩新聞：不副署財劃法創憲政首例（2025-12-15）","https://tw.news.yahoo.com/%E4%B8%8D%E5%89%AF%E7%BD%B2%E8%B2%A1%E5%8A%83%E6%B3%95%E5%89%B5%E6%86%B2%E6%94%BF%E9%A6%96%E4%BE%8B-%E5%8D%93%E6%8F%86-%E6%94%BF%E9%99%A2%E6%9C%89%E8%B2%AC%E4%BB%BB%E6%8D%8D%E8%A1%9B%E6%AC%8A%E5%8A%9B%E5%88%86%E7%AB%8B%E5%8E%9F%E5%89%87-091000873.html"),
 41:("LINE TODAY：卓榮泰——善盡民主憲政守門人職責（2025-12-14）","https://today.line.me/tw/v3/article/oq9Wae6"),
 42:("民報：卓榮泰不副署財劃法——什麼是副署（2025-12-16）","https://www.peoplenews.tw/articles/hot-news/6646"),
 43:("風傳媒(zmedia)：正式宣布不副署，卓榮泰提三理由（2025-12-15）","https://www.zmedia.com.tw/Document/Detail/39555"),
 44:("記者爆料網：行政院不副署財劃法修正案（2025-12-15）","https://new-reporter.com/news/110570/"),
 45:("信傳媒：行政院臨時院會拍板覆議警察人事條例（2025-04-01）","https://www.cmmedia.com.tw/home/articles/53583"),
 46:("立法院公報：院會質詢與譴責案紀錄","https://ppg.ly.gov.tw/ppg/PublicationBulletinDetail/download/communique1/final/pdf/114/74/LCIDC01_1147401.pdf"),
 47:("自由時報：憲法法庭持續運轉，2/6新判決（2026-02-05）","https://news.ltn.com.tw/news/politics/breakingnews/5333542"),
 48:("wingverse：憲法法庭停擺又重啟——114憲判1解析（2026-04）","https://www.wingverse.com/constitutional-court-comparative-law/"),
 49:("學習好：警察50歲退休金攻略（2026-04-29）","http://thxuexi.com/retirement-pension-for-police-officers-at-the-age-of-50/"),
}

def embed_images(body, md_dir):
    """Replace relative <img src> with base64 data URIs so the HTML is self-contained."""
    def repl(m):
        src = m.group(2)
        if src.startswith(("data:", "http://", "https://")):
            return m.group(0)
        path = os.path.join(md_dir, src)
        if not os.path.isfile(path):
            print("  !! image not found:", path)
            return m.group(0)
        mime = mimetypes.guess_type(path)[0] or "image/png"
        b64 = base64.b64encode(open(path, "rb").read()).decode("ascii")
        print("  embedded:", src, f"({len(b64)//1024} KB b64)")
        return f'{m.group(1)}src="data:{mime};base64,{b64}"{m.group(3)}'
    return re.sub(r'(<img\b[^>]*?\s)src="([^"]+)"([^>]*>)', repl, body)

def convert(src, dst, title, with_sources=False):
    text = open(src, encoding="utf-8").read()
    body = md.render(text)
    body = embed_images(body, os.path.dirname(os.path.abspath(src)))
    # citations [^n^] -> sup
    body = re.sub(r"\[\^(\d+)\^\]", r'<sup class="cite">[\1]</sup>', body)
    # add ids to headings + collect TOC
    toc, counter = [], 0
    def add_id(m):
        nonlocal counter
        counter += 1
        level, content = m.group(1), m.group(2)
        hid = f"sec{counter}"
        plain = re.sub(r"<[^>]+>", "", content)
        if int(level) <= 3:
            toc.append((int(level), plain.strip(), hid))
        return f'<h{level} id="{hid}">{content}</h{level}>'
    body = re.sub(r"<h([1-3])>(.*?)</h\1>", add_id, body, flags=re.S)
    items = "".join(
        f'<li style="margin-left:{(lv-1)*1.1}em"><a href="#{hid}">{html.escape(t)}</a></li>'
        for lv, t, hid in toc if lv <= 2)
    toc_html = f'<nav class="toc"><strong>目錄</strong><ul>{items}</ul></nav>'
    src_html = ""
    if with_sources:
        lis = "".join(f'<li value="{k}">{html.escape(v[0])} — <a href="{v[1]}">{v[1]}</a></li>'
                      for k, v in sorted(SOURCES.items()))
        src_html = (f'<details class="sources"><summary><strong>引用來源對照（編號對應文中標註）</strong></summary>'
                    f'<ol>{lis}</ol></details>')
    page = f"""<!DOCTYPE html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title><style>{CSS}</style></head>
<body><main>
{toc_html}
{body}
{src_html}
<footer>產生日期：2026-10-08｜本 HTML 為研究報告之閱讀版本，引用編號對應文末來源對照</footer>
</main></body></html>"""
    open(dst, "w", encoding="utf-8").write(page)
    print("written:", dst, len(page), "bytes")

base = r"C:\Users\ed249\Documents\kimi\tasks\2026-10-08\20-20-26-0f3511d0"
convert(base + r"\EZ_WAY_關貿爭議完整研究報告_20261008.md",
        base + r"\EZ_WAY_關貿爭議完整研究報告_20261008.html",
        "EZ WAY 易利委與關貿網路爭議：完整事實研究報告（2026-10-08）", with_sources=True)
convert(base + r"\對抗消耗監督資源_初步量化分析.md",
        base + r"\對抗消耗監督資源_初步量化分析.html",
        "對抗消耗監督資源：初步量化檢驗（2026-10-08）")
convert(base + r"\委外與責任碎片化分析_20261008.md",
        base + r"\委外與責任碎片化分析_20261008.html",
        "委外、專案分工與責任碎片化（2026-10-08）")
convert(base + r"\碎片化框架第二案例_台電虧損_20261008.md",
        base + r"\碎片化框架第二案例_台電虧損_20261008.html",
        "碎片化檢驗框架第二案例：台電虧損（2026-10-08）")
convert(base + r"\MBB卸責槽_治理必然性彙整_20261008.md",
        base + r"\MBB卸責槽_治理必然性彙整_20261008.html",
        "MBB 卸責槽與治理必然性——彙整報告（2026-10-08）")
convert(base + r"\碎片化框架多案例擴充_20261009.md",
        base + r"\碎片化框架多案例擴充_20261009.html",
        "碎片化檢驗框架：多案例擴充報告（2026-10-09）")
convert(base + r"\檢討疊代記錄_20261009.md",
        base + r"\檢討疊代記錄_20261009.html",
        "五份報告檢討與疊代記錄（2026-10-09）")
convert(base + r"\相關報告盤點與彙整_20261011.md",
        base + r"\相關報告盤點與彙整_20261011.html",
        "相關報告盤點與彙整（2026-10-11）")
convert(base + r"\委外碎片化xMBB卸責槽_例證研究_長程稽核_20261011.md",
        base + r"\委外碎片化xMBB卸責槽_例證研究_長程稽核_20261011.html",
        "委外碎片化 × MBB 卸責槽：關係例證研究與長程稽核管理（2026-10-11）")
convert(base + r"\閉環驗證框架v2_十案例複驗_20261011.md",
        base + r"\閉環驗證框架v2_十案例複驗_20261011.html",
        "閉環驗證框架 v2：MBB 8D 紀律的十案例複驗（2026-10-11）")
