"""
╔══════════════════════════════════════════════════════════════╗
║        ACADEMICAI — LECTURER PLATFORM  v2.0                  ║
║  PDF → Slides · MCQ · Exam (WORD) · Summary · Flashcards     ║
║  Zero external packages — Python built-ins only              ║
╚══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import requests
import json
import re
import base64
import io
import zipfile
import random

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Kaabe — Academic AI Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');
*,*::before,*::after{box-sizing:border-box;}
html,body,[class*=css]{font-family:'DM Sans',sans-serif;background:#080c14 !important;color:#dde3ee !important;}
.stApp{background:#080c14 !important;}
section[data-testid=stSidebar]{background:#050810 !important;border-right:1px solid #1a2235;}
section[data-testid=stSidebar] *{color:#8899bb !important;}
#MainMenu,footer,header{visibility:hidden;}

.hero{background:linear-gradient(135deg,#0d1628 0%,#111e38 50%,#0d1628 100%);
  border:1px solid #1e3060;border-radius:16px;padding:1.8rem 2.5rem;
  margin-bottom:1.5rem;display:flex;align-items:center;gap:1.5rem;}
.hero-icon{font-size:3.2rem;line-height:1;}
.hero h1{font-family:'Syne',sans-serif;font-size:1.9rem;font-weight:800;color:#fff;margin:0 0 .3rem;}
.hero p{font-size:.88rem;color:#7a8fb5;margin:0;}

.tool-bar{display:flex;gap:8px;margin-bottom:1.5rem;flex-wrap:wrap;}
.tool-btn{padding:.5rem 1.1rem;border:1px solid #1a2a45;border-radius:8px;
  background:#0d1628;color:#8899bb;cursor:pointer;font-size:.85rem;
  font-family:'DM Sans',sans-serif;transition:all .15s;white-space:nowrap;}
.tool-btn:hover{border-color:#3a7bd5;color:#fff;}
.tool-btn.active{border-color:#3a7bd5;background:#0f1e3a;color:#fff;font-weight:600;}

.section-card{background:#0d1628;border:1px solid #1a2a45;border-radius:12px;
  padding:1.3rem 1.5rem;margin-bottom:1rem;}
.section-title{font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;
  color:#fff;margin-bottom:.8rem;display:flex;align-items:center;gap:8px;}

.mcq-card{background:#0a1220;border:1px solid #1a2a45;border-radius:10px;
  padding:1.1rem 1.3rem;margin-bottom:.9rem;}
.mcq-q{font-weight:600;font-size:.93rem;color:#e0e8f8;margin-bottom:.6rem;}
.mcq-opt{display:flex;align-items:flex-start;gap:10px;padding:.35rem .5rem;
  border-radius:6px;font-size:.86rem;color:#8899bb;margin-bottom:3px;border:1px solid transparent;}
.mcq-opt.correct{background:#0a2a1a;border-color:#1a5a30;color:#4ade80;}
.mcq-letter{font-family:'Syne',sans-serif;font-weight:700;color:#3a7bd5;min-width:18px;}
.mcq-explain{background:#0f2240;border-left:3px solid #3a7bd5;border-radius:0 6px 6px 0;
  padding:.5rem .8rem;font-size:.8rem;color:#7ab3d4;margin-top:.5rem;}

.flashcard{background:linear-gradient(135deg,#0d1e38,#111e38);border:1px solid #2a4070;
  border-radius:14px;padding:2rem;text-align:center;min-height:180px;
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  margin-bottom:1rem;transition:all .2s;}
.flashcard:hover{border-color:#3a7bd5;transform:translateY(-2px);}
.fc-label{font-size:.68rem;color:#3a7bd5;text-transform:uppercase;letter-spacing:.1em;margin-bottom:.7rem;}
.fc-text{font-size:1.05rem;font-weight:600;color:#e0e8f8;}

.summary-section{background:#0a1220;border:1px solid #1a2a45;border-radius:10px;
  padding:1.1rem 1.3rem;margin-bottom:.7rem;}
.summary-heading{font-family:'Syne',sans-serif;font-size:.93rem;font-weight:700;
  color:#3a7bd5;margin-bottom:.4rem;}
.summary-text{font-size:.86rem;color:#8899bb;line-height:1.75;}
.key-term{display:inline-block;background:#0f2240;border:1px solid #2a4070;
  border-radius:6px;padding:3px 10px;font-size:.78rem;color:#60a5fa;margin:2px 3px;}

.exam-preview{background:#0a0f1e;border:1px solid #1a2a45;border-radius:10px;
  padding:1.2rem 1.5rem;margin-bottom:.8rem;font-family:'DM Sans',sans-serif;}
.exam-sec-hdr{background:#0f1e3a;border-radius:6px;padding:.5rem .9rem;
  font-weight:700;color:#60a5fa;font-size:.88rem;margin:.8rem 0 .5rem;}
.exam-q-row{padding:.45rem 0;border-bottom:1px solid #131e30;font-size:.87rem;color:#c0cce0;}
.exam-qnum{color:#3a7bd5;font-weight:700;margin-right:6px;}
.marks-tag{float:right;background:#0d1628;border:1px solid #2a3a55;
  border-radius:20px;padding:1px 8px;font-size:.72rem;color:#7ab3d4;}
.ans-line{border-bottom:1px dashed #1e2e45;height:26px;margin:.3rem 0;}

.progress-bar{background:#0d1628;border-radius:8px;height:5px;overflow:hidden;margin:.5rem 0;}
.progress-fill{height:100%;border-radius:8px;background:linear-gradient(90deg,#3a7bd5,#00c896);transition:width .4s ease;}
.stat-pill{display:inline-flex;align-items:center;gap:5px;background:#0d1628;
  border:1px solid #1a2a45;border-radius:20px;padding:3px 10px;font-size:.78rem;color:#8899bb;margin-right:6px;}
.stat-pill b{color:#fff;}
.qa-msg{padding:.8rem 1rem;border-radius:10px;margin-bottom:.6rem;font-size:.88rem;line-height:1.65;}
.qa-user{background:#0f2240;border:1px solid #1e3a6a;color:#c0d4f5;text-align:right;}
.qa-ai{background:#0a1a30;border:1px solid #1a2a45;color:#8ab4d4;}
.qa-label{font-size:.66rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:#3a7bd5;margin-bottom:.25rem;}

.stButton>button{font-family:'DM Sans',sans-serif !important;font-weight:500 !important;}
.stTextInput>div>div,.stTextArea textarea,.stSelectbox>div>div,.stNumberInput>div>div>input{
  background:#0d1628 !important;border-color:#1a2a45 !important;color:#dde3ee !important;}
.stTabs [data-baseweb=tab-list]{background:#0d1628;border-radius:8px;padding:4px;gap:4px;}
.stTabs [data-baseweb=tab]{color:#5a7099 !important;font-family:'DM Sans',sans-serif !important;font-size:13px !important;}
.stTabs [aria-selected=true]{background:#1a2a45 !important;color:#fff !important;border-radius:6px !important;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# THEMES FOR PPTX
# ─────────────────────────────────────────────────────────────
THEMES = {
    "Academic Dark":   {"bg":"0F1729","title_bg":"1E293B","accent":"60A5FA","text":"F8FAFC","sub":"94A3B8","box":"1E293B","mono":"93C5FD"},
    "University Blue": {"bg":"0A1940","title_bg":"0F2850","accent":"3B82F6","text":"FFFFFF","sub":"93C5FD","box":"143264","mono":"BAE6FD"},
    "Forest Research": {"bg":"0A1A0A","title_bg":"142E14","accent":"4ADE80","text":"F0FDF4","sub":"86EFAC","box":"143214","mono":"BBF7D0"},
    "Executive White": {"bg":"FFFFFF","title_bg":"F1F5F9","accent":"2563EB","text":"0F172A","sub":"64748B","box":"F8FAFC","mono":"1D4ED8"},
    "Crimson":         {"bg":"140505","title_bg":"280A0A","accent":"EF4444","text":"FEF2F2","sub":"FCA5A5","box":"280A0A","mono":"FECACA"},
    "Purple Scholar":  {"bg":"0F0F1A","title_bg":"1E1E3A","accent":"A855F7","text":"F8FAFC","sub":"C4B5FD","box":"1E1E3A","mono":"DDD6FE"},
}

# ─────────────────────────────────────────────────────────────
# GEMINI API
# ─────────────────────────────────────────────────────────────
MODELS = ["gemini-2.5-flash","gemini-2.0-flash","gemini-2.5-flash-preview-05-20",
          "gemini-2.0-flash-lite","gemini-1.5-flash-latest"]

def call_gemini(api_key, prompt, pdf_b64=None, max_tokens=8192, json_mode=True):
    parts = []
    if pdf_b64:
        parts.append({"inline_data":{"mime_type":"application/pdf","data":pdf_b64}})
    parts.append({"text": prompt})
    cfg = {"temperature":0.2,"maxOutputTokens":max_tokens}
    if json_mode:
        cfg["responseMimeType"] = "application/json"
    last_err = ""
    for model in MODELS:
        url  = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        body = {"contents":[{"parts":parts}],"generationConfig":cfg}
        try:
            r = requests.post(url, json=body, timeout=120)
        except requests.exceptions.Timeout:
            raise ValueError("Request timed out. Try fewer questions or a smaller PDF.")
        except requests.exceptions.ConnectionError:
            raise ValueError("No internet connection.")
        if r.status_code == 200:
            d = r.json()
            try: return d["candidates"][0]["content"]["parts"][0]["text"]
            except (KeyError,IndexError): raise ValueError(f"Unexpected response: {str(d)[:200]}")
        elif r.status_code == 404: last_err=r.text; continue
        elif r.status_code == 403: raise ValueError("Invalid API key. Get free key at aistudio.google.com/app/apikey")
        elif r.status_code == 429: raise ValueError("Rate limit. Wait 1 minute and try again.")
        else: raise ValueError(f"API error {r.status_code}: {r.text[:200]}")
    raise ValueError(f"No working Gemini model.\n{last_err[:150]}")

# ─────────────────────────────────────────────────────────────
# JSON REPAIR
# ─────────────────────────────────────────────────────────────
def safe_parse(raw: str) -> dict:
    text = raw.strip()
    text = re.sub(r"^```(?:json)?","",text).strip()
    text = re.sub(r"```$","",text).strip()
    start=text.find("{"); end=text.rfind("}")+1
    if start==-1: raise ValueError("No JSON found in AI response.")
    candidate=text[start:end]
    result=[]; in_s=False; esc=False
    for ch in candidate:
        if esc: result.append(ch); esc=False; continue
        if ch=="\\" and in_s: esc=True; result.append(ch); continue
        if ch=='"': in_s=not in_s; result.append(ch); continue
        if in_s and ch=="\n": result.append(" "); continue
        if in_s and ch=="\r": continue
        result.append(ch)
    candidate="".join(result)
    candidate=re.sub(r",\s*([\}\]])",r"\1",candidate)
    try: return json.loads(candidate)
    except: pass
    candidate=re.sub(r'(?<!\\)\\([^"\\/bfnrtu])',r' ',candidate)
    try: return json.loads(candidate)
    except: pass
    stack=[]; in_s=False; esc=False
    for ch in candidate:
        if esc: esc=False; continue
        if ch=="\\" and in_s: esc=True; continue
        if ch=='"': in_s=not in_s; continue
        if not in_s:
            if ch in "{[": stack.append("}" if ch=="{" else "]")
            elif ch in "}]" and stack and stack[-1]==ch: stack.pop()
    candidate=candidate+"".join(reversed(stack))
    candidate=re.sub(r",\s*([\}\]])",r"\1",candidate)
    try: return json.loads(candidate)
    except: raise ValueError("Could not parse AI response. Click Generate again — Gemini sometimes varies output.")

# ─────────────────────────────────────────────────────────────
# WORD DOCX BUILDER (pure zipfile + xml, zero dependencies)
# ─────────────────────────────────────────────────────────────
def build_docx(xml_body: str) -> bytes:
    """Assemble a valid .docx from raw word/document.xml body content."""
    CT = "application/vnd.openxmlformats-officedocument.wordprocessingml"

    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml"  ContentType="application/xml"/>
  <Override PartName="/word/document.xml"  ContentType="{CT}.document.main+xml"/>
  <Override PartName="/word/styles.xml"    ContentType="{CT}.styles+xml"/>
  <Override PartName="/word/settings.xml"  ContentType="{CT}.settings+xml"/>
  <Override PartName="/docProps/app.xml"   ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>""".replace("{CT}", CT)

    rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""

    doc_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>
</Relationships>"""

    styles = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
          xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml">
  <w:docDefaults>
    <w:rPrDefault><w:rPr>
      <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/>
      <w:sz w:val="24"/><w:szCs w:val="24"/>
    </w:rPr></w:rPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:pPr><w:spacing w:after="160" w:line="276" w:lineRule="auto"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:pPr><w:spacing w:before="240" w:after="120"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="36"/><w:color w:val="1F3864"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:pPr><w:spacing w:before="200" w:after="80"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="28"/><w:color w:val="2F5496"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/>
    <w:pPr><w:spacing w:before="160" w:after="60"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="24"/><w:color w:val="1F4E79"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Code">
    <w:name w:val="Code"/>
    <w:rPr><w:rFonts w:ascii="Courier New" w:hAnsi="Courier New"/><w:sz w:val="20"/></w:rPr>
  </w:style>
</w:styles>"""

    settings = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:defaultTabStop w:val="720"/>
</w:settings>"""

    app_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">
  <Application>Kaabe</Application>
</Properties>"""

    document = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml">
  <w:body>
    {xml_body}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"
               w:header="720" w:footer="720" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>"""

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", rels)
        z.writestr("word/document.xml", document)
        z.writestr("word/_rels/document.xml.rels", doc_rels)
        z.writestr("word/styles.xml", styles)
        z.writestr("word/settings.xml", settings)
        z.writestr("docProps/app.xml", app_xml)
    buf.seek(0)
    return buf.read()

# ─────────────────────────────────────────────────────────────
# DOCX XML HELPERS
# ─────────────────────────────────────────────────────────────
NS = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'

def we(s):
    """XML escape for Word content."""
    return (str(s).replace("&","&amp;").replace("<","&lt;")
            .replace(">","&gt;").replace('"',"&quot;"))

def w_para(text, style="Normal", bold=False, italic=False,
           size=24, color=None, align="left", indent=0, space_after=160):
    """Single paragraph XML."""
    algn_map = {"left":"left","center":"center","right":"right","justify":"both"}
    algn = algn_map.get(align, "left")
    b_tag   = "<w:b/>" if bold else ""
    i_tag   = "<w:i/>" if italic else ""
    col_tag = f'<w:color w:val="{color}"/>' if color else ""
    ind_tag = f'<w:ind w:left="{indent}"/>' if indent else ""
    return f"""<w:p>
  <w:pPr>
    <w:pStyle w:val="{style}"/>
    <w:jc w:val="{algn}"/>
    <w:spacing w:after="{space_after}"/>
    {ind_tag}
  </w:pPr>
  <w:r>
    <w:rPr>{b_tag}{i_tag}{col_tag}<w:sz w:val="{size}"/><w:szCs w:val="{size}"/></w:rPr>
    <w:t xml:space="preserve">{we(text)}</w:t>
  </w:r>
</w:p>"""

def w_para_runs(runs, style="Normal", align="left", space_after=160, indent=0):
    """Paragraph with multiple runs (mixed formatting)."""
    algn_map = {"left":"left","center":"center","right":"right"}
    algn = algn_map.get(align,"left")
    ind_tag = f'<w:ind w:left="{indent}"/>' if indent else ""
    runs_xml = ""
    for r in runs:
        b   = "<w:b/>"  if r.get("bold")   else ""
        i   = "<w:i/>"  if r.get("italic") else ""
        rc  = r.get("color","")
        col = f'<w:color w:val="{rc}"/>' if rc else ""
        sz  = r.get("size", 24)
        fn  = f'<w:rFonts w:ascii="{r["font"]}" w:hAnsi="{r["font"]}"/>' if r.get("font") else ""
        runs_xml += f'<w:r><w:rPr>{b}{i}{col}{fn}<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/></w:rPr><w:t xml:space="preserve">{we(r.get("text",""))}</w:t></w:r>'
    return f"""<w:p>
  <w:pPr><w:pStyle w:val="{style}"/><w:jc w:val="{algn}"/>
  <w:spacing w:after="{space_after}"/>{ind_tag}</w:pPr>
  {runs_xml}
</w:p>"""

def w_empty(n=1):
    return "<w:p><w:pPr><w:spacing w:after='0'/></w:pPr></w:p>" * n

def w_hr():
    return """<w:p><w:pPr><w:pBdr>
  <w:bottom w:val="single" w:sz="6" w:space="1" w:color="2F5496"/>
</w:pBdr><w:spacing w:after="120"/></w:pPr></w:p>"""

def w_table(headers, rows, col_widths=None):
    """Build a Word table."""
    total_w = 9360  # twips for a standard page
    n_cols  = len(headers)
    if not col_widths:
        col_widths = [total_w // n_cols] * n_cols

    def cell(text, bold=False, shade=None):
        b = "<w:b/>" if bold else ""
        sh = f'<w:shd w:val="clear" w:color="auto" w:fill="{shade}"/>' if shade else ""
        return f"""<w:tc>
  <w:tcPr>{sh}<w:tcW w:w="{col_widths[0]}" w:type="dxa"/></w:tcPr>
  <w:p><w:pPr><w:spacing w:after="60"/></w:pPr>
  <w:r><w:rPr>{b}<w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>
  <w:t xml:space="preserve">{we(text)}</w:t></w:r></w:p>
</w:tc>"""

    # Header row
    hdr_cells = "".join(cell(h, bold=True, shade="2F5496") for h in headers)
    # Swap shade per header for color — simplify to one shade
    hdr_cells = ""
    for i,h in enumerate(headers):
        shade="1F3864"
        hdr_cells += f"""<w:tc>
  <w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="{shade}"/>
  <w:tcW w:w="{col_widths[i%len(col_widths)]}" w:type="dxa"/></w:tcPr>
  <w:p><w:pPr><w:spacing w:after="60"/><w:jc w:val="center"/></w:pPr>
  <w:r><w:rPr><w:b/><w:color w:val="FFFFFF"/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>
  <w:t xml:space="preserve">{we(h)}</w:t></w:r></w:p>
</w:tc>"""

    body_rows = ""
    for ri, row in enumerate(rows):
        shade = "EEF2FF" if ri%2==0 else "FFFFFF"
        row_cells = ""
        for ci, val in enumerate(row[:n_cols]):
            cw = col_widths[ci] if ci < len(col_widths) else col_widths[-1]
            row_cells += f"""<w:tc>
  <w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="{shade}"/>
  <w:tcW w:w="{cw}" w:type="dxa"/></w:tcPr>
  <w:p><w:pPr><w:spacing w:after="60"/></w:pPr>
  <w:r><w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>
  <w:t xml:space="preserve">{we(val)}</w:t></w:r></w:p>
</w:tc>"""
        body_rows += f"<w:tr>{row_cells}</w:tr>"

    return f"""<w:tbl>
  <w:tblPr>
    <w:tblStyle w:val="TableGrid"/>
    <w:tblW w:w="{total_w}" w:type="dxa"/>
    <w:tblBorders>
      <w:top    w:val="single" w:sz="4" w:color="2F5496"/>
      <w:left   w:val="single" w:sz="4" w:color="2F5496"/>
      <w:bottom w:val="single" w:sz="4" w:color="2F5496"/>
      <w:right  w:val="single" w:sz="4" w:color="2F5496"/>
      <w:insideH w:val="single" w:sz="4" w:color="CCCCCC"/>
      <w:insideV w:val="single" w:sz="4" w:color="CCCCCC"/>
    </w:tblBorders>
    <w:tblCellMar>
      <w:top    w:w="80"  w:type="dxa"/>
      <w:left   w:w="120" w:type="dxa"/>
      <w:bottom w:w="80"  w:type="dxa"/>
      <w:right  w:w="120" w:type="dxa"/>
    </w:tblCellMar>
  </w:tblPr>
  <w:tr>{hdr_cells}</w:tr>
  {body_rows}
</w:tbl>
{w_empty()}"""

def w_answer_lines(n=4):
    lines=""
    for _ in range(n):
        lines+="""<w:p><w:pPr>
  <w:spacing w:after="0"/>
  <w:pBdr><w:bottom w:val="single" w:sz="4" w:space="1" w:color="AAAAAA"/></w:pBdr>
</w:pPr></w:p>"""
    return lines + w_empty()

# ─────────────────────────────────────────────────────────────
# EXAM WORD BUILDER
# ─────────────────────────────────────────────────────────────
def build_exam_docx(data: dict, include_ms: bool) -> bytes:
    parts = []

    # ── Cover page ─────────────────────────────────────────
    parts.append(w_para(data.get("institution","UNIVERSITY"), "Normal",
                        bold=True, size=32, color="1F3864", align="center", space_after=80))
    parts.append(w_para(data.get("title","EXAMINATION PAPER"), "Heading1",
                        align="center", space_after=80))
    parts.append(w_para(data.get("course",""), "Normal",
                        bold=True, size=26, align="center", space_after=60))
    parts.append(w_hr())

    # Info table
    info_rows = [
        ["Date:", data.get("date","________________")],
        ["Duration:", data.get("duration","")],
        ["Total Marks:", str(data.get("total_marks",""))],
        ["Student Name:", "________________________________"],
        ["Student ID:", "________________________________"],
        ["Lecturer:", data.get("lecturer","________________________________")],
    ]
    for row in info_rows:
        parts.append(w_para_runs([
            {"text": row[0], "bold": True, "size": 22, "color": "1F3864"},
            {"text": "  " + row[1], "size": 22},
        ], space_after=80))

    parts.append(w_hr())
    parts.append(w_empty())

    # Instructions
    parts.append(w_para("INSTRUCTIONS TO CANDIDATES", "Heading2",
                        color="1F3864", space_after=80))
    for inst in data.get("instructions",[]):
        parts.append(w_para_runs([
            {"text": "• ", "bold": True, "color": "2F5496", "size": 22},
            {"text": inst, "size": 22},
        ], space_after=60))

    parts.append(w_empty(2))

    # ── Sections ───────────────────────────────────────────
    for sec in data.get("sections", []):
        sec_name  = sec.get("name","")
        sec_desc  = sec.get("description","")
        sec_marks = sec.get("marks","")
        sec_instr = sec.get("instructions","")

        parts.append(w_hr())
        parts.append(w_para(
            f"{sec_name}  —  {sec_desc}  ({sec_marks} marks)",
            "Heading2", color="1F3864", space_after=60
        ))
        if sec_instr:
            parts.append(w_para(sec_instr, "Normal", italic=True,
                                size=20, color="555555", space_after=120))

        stype = sec.get("type","short_answer")
        qs    = sec.get("questions",[])

        for q in qs:
            qnum  = q.get("num","")
            qtext = q.get("text","")
            qmks  = q.get("marks","")
            alines= q.get("answer_lines", 4)

            # Question line
            parts.append(w_para_runs([
                {"text": f"Q{qnum}.  ", "bold": True, "size": 24, "color": "1F3864"},
                {"text": qtext, "size": 22},
                {"text": f"  [{qmks} marks]", "bold": True, "size": 20, "color": "2F5496", "italic": True},
            ], space_after=80))

            # MCQ options
            if stype == "mcq" and q.get("options"):
                for letter, opt in q["options"].items():
                    parts.append(w_para_runs([
                        {"text": f"  {letter})  ", "bold": True, "size": 22, "color": "2F5496"},
                        {"text": opt, "size": 22},
                    ], space_after=40))
                parts.append(w_empty())

            # Sub-parts
            elif q.get("parts"):
                for p in q["parts"]:
                    parts.append(w_para_runs([
                        {"text": f"  ({p.get('part','')})  ", "bold": True, "size": 22, "color": "2F5496"},
                        {"text": p.get("text",""), "size": 22},
                        {"text": f"  [{p.get('marks','')} marks]", "size": 20, "color": "888888", "italic": True},
                    ], space_after=60, indent=360))
                    parts.append(w_answer_lines(p.get("answer_lines", 4)))
            else:
                parts.append(w_answer_lines(alines))

        parts.append(w_empty())

    # ── Mark Scheme ────────────────────────────────────────
    if include_ms:
        parts.append(w_para("", "Normal"))
        # Page break simulation
        parts.append(w_para("─"*80, "Normal", size=8, color="CCCCCC"))
        parts.append(w_empty())
        parts.append(w_para("MARK SCHEME", "Heading1",
                            color="1F3864", align="center", space_after=80))
        parts.append(w_para(data.get("title",""), "Normal",
                            italic=True, align="center", size=22, color="555555", space_after=160))
        parts.append(w_hr())

        for sec in data.get("sections",[]):
            parts.append(w_para(sec.get("name",""), "Heading2", color="1F3864", space_after=80))
            stype = sec.get("type","short_answer")
            for q in sec.get("questions",[]):
                ans = q.get("model_answer","")
                qmk = q.get("marks","")
                parts.append(w_para_runs([
                    {"text": f"Q{q.get('num','')}  [{qmk} marks]:  ", "bold": True, "size": 22, "color": "1F3864"},
                    {"text": ans, "size": 22},
                ], space_after=80))
                # MCQ correct answer
                if stype=="mcq" and q.get("correct"):
                    parts.append(w_para_runs([
                        {"text": "   Correct: ", "bold": True, "size": 20, "color": "2F5496"},
                        {"text": q["correct"], "size": 20, "bold": True},
                        {"text": f"  —  {q.get('options',{}).get(q['correct'],'')}", "size": 20},
                    ], space_after=40, indent=360))
                if q.get("parts"):
                    for p in q["parts"]:
                        parts.append(w_para_runs([
                            {"text": f"   ({p.get('part','')})  ", "bold": True, "size": 20, "color": "2F5496"},
                            {"text": p.get("model_answer",""), "size": 20},
                            {"text": f"  [{p.get('marks','')} marks]", "size": 18, "color": "888888", "italic": True},
                        ], space_after=40, indent=360))
                parts.append(w_empty())

    return build_docx("".join(parts))

# ─────────────────────────────────────────────────────────────
# MCQ WORD BUILDER
# ─────────────────────────────────────────────────────────────
def build_mcq_docx(data: dict, show_answers: bool) -> bytes:
    parts = []
    subj = data.get("subject","")
    qs   = data.get("questions",[])

    parts.append(w_para("MULTIPLE CHOICE QUESTIONS", "Heading1",
                        color="1F3864", align="center", space_after=80))
    parts.append(w_para(subj, "Normal", italic=True, align="center",
                        size=22, color="555555", space_after=160))
    parts.append(w_hr())
    parts.append(w_empty())

    for q in qs:
        parts.append(w_para_runs([
            {"text": f"Q{q.get('num','')}.  ", "bold": True, "size": 24, "color": "1F3864"},
            {"text": q.get("question",""), "size": 22},
            {"text": f"  [{q.get('difficulty','')} | {q.get('topic','')}]",
             "size": 18, "color": "888888", "italic": True},
        ], space_after=80))
        for k, v in q.get("options",{}).items():
            marker = "✓ " if show_answers and k==q.get("correct","") else "   "
            col    = "1F7A3A" if show_answers and k==q.get("correct","") else "333333"
            parts.append(w_para_runs([
                {"text": f"  {k})  ", "bold": True, "size": 22, "color": "2F5496"},
                {"text": marker+v, "size": 22, "color": col},
            ], space_after=40))
        if show_answers and q.get("explanation"):
            parts.append(w_para_runs([
                {"text": "Explanation: ", "bold": True, "size": 20, "color": "2F5496"},
                {"text": q["explanation"], "size": 20, "italic": True},
            ], space_after=60, indent=360))
        parts.append(w_empty())

    return build_docx("".join(parts))

# ─────────────────────────────────────────────────────────────
# SUMMARY WORD BUILDER
# ─────────────────────────────────────────────────────────────
def build_summary_docx(data: dict) -> bytes:
    parts = []
    parts.append(w_para("ACADEMIC SUMMARY", "Heading1", color="1F3864",
                        align="center", space_after=80))
    parts.append(w_para(data.get("title",""), "Normal", bold=True,
                        align="center", size=26, space_after=60))
    parts.append(w_para(data.get("subject",""), "Normal", italic=True,
                        align="center", size=22, color="555555", space_after=160))
    parts.append(w_hr())

    parts.append(w_para("Overview", "Heading2", color="1F3864", space_after=80))
    parts.append(w_para(data.get("overview",""), "Normal", size=22, space_after=160))

    for sec in data.get("sections",[]):
        parts.append(w_para(sec.get("heading",""), "Heading2", color="1F3864", space_after=80))
        parts.append(w_para(sec.get("summary",""), "Normal", size=22, space_after=80))
        for kp in sec.get("key_points",[]):
            parts.append(w_para_runs([
                {"text": "▸  ", "bold": True, "color": "2F5496", "size": 22},
                {"text": kp, "size": 22},
            ], space_after=40))
        parts.append(w_empty())

    if data.get("key_terms"):
        parts.append(w_para("Key Terms & Definitions", "Heading2", color="1F3864", space_after=80))
        rows=[[kt.get("term",""),kt.get("definition",""),kt.get("example","")] for kt in data["key_terms"]]
        parts.append(w_table(["Term","Definition","Example"],rows,[2000,4500,2860]))

    if data.get("formulas"):
        parts.append(w_empty())
        parts.append(w_para("Key Formulas", "Heading2", color="1F3864", space_after=80))
        rows=[[f.get("name",""),f.get("formula",""),f.get("meaning",""),f.get("variables","")] for f in data["formulas"]]
        parts.append(w_table(["Name","Formula","Meaning","Variables"],rows,[2000,2200,2700,2500]))

    if data.get("key_conclusions"):
        parts.append(w_empty())
        parts.append(w_para("Key Conclusions", "Heading2", color="1F3864", space_after=80))
        for c in data["key_conclusions"]:
            parts.append(w_para_runs([
                {"text": "✓  ", "bold": True, "color": "1F7A3A", "size": 22},
                {"text": c, "size": 22},
            ], space_after=60))

    return build_docx("".join(parts))

# ─────────────────────────────────────────────────────────────
# PPTX BUILDER (pure zipfile + xml)
# ─────────────────────────────────────────────────────────────
def emu(i): return int(i*914400)
def pt(p):  return int(p*12700)
SLIDE_W=emu(13.33); SLIDE_H=emu(7.5)

def xe(s):
    return (str(s).replace("&","&amp;").replace("<","&lt;")
            .replace(">","&gt;").replace('"',"&quot;").replace("'","&apos;"))

def sp_rect(n,x,y,w,h,fill,line=None,lw=0):
    ln=(f'<a:ln w="{pt(lw)}"><a:solidFill><a:srgbClr val="{line}"/></a:solidFill></a:ln>'
        if line and lw>0 else '<a:ln><a:noFill/></a:ln>')
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="1" name="{n}"/>'
            f'<p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/>'
            f'<a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
            f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>{ln}</p:spPr></p:sp>')

def mk_para(text,sz,bold=False,italic=False,color="FFFFFF",
            align="l",font="Calibri",bullet="",spc=0):
    alg={"l":"l","c":"ctr","r":"r"}.get(align,"l")
    b=' b="1"' if bold else ""; i=' i="1"' if italic else ""
    bul=f'<a:buChar char="{xe(bullet)}"/>' if bullet else "<a:buNone/>"
    sa=f'<a:spcAft><a:spcPts val="{spc*100}"/></a:spcAft>' if spc else ""
    return (f'<a:p><a:pPr algn="{alg}" indent="0" marL="228600">{bul}{sa}</a:pPr>'
            f'<a:r><a:rPr lang="en-US" sz="{int(sz*100)}" dirty="0"{b}{i}>'
            f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
            f'<a:latin typeface="{font}"/></a:rPr>'
            f'<a:t>{xe(text)}</a:t></a:r></a:p>')

def txbox(n,x,y,w,h,paras):
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="2" name="{n}"/>'
            f'<p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/>'
            f'<a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>'
            f'<p:txBody><a:bodyPr wrap="square" lIns="45720" rIns="45720" tIns="45720" bIns="45720"/>'
            f'<a:lstStyle/>{"".join(paras)}</p:txBody></p:sp>')

def sld_xml(shapes,bg):
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
            f' xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"'
            f' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            f'<p:cSld><p:bg><p:bgPr>'
            f'<a:solidFill><a:srgbClr val="{bg}"/></a:solidFill>'
            f'<a:effectLst/></p:bgPr></p:bg><p:spTree>'
            f'<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
            f'<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{SLIDE_W}" cy="{SLIDE_H}"/>'
            f'<a:chOff x="0" y="0"/><a:chExt cx="{SLIDE_W}" cy="{SLIDE_H}"/></a:xfrm></p:grpSpPr>'
            f'{"".join(shapes)}</p:spTree></p:cSld></p:sld>')

def hdr(title,T):
    return [sp_rect("top",0,0,13.33,0.14,T["accent"]),
            sp_rect("tb",0.4,0.22,12.53,0.90,T["title_bg"]),
            txbox("tt",0.55,0.24,12.2,0.86,[mk_para(title,26,bold=True,color=T["text"],font="Georgia")])]

def bld_title(s,T):
    return sld_xml([sp_rect("bg",0,0,13.33,7.5,T["bg"]),sp_rect("bar",0,0,0.22,7.5,T["accent"]),
                    sp_rect("ln",0.5,7.0,4.5,0.06,T["accent"]),
                    txbox("ti",0.5,1.1,12.3,2.2,[mk_para(s.get("title",""),44,bold=True,color=T["text"],font="Georgia")]),
                    txbox("su",0.5,3.4,12.3,0.9,[mk_para(s.get("subtitle",""),22,color=T["sub"])]),
                    txbox("au",0.5,4.5,12.3,0.7,[mk_para(s.get("body",""),16,italic=True,color=T["sub"])])],T["bg"])

def bld_bullets(s,T):
    sh=hdr(s.get("title",""),T)
    ps=[mk_para(b,18,color=T["sub"],bullet="▸",spc=4) for b in s.get("bullets",[])]
    sh.append(txbox("bd",0.6,1.28,12.2,5.9,ps))
    return sld_xml(sh,T["bg"])

def bld_lecture(s,T):
    sh=hdr(s.get("title",""),T); ps=[]
    def sec(lbl,content,mono=False):
        if not content: return
        ps.append(mk_para(lbl,14,bold=True,color=T["accent"],spc=2))
        fn="Courier New" if mono else "Calibri"
        col=T["mono"] if mono else T["sub"]
        for line in str(content).split("\\n"):
            ps.append(mk_para(line.strip() or " ",15 if mono else 16,color=col,font=fn,spc=1))
        ps.append(mk_para(" ",5,color=T["bg"]))
    sec("📖  THEORY",s.get("theory",""))
    sec("📐  FORMULA",s.get("formula",""),mono=True)
    if s.get("where"): ps.append(mk_para("   "+s["where"],13,italic=True,color=T["sub"])); ps.append(mk_para(" ",5,color=T["bg"]))
    sec("✏️  EXAMPLE",s.get("example",""))
    sec("🔢  CALCULATION",s.get("calculation",""),mono=True)
    sh.append(txbox("bd",0.6,1.26,12.2,6.0,ps))
    return sld_xml(sh,T["bg"])

def bld_formula(s,T):
    sh=hdr(s.get("title",""),T)
    sh.append(sp_rect("fb",1.5,1.32,10.3,1.4,T["title_bg"],T["accent"],1.2))
    sh.append(txbox("fml",1.6,1.35,10.1,1.35,[mk_para(s.get("formula",""),30,bold=True,color=T["text"],font="Courier New",align="c")]))
    ps=[]
    if s.get("where"):
        ps.append(mk_para("Where:",15,bold=True,color=T["accent"]))
        for p in str(s["where"]).split(","):
            ps.append(mk_para(p.strip(),15,color=T["sub"],bullet="•"))
        ps.append(mk_para(" ",5,color=T["bg"]))
    if s.get("example"):
        ps.append(mk_para("Worked Example:",15,bold=True,color=T["accent"]))
        ps.append(mk_para(s["example"],15,color=T["sub"]))
        ps.append(mk_para(" ",5,color=T["bg"]))
    if s.get("calculation"):
        ps.append(mk_para("Solution:",15,bold=True,color=T["accent"]))
        for line in str(s["calculation"]).split("\\n"):
            ps.append(mk_para(line.strip() or " ",15,color=T["mono"],font="Courier New"))
    if ps: sh.append(txbox("rest",0.6,2.88,12.2,4.4,ps))
    return sld_xml(sh,T["bg"])

def bld_two_col(s,T):
    sh=hdr(s.get("title",""),T)
    sh+=[sp_rect("lc",0.35,1.1,6.1,6.0,T["box"],T["accent"],0.7),
         sp_rect("lh",0.35,1.1,6.1,0.5,T["accent"]),
         txbox("lt",0.45,1.12,5.9,0.46,[mk_para(s.get("left_title",""),14,bold=True,color="FFFFFF",align="c")])]
    sh.append(txbox("lb",0.45,1.7,5.9,5.2,[mk_para(b,15,color=T["sub"],bullet="▸",spc=3) for b in s.get("left_points",[])]))
    sh+=[sp_rect("rc",6.88,1.1,6.1,6.0,T["box"],T["accent"],0.7),
         sp_rect("rh",6.88,1.1,6.1,0.5,T["accent"]),
         txbox("rt",6.98,1.12,5.9,0.46,[mk_para(s.get("right_title",""),14,bold=True,color="FFFFFF",align="c")])]
    sh.append(txbox("rb",6.98,1.7,5.9,5.2,[mk_para(b,15,color=T["sub"],bullet="▸",spc=3) for b in s.get("right_points",[])]))
    return sld_xml(sh,T["bg"])

def bld_stat(s,T):
    sh=hdr(s.get("title",""),T); xpos=[0.4,4.65,8.9]; ww=3.9
    for i,si in enumerate(s.get("stats",[])[:3]):
        xp=xpos[i]
        sh+=[sp_rect(f"sc{i}",xp,1.3,ww,3.6,T["box"],T["accent"],0.8),
             sp_rect(f"sl{i}",xp,1.3,ww,0.12,T["accent"]),
             txbox(f"sv{i}",xp+0.1,1.55,ww-0.2,1.5,[mk_para(si.get("value",""),52,bold=True,color=T["accent"],font="Georgia",align="c")]),
             txbox(f"slb{i}",xp+0.1,3.1,ww-0.2,0.6,[mk_para(si.get("label",""),14,color=T["sub"],align="c")])]
    if s.get("body"): sh.append(txbox("bd",0.5,5.1,12.3,1.1,[mk_para(s["body"],14,italic=True,color=T["sub"])]))
    return sld_xml(sh,T["bg"])

def bld_table(s,T):
    sh=hdr(s.get("title",""),T); ps=[]
    headers=s.get("headers",[]); rows=s.get("rows",[])
    if headers:
        ps.append(mk_para("  |  ".join(str(h)[:18] for h in headers),14,bold=True,color=T["accent"],font="Courier New"))
        ps.append(mk_para("─"*60,10,color=T["sub"],font="Courier New"))
        for row in rows[:14]:
            cells=[str(v)[:18] for v in row[:len(headers)]]
            while len(cells)<len(headers): cells.append("")
            ps.append(mk_para("  |  ".join(cells),13,color=T["sub"],font="Courier New",spc=2))
    else: ps.append(mk_para("No table data.",16,color=T["sub"]))
    sh.append(txbox("tbl",0.5,1.3,12.3,5.9,ps))
    return sld_xml(sh,T["bg"])

def bld_conclusion(s,T):
    sh=hdr(s.get("title","Key Takeaways"),T)
    sh+=[sp_rect("cb",0.4,1.2,12.53,5.9,T["box"],T["accent"],0.8),sp_rect("bb",0,7.36,13.33,0.14,T["accent"])]
    ps=[mk_para(b,18,color=T["sub"],bullet="✓",spc=6) for b in s.get("bullets",[])]
    sh.append(txbox("bd",0.7,1.4,12.0,5.7,ps))
    return sld_xml(sh,T["bg"])

def build_pptx_slide(s,T):
    t=s.get("type","bullets")
    if   t=="title":        return bld_title(s,T)
    elif t=="lecture":      return bld_lecture(s,T)
    elif t=="formula":      return bld_formula(s,T)
    elif t=="two_col":      return bld_two_col(s,T)
    elif t=="stat_callout": return bld_stat(s,T)
    elif t=="table":        return bld_table(s,T)
    elif t=="conclusion":   return bld_conclusion(s,T)
    else:                   return bld_bullets(s,T)

def assemble_pptx(slides_xml_list):
    buf=io.BytesIO()
    with zipfile.ZipFile(buf,"w",zipfile.ZIP_DEFLATED) as z:
        ct_s="\n".join(f'<Override PartName="/ppt/slides/slide{i+1}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>' for i in range(len(slides_xml_list)))
        z.writestr("[Content_Types].xml",f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/><Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/><Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/><Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>{ct_s}</Types>')
        z.writestr("_rels/.rels",'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/></Relationships>')
        z.writestr("docProps/app.xml",'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"><Application>Kaabe</Application></Properties>')
        z.writestr("ppt/theme/theme1.xml",'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="T"><a:themeElements><a:clrScheme name="O"><a:dk1><a:sysClr lastClr="000000" val="windowText"/></a:dk1><a:lt1><a:sysClr lastClr="FFFFFF" val="window"/></a:lt1><a:dk2><a:srgbClr val="44546A"/></a:dk2><a:lt2><a:srgbClr val="E7E6E6"/></a:lt2><a:accent1><a:srgbClr val="4472C4"/></a:accent1><a:accent2><a:srgbClr val="ED7D31"/></a:accent2><a:accent3><a:srgbClr val="A9D18E"/></a:accent3><a:accent4><a:srgbClr val="FFC000"/></a:accent4><a:accent5><a:srgbClr val="5B9BD5"/></a:accent5><a:accent6><a:srgbClr val="70AD47"/></a:accent6><a:hlink><a:srgbClr val="0563C1"/></a:hlink><a:folHlink><a:srgbClr val="954F72"/></a:folHlink></a:clrScheme><a:fontScheme name="O"><a:majorFont><a:latin typeface="Calibri Light"/><a:ea typeface=""/><a:cs typeface=""/></a:majorFont><a:minorFont><a:latin typeface="Calibri"/><a:ea typeface=""/><a:cs typeface=""/></a:minorFont></a:fontScheme><a:fmtScheme name="O"><a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst><a:lnStyleLst><a:ln w="6350"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln><a:ln w="12700"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln><a:ln w="19050"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst><a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst><a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst></a:fmtScheme></a:themeElements></a:theme>')
        z.writestr("ppt/slideMasters/slideMaster1.xml",'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><p:cSld><p:bg><p:bgRef idx="1001"><a:schemeClr val="bg1"/></p:bgRef></p:bg><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld><p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/><p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst><p:txStyles><p:titleStyle><a:lstStyle/></p:titleStyle><p:bodyStyle><a:lstStyle/></p:bodyStyle><p:otherStyle><a:lstStyle/></p:otherStyle></p:txStyles></p:sldMaster>')
        z.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels",'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/></Relationships>')
        z.writestr("ppt/slideLayouts/slideLayout1.xml",'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" type="blank"><p:cSld name="Blank"><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>')
        z.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels",'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/></Relationships>')
        sld_ids="\n".join(f'<p:sldId id="{256+i}" r:id="rId{i+3}"/>' for i in range(len(slides_xml_list)))
        prs_rels="\n".join(f'<Relationship Id="rId{i+3}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i+1}.xml"/>' for i in range(len(slides_xml_list)))
        for i,xml in enumerate(slides_xml_list):
            z.writestr(f"ppt/slides/slide{i+1}.xml",xml)
            z.writestr(f"ppt/slides/_rels/slide{i+1}.xml.rels",'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/></Relationships>')
        z.writestr("ppt/presentation.xml",f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" saveSubsetFonts="1"><p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst><p:sldIdLst>{sld_ids}</p:sldIdLst><p:sldSz cx="{SLIDE_W}" cy="{SLIDE_H}" type="custom"/><p:notesSz cx="{emu(7.5)}" cy="{emu(10)}"/></p:presentation>')
        z.writestr("ppt/_rels/presentation.xml.rels",f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/>{prs_rels}</Relationships>')
    buf.seek(0); return buf.read()

# ─────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────
for k,v in {"tool":"slides","pdf_b64":None,"filename":"",
            "chat":[],"fc_idx":0,"fc_show":False,
            "mcq_data":None,"summary_data":None,
            "exam_data":None,"fc_data":None}.items():
    if k not in st.session_state: st.session_state[k]=v

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔑 Gemini API Key")
    st.markdown('<div style="background:#0a1220;border:1px solid #1e3060;border-radius:8px;padding:.8rem;font-size:.77rem;color:#5a7099;line-height:1.7;margin-bottom:.8rem">Free key at <a href="https://aistudio.google.com/app/apikey" target="_blank" style="color:#3a7bd5">aistudio.google.com</a><br>No credit card needed</div>',unsafe_allow_html=True)
    api_key = st.text_input("","",type="password",placeholder="AIzaSy...",label_visibility="collapsed")
    st.markdown("---")
    st.markdown("### 📄 Upload PDF")
    uploaded = st.file_uploader("",type=["pdf"],label_visibility="collapsed")
    if uploaded:
        b64=base64.standard_b64encode(uploaded.getvalue()).decode()
        st.session_state.pdf_b64=b64; st.session_state.filename=uploaded.name
        kb=len(uploaded.getvalue())//1024
        st.markdown(f'<div style="background:#0a1e0a;border:1px solid #1a4a1a;border-radius:8px;padding:.6rem .9rem;font-size:.8rem;color:#4ade80">✓ {uploaded.name}<br><span style="color:#5a7099">{kb} KB</span></div>',unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 🎨 Slide Theme")
    sel_theme=st.selectbox("",list(THEMES.keys()),label_visibility="collapsed")
    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    num_slides  = st.slider("Slides",        6, 20, 10)
    num_mcq     = st.slider("MCQ questions", 5, 40, 15)
    num_fc      = st.slider("Flashcards",    5, 30, 12)
    course_name = st.text_input("Course name",placeholder="e.g. Engineering Mathematics")
    institution = st.text_input("Institution",placeholder="e.g. University of Somalia")
    lecturer    = st.text_input("Lecturer name",placeholder="e.g. Dr. Ahmed")
    focus_topic = st.text_input("Focus topic (optional)",placeholder="e.g. integration, forces")

# ─────────────────────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────────────────────
fn=st.session_state.filename
st.markdown(f"""
<div class="hero">
  <div class="hero-icon">🎓</div>
  <div>
    <h1>🎓 Kaabe</h1>
    <p>Your AI-powered Academic Platform for Lecturers · Somalia & Beyond</p>
  </div>
  <div style="margin-left:auto">
    <span class="stat-pill">📄 <b>{(fn[:22]+"…") if len(fn)>24 else (fn or "No PDF")}</b></span>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# TOOL BAR
# ─────────────────────────────────────────────────────────────
TOOLS=[("slides","📊 Lecture Slides"),("mcq","❓ MCQ"),
       ("exam","📝 Exam Paper"),("summary","📋 Summary"),
       ("flashcards","🃏 Flashcards"),("qa","💬 AI Tutor")]
cols=st.columns(len(TOOLS))
for i,(tid,tlabel) in enumerate(TOOLS):
    with cols[i]:
        if st.button(tlabel,key=f"t_{tid}",use_container_width=True,
                     type="primary" if st.session_state.tool==tid else "secondary"):
            st.session_state.tool=tid; st.rerun()

st.markdown("---")

def check_ready():
    if not api_key:
        st.warning("🔑 Enter your Gemini API key in the sidebar.")
        return False
    if not st.session_state.pdf_b64:
        st.warning("📄 Upload a PDF in the sidebar.")
        return False
    return True

def sp(se,pe,msg,pct):
    se.markdown(f'<div style="text-align:center;font-size:.88rem;color:#5a7099;margin:.4rem 0">{msg}</div>',unsafe_allow_html=True)
    pe.markdown(f'<div class="progress-bar"><div class="progress-fill" style="width:{pct}%"></div></div>',unsafe_allow_html=True)

tool=st.session_state.tool

# ═════════════════════════════════════════════════════════════
# 1. LECTURE SLIDES
# ═════════════════════════════════════════════════════════════
if tool=="slides":
    st.markdown("## 📊 Lecture Slides Generator")
    c1,c2=st.columns([2,1])
    with c1:
        pres_style=st.selectbox("Style",["University Lecture","Research Paper Summary","Technical Report","Business Analysis"])
        incl_f=st.checkbox("Extract formulas & equations",value=True)
        incl_e=st.checkbox("Include worked examples",value=True)
        incl_t=st.checkbox("Extract tables & data",value=True)
    with c2:
        st.markdown('<div style="background:#0a1220;border:1px solid #1a2a45;border-radius:8px;padding:1rem;font-size:.8rem;color:#5a7099"><b style="color:#fff">Slide types generated:</b><br>📖 Theory explanation<br>📐 Formula + variables<br>✏️ Worked example<br>🔢 Step-by-step calculation<br>📊 Data tables<br>🔄 Two-column comparison<br>✓ Conclusion & takeaways</div>',unsafe_allow_html=True)

    if st.button("✨ Generate Lecture Slides",type="primary",use_container_width=True):
        if not check_ready(): st.stop()
        se=st.empty(); pe=st.empty()
        try:
            sp(se,pe,"🧠 AI reading PDF as university professor…",20)
            fi=f"Focus especially on: {focus_topic}." if focus_topic else ""
            ci=f"Course: {course_name}." if course_name else ""
            prompt=f"""You are a brilliant university professor. Read this entire PDF deeply.
Create a {num_slides}-slide {pres_style} presentation. {ci} {fi}
Use ONLY real content. Never invent. Act as a lecturer.
For every formula: exact formula, define variables, give worked numerical example with steps.
{"Extract every formula exactly." if incl_f else ""}
{"Include worked examples with step-by-step calculation." if incl_e else ""}
{"Extract all tables with exact data." if incl_t else ""}
NEVER say "from the document" or "the document says" — just state facts directly.
CRITICAL JSON: Return raw JSON only. No fences. Strings on ONE line. Use \\n for line breaks. No trailing commas.
{{"title":"...","subtitle":"...","author":"...","slides":[
{{"slide_num":1,"type":"title","title":"...","subtitle":"...","body":"Author · Year"}},
{{"slide_num":2,"type":"bullets","title":"...","bullets":["fact 1","fact 2","fact 3","fact 4","fact 5"]}},
{{"slide_num":3,"type":"lecture","title":"Concept","theory":"explanation","formula":"y=mx+c","where":"y=output, m=slope, x=input, c=intercept","example":"Given m=3 c=2 x=4","calculation":"y=3*4+2\\ny=14"}},
{{"slide_num":4,"type":"formula","title":"Formula Name","formula":"E=mc^2","where":"E=energy J, m=mass kg, c=3e8 m/s","example":"Find energy for 0.5 kg","calculation":"E=0.5*(3e8)^2\\nE=4.5e16 J"}},
{{"slide_num":5,"type":"two_col","title":"...","left_title":"...","left_points":["a","b","c"],"right_title":"...","right_points":["x","y","z"]}},
{{"slide_num":6,"type":"stat_callout","title":"...","stats":[{{"value":"87%","label":"name","note":"context"}},{{"value":"3.14","label":"name","note":"ctx"}},{{"value":"2.4M","label":"name","note":"ctx"}}],"body":"context"}},
{{"slide_num":7,"type":"table","title":"...","headers":["Col1","Col2","Col3"],"rows":[["a","b","c"],["d","e","f"]]}},
{{"slide_num":8,"type":"conclusion","title":"Key Takeaways","bullets":["finding 1","finding 2","formula learned","application","next steps"]}}
]}}
Generate exactly {num_slides} slides."""
            raw=call_gemini(api_key,prompt,st.session_state.pdf_b64,8192)
            sp(se,pe,"🔧 Parsing JSON…",50)
            plan=safe_parse(raw)
            sp(se,pe,"🎨 Building slides…",65)
            T=THEMES[sel_theme]; xmls=[]
            slides=plan.get("slides",[])
            for i,s in enumerate(slides):
                sp(se,pe,f"🖼️ Slide {i+1}/{len(slides)}…",65+int(i/max(len(slides),1)*25))
                xmls.append(build_pptx_slide(s,T))
            sp(se,pe,"💾 Assembling PPTX…",93)
            pptx=assemble_pptx(xmls)
            se.empty(); pe.empty()
            st.success(f"✅ {len(xmls)} slides ready!")
            safe=re.sub(r"[^a-zA-Z0-9_\- ]","",plan.get("title","slides"))[:40].strip().replace(" ","_") or "slides"
            st.download_button("⬇️ Download Slides (.pptx)",data=pptx,file_name=f"{safe}.pptx",
                               mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                               use_container_width=True)
        except (ValueError,Exception) as e:
            se.empty(); pe.empty(); st.error(str(e))

# ═════════════════════════════════════════════════════════════
# 2. MCQ
# ═════════════════════════════════════════════════════════════
elif tool=="mcq":
    st.markdown("## ❓ MCQ Generator")
    c1,c2,c3=st.columns(3)
    with c1: mcq_diff=st.selectbox("Difficulty",["Easy","Medium","Hard","Mixed"])
    with c2: mcq_type=st.selectbox("Type",["Conceptual","Calculation-based","Mixed"])
    with c3: show_ans=st.checkbox("Show answers & explanations",value=True)

    if st.button("🎯 Generate MCQ",type="primary",use_container_width=True):
        if not check_ready(): st.stop()
        se=st.empty(); pe=st.empty()
        try:
            sp(se,pe,"🧠 Generating MCQ questions…",30)
            fi=f"Focus on: {focus_topic}." if focus_topic else ""
            prompt=f"""You are a university examiner. Create {num_mcq} multiple choice questions. Difficulty: {mcq_diff}. Type: {mcq_type}. {fi}
Include calculation-based questions with real numbers where possible.
NEVER say "from the document" or "according to the text" — write questions as standalone academic questions.
Each question must have 4 options (A,B,C,D) with exactly one correct answer.
Return raw JSON only, no fences:
{{"subject":"subject name","questions":[
{{"num":1,"question":"Question text?","options":{{"A":"option","B":"option","C":"option","D":"option"}},"correct":"A","explanation":"Why A is correct. Include calculation if applicable.","difficulty":"Easy","topic":"topic"}}
]}}
Generate exactly {num_mcq} questions covering all major topics."""
            raw=call_gemini(api_key,prompt,st.session_state.pdf_b64,8192)
            sp(se,pe,"✅ Parsing…",80)
            data=safe_parse(raw); st.session_state.mcq_data=data
            se.empty(); pe.empty()
        except (ValueError,Exception) as e:
            se.empty(); pe.empty(); st.error(str(e))

    if st.session_state.mcq_data:
        data=st.session_state.mcq_data; qs=data.get("questions",[]); subj=data.get("subject","")
        st.markdown(f'<div style="margin-bottom:1rem"><span class="stat-pill">📚 <b>{subj}</b></span><span class="stat-pill">❓ <b>{len(qs)}</b> questions</span></div>',unsafe_allow_html=True)
        # Word download
        docx=build_mcq_docx(data,show_ans)
        st.download_button("⬇️ Download MCQ (.docx)",data=docx,file_name="mcq.docx",
                           mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                           use_container_width=True)
        for q in qs:
            corr=q.get("correct","")
            st.markdown(f'<div class="mcq-card"><div style="display:flex;justify-content:space-between;margin-bottom:.4rem"><span style="font-size:.7rem;color:#3a7bd5;font-weight:700">Q{q.get("num","")} · {q.get("topic","")}</span><span style="font-size:.7rem;background:#0f2240;border:1px solid #1e3a6a;border-radius:20px;padding:1px 8px;color:#7ab3d4">{q.get("difficulty","")}</span></div><div class="mcq-q">{q.get("question","")}</div>',unsafe_allow_html=True)
            for k,v in q.get("options",{}).items():
                cls="correct" if show_ans and k==corr else ""
                st.markdown(f'<div class="mcq-opt {cls}"><span class="mcq-letter">{k}</span>{v}</div>',unsafe_allow_html=True)
            if show_ans and q.get("explanation"):
                st.markdown(f'<div class="mcq-explain">💡 {q["explanation"]}</div>',unsafe_allow_html=True)
            st.markdown('</div>',unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════
# 3. EXAM PAPER  ← FULLY REBUILT
# ═════════════════════════════════════════════════════════════
elif tool=="exam":
    st.markdown("## 📝 Exam Paper Generator")

    # ── Exam structure builder ────────────────────────────
    st.markdown('<div class="section-card"><div class="section-title">🏗️ Build Your Exam Structure</div>',unsafe_allow_html=True)
    st.markdown("Add sections and choose the question type for each. The AI will create questions matching your exact structure.")
    st.markdown('</div>',unsafe_allow_html=True)

    c1,c2,c3,c4=st.columns(4)
    with c1: exam_dur  = st.selectbox("Duration",["30 minutes","1 hour","1.5 hours","2 hours","2.5 hours","3 hours"])
    with c2: total_mks = st.selectbox("Total marks",["25","50","60","80","100","120"])
    with c3: exam_diff = st.selectbox("Difficulty",["Easy","Medium","Hard","Mixed"])
    with c4: incl_ms   = st.checkbox("Include mark scheme",value=True)

    st.markdown("### 📋 Exam Sections")
    st.markdown('<div style="font-size:.82rem;color:#5a7099;margin-bottom:.8rem">Define each section of your exam. Each section can have a different question type.</div>',unsafe_allow_html=True)

    # Section builder — stored in session state
    if "exam_sections" not in st.session_state:
        st.session_state.exam_sections = [
            {"name":"Section A","type":"mcq",            "marks":20,"num_q":10,"desc":"Multiple choice questions"},
            {"name":"Section B","type":"short_answer",   "marks":30,"num_q":5, "desc":"Short answer questions"},
            {"name":"Section C","type":"long_answer",    "marks":30,"num_q":3, "desc":"Long answer / essay questions"},
        ]

    SECTION_TYPES = {
        "mcq":           "MCQ (Multiple Choice)",
        "true_false":    "True / False",
        "short_answer":  "Short Answer",
        "long_answer":   "Long Answer / Essay",
        "calculation":   "Calculation / Problem Solving",
        "fill_blank":    "Fill in the Blank",
        "matching":      "Matching",
        "case_study":    "Case Study",
    }

    updated_sections=[]
    for i,sec in enumerate(st.session_state.exam_sections):
        with st.expander(f"Section {i+1} — {sec['name']} ({sec['type'].replace('_',' ').title()})",expanded=True):
            rc1,rc2,rc3,rc4,rc5=st.columns([2,2,1,1,1])
            with rc1: sec_name  = st.text_input("Section name",sec["name"],key=f"sn{i}")
            with rc2: sec_type  = st.selectbox("Question type",list(SECTION_TYPES.keys()),
                                                index=list(SECTION_TYPES.keys()).index(sec["type"]) if sec["type"] in SECTION_TYPES else 0,
                                                format_func=lambda x:SECTION_TYPES[x],key=f"st{i}")
            with rc3: sec_marks = st.number_input("Marks",1,200,sec["marks"],key=f"sm{i}")
            with rc4: sec_numq  = st.number_input("Questions",1,30,sec["num_q"],key=f"sq{i}")
            with rc5:
                st.markdown("<div style='height:28px'></div>",unsafe_allow_html=True)
                if st.button("🗑️",key=f"del{i}",help="Remove section"):
                    st.session_state.exam_sections.pop(i); st.rerun()
            sec_desc=st.text_input("Section instructions (optional)",sec.get("desc",""),key=f"sd{i}")
            updated_sections.append({"name":sec_name,"type":sec_type,"marks":sec_marks,
                                     "num_q":sec_numq,"desc":sec_desc})

    st.session_state.exam_sections=updated_sections

    ac1,ac2=st.columns(2)
    with ac1:
        if st.button("➕ Add Section",use_container_width=True):
            n=len(st.session_state.exam_sections)+1
            st.session_state.exam_sections.append({"name":f"Section {chr(64+n)}","type":"short_answer","marks":20,"num_q":4,"desc":""})
            st.rerun()
    with ac2:
        total_configured=sum(s["marks"] for s in st.session_state.exam_sections)
        st.markdown(f'<div style="background:#0a1220;border:1px solid #1a2a45;border-radius:8px;padding:.6rem 1rem;font-size:.85rem;color:#8899bb;text-align:center">Total configured: <b style="color:#60a5fa">{total_configured}</b> / <b style="color:#fff">{total_mks}</b> marks</div>',unsafe_allow_html=True)

    st.markdown("---")
    if st.button("📝 Generate Exam Paper",type="primary",use_container_width=True):
        if not check_ready(): st.stop()
        se=st.empty(); pe=st.empty()
        try:
            sp(se,pe,"🧠 AI generating exam paper…",25)
            ci=f"Course: {course_name}." if course_name else ""
            ii=f"Institution: {institution}." if institution else ""
            li=f"Lecturer: {lecturer}." if lecturer else ""
            fi=f"Focus on: {focus_topic}." if focus_topic else ""

            sections_spec=""
            for sec in st.session_state.exam_sections:
                sections_spec+=f'\n  - Section "{sec["name"]}": {sec["num_q"]} {SECTION_TYPES.get(sec["type"],sec["type"])} questions, {sec["marks"]} marks total. Instructions: {sec["desc"] or "Standard instructions."}'

            # Build section JSON template
            def sec_template(sec):
                t=sec["type"]; n=sec["num_q"]; mk=sec["marks"]; qmk=round(mk/max(n,1))
                if t=="mcq":
                    return f'{{"name":"{sec["name"]}","type":"mcq","description":"{SECTION_TYPES[t]}","marks":{mk},"instructions":"{sec["desc"] or "Circle the correct answer."}","questions":[{{"num":"1","text":"Question text?","marks":{qmk},"answer_lines":1,"options":{{"A":"option","B":"option","C":"option","D":"option"}},"correct":"A","model_answer":"A — explanation"}}]}}'
                elif t=="true_false":
                    return f'{{"name":"{sec["name"]}","type":"true_false","description":"{SECTION_TYPES[t]}","marks":{mk},"instructions":"{sec["desc"] or "Write True or False."}","questions":[{{"num":"1","text":"Statement to evaluate.","marks":{qmk},"answer_lines":1,"model_answer":"True/False — explanation"}}]}}'
                elif t=="fill_blank":
                    return f'{{"name":"{sec["name"]}","type":"fill_blank","description":"{SECTION_TYPES[t]}","marks":{mk},"instructions":"{sec["desc"] or "Fill in the blank."}","questions":[{{"num":"1","text":"Sentence with _______ blank.","marks":{qmk},"answer_lines":1,"model_answer":"correct word/phrase"}}]}}'
                elif t=="short_answer":
                    return f'{{"name":"{sec["name"]}","type":"short_answer","description":"{SECTION_TYPES[t]}","marks":{mk},"instructions":"{sec["desc"] or "Answer clearly and concisely."}","questions":[{{"num":"1","text":"Short question requiring a direct answer.","marks":{qmk},"answer_lines":4,"model_answer":"Clear model answer with key points"}}]}}'
                elif t=="long_answer":
                    return f'{{"name":"{sec["name"]}","type":"long_answer","description":"{SECTION_TYPES[t]}","marks":{mk},"instructions":"{sec["desc"] or "Answer in full. Show all reasoning."}","questions":[{{"num":"1","text":"Full question here.","marks":{qmk},"answer_lines":12,"parts":[{{"part":"a","text":"Part (a) text","marks":4,"answer_lines":4,"model_answer":"model"}},{{"part":"b","text":"Part (b) text","marks":4,"answer_lines":4,"model_answer":"model"}},{{"part":"c","text":"Part (c) text","marks":{qmk-8},"answer_lines":4,"model_answer":"model"}}],"model_answer":"Full model answer"}}]}}'
                elif t=="calculation":
                    return f'{{"name":"{sec["name"]}","type":"calculation","description":"{SECTION_TYPES[t]}","marks":{mk},"instructions":"{sec["desc"] or "Show all working. State formulae used."}","questions":[{{"num":"1","text":"Numerical problem requiring calculation.","marks":{qmk},"answer_lines":10,"parts":[{{"part":"a","text":"Part (a) — setup (3 marks)","marks":3,"answer_lines":4,"model_answer":"step 1: ... step 2: ..."}},{{"part":"b","text":"Part (b) — solve (4 marks)","marks":4,"answer_lines":6,"model_answer":"step by step calculation"}},{{"part":"c","text":"Part (c) — interpret ({qmk-7} marks)","marks":{qmk-7},"answer_lines":3,"model_answer":"interpretation"}}],"model_answer":"Full solution"}}]}}'
                elif t=="matching":
                    return f'{{"name":"{sec["name"]}","type":"matching","description":"{SECTION_TYPES[t]}","marks":{mk},"instructions":"{sec["desc"] or "Match column A with column B."}","questions":[{{"num":"1","text":"Match each term in Column A with the correct definition in Column B.","marks":{mk},"answer_lines":2,"model_answer":"1-B, 2-D, 3-A, 4-C (etc.)"}}]}}'
                elif t=="case_study":
                    return f'{{"name":"{sec["name"]}","type":"case_study","description":"{SECTION_TYPES[t]}","marks":{mk},"instructions":"{sec["desc"] or "Read the case carefully and answer all parts."}","questions":[{{"num":"1","text":"[Case study scenario here]. Based on the above case, answer the following:","marks":{mk},"answer_lines":2,"parts":[{{"part":"a","text":"Analysis question (a)","marks":round(mk/3),"answer_lines":6,"model_answer":"analysis model"}},{{"part":"b","text":"Evaluation question (b)","marks":round(mk/3),"answer_lines":6,"model_answer":"evaluation model"}},{{"part":"c","text":"Application question (c)","marks":mk-2*round(mk/3),"answer_lines":6,"model_answer":"application model"}}],"model_answer":"Overall case discussion"}}]}}'
                else:
                    return f'{{"name":"{sec["name"]}","type":"{t}","description":"{SECTION_TYPES.get(t,t)}","marks":{mk},"instructions":"{sec["desc"] or "Answer all questions."}","questions":[{{"num":"1","text":"Question text.","marks":{qmk},"answer_lines":6,"model_answer":"model answer"}}]}}'

            sections_json_template="["+",\n".join(sec_template(s) for s in st.session_state.exam_sections)+"]"

            prompt=f"""You are a chief university examiner. Read this PDF and create a complete, professional exam paper.
{ci} {ii} {li} Duration: {exam_dur}. Total marks: {total_mks}. Difficulty: {exam_diff}. {fi}

EXAM STRUCTURE (you MUST follow exactly):
{sections_spec}

CRITICAL RULES:
- Write all questions as standalone academic questions — NEVER say "from the document", "according to the text", "the document states", "as mentioned in" or any reference to any document.
- Write questions as if you are an examiner testing student knowledge directly.
- Questions must test understanding, application and analysis — not just recall.
- Include real numbers and data in calculation questions.
- For MCQ: include one clearly correct answer and three plausible distractors.
- For case study: write a realistic mini-scenario then ask analytical questions.
- For matching: provide two columns of {min(8,5)} items each.
- Model answers must be complete, detailed, and include all marking points.

Return raw JSON only, no fences, no explanation:
{{
  "title": "exam title",
  "institution": "{institution or 'University'}",
  "course": "{course_name or 'Course Name'}",
  "lecturer": "{lecturer or ''}",
  "duration": "{exam_dur}",
  "total_marks": {total_mks},
  "date": "________________",
  "instructions": ["Read all questions carefully before answering","Answer ALL questions unless instructed otherwise","Show all working for calculation questions","Write legibly in the space provided","Mobile phones and electronic devices are not permitted"],
  "sections": {sections_json_template}
}}

Replace all template questions with REAL academic questions based on the content of this PDF.
Generate exactly {sum(s['num_q'] for s in st.session_state.exam_sections)} questions total across all sections."""

            raw=call_gemini(api_key,prompt,st.session_state.pdf_b64,8192)
            sp(se,pe,"✅ Parsing exam paper…",75)
            data=safe_parse(raw); st.session_state.exam_data=data
            se.empty(); pe.empty()
        except (ValueError,Exception) as e:
            se.empty(); pe.empty(); st.error(str(e))
            import traceback; st.code(traceback.format_exc())

    if st.session_state.exam_data:
        data=st.session_state.exam_data

        # ── Word download ─────────────────────────────────
        docx_bytes=build_exam_docx(data,incl_ms)
        st.success("✅ Exam paper ready!")
        safe=re.sub(r"[^a-zA-Z0-9_\- ]","",data.get("title","exam"))[:40].strip().replace(" ","_") or "exam"
        st.download_button(
            "⬇️ Download Exam Paper (.docx)",
            data=docx_bytes,
            file_name=f"{safe}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )

        # ── Preview ───────────────────────────────────────
        st.markdown(f"""
        <div class="exam-preview">
          <div style="text-align:center;border-bottom:2px solid #1e3a6a;padding-bottom:.8rem;margin-bottom:.8rem">
            <div style="font-size:.85rem;font-weight:700;color:#60a5fa">{data.get('institution','')}</div>
            <div style="font-size:1.2rem;font-weight:700;color:#fff;margin:.3rem 0">{data.get('title','')}</div>
            <div style="font-size:.82rem;color:#8899bb">{data.get('course','')} &nbsp;·&nbsp; {data.get('duration','')} &nbsp;·&nbsp; {data.get('total_marks','')} marks</div>
          </div>
        """,unsafe_allow_html=True)

        st.markdown("**Instructions:**")
        for inst in data.get("instructions",[]): st.markdown(f"- {inst}")
        st.markdown("---")

        for sec in data.get("sections",[]):
            stype=sec.get("type","short_answer")
            st.markdown(f'<div class="exam-sec-hdr">{sec.get("name","")}  —  {sec.get("description","")}  ({sec.get("marks","")} marks)</div>',unsafe_allow_html=True)
            if sec.get("instructions"):
                st.markdown(f'<div style="font-size:.8rem;color:#5a7099;font-style:italic;margin-bottom:.5rem">{sec["instructions"]}</div>',unsafe_allow_html=True)

            for q in sec.get("questions",[]):
                st.markdown(f'<div class="exam-q"><span class="exam-qnum">Q{q.get("num","")}.&nbsp;</span>{q.get("text","")}<span class="marks-tag">[{q.get("marks","")} marks]</span></div>',unsafe_allow_html=True)
                if stype=="mcq" and q.get("options"):
                    for k,v in q.get("options",{}).items():
                        st.markdown(f'<div style="padding:.2rem .5rem .2rem 2rem;font-size:.84rem;color:#8899bb">{k}) {v}</div>',unsafe_allow_html=True)
                elif q.get("parts"):
                    for p in q.get("parts",[]):
                        st.markdown(f'<div class="exam-q" style="padding-left:2rem"><span class="exam-qnum">({p.get("part","")})&nbsp;</span>{p.get("text","")}<span class="marks-tag">[{p.get("marks","")} marks]</span></div>',unsafe_allow_html=True)
                        for _ in range(min(p.get("answer_lines",3),5)):
                            st.markdown('<div class="ans-line"></div>',unsafe_allow_html=True)

        st.markdown("</div>",unsafe_allow_html=True)

        if incl_ms:
            with st.expander("📋 Mark Scheme"):
                for sec in data.get("sections",[]):
                    st.markdown(f"**{sec.get('name','')}**")
                    stype=sec.get("type","")
                    for q in sec.get("questions",[]):
                        st.markdown(f"**Q{q.get('num','')}** [{q.get('marks','')} marks]: {q.get('model_answer','')}")
                        if stype=="mcq" and q.get("correct"):
                            opts=q.get("options",{})
                            st.markdown(f"  ✓ **{q['correct']}**: {opts.get(q['correct'],'')}")
                        if q.get("parts"):
                            for p in q["parts"]:
                                st.markdown(f"  **({p.get('part','')})** [{p.get('marks','')} mk]: {p.get('model_answer','')}")

# ═════════════════════════════════════════════════════════════
# 4. SUMMARY
# ═════════════════════════════════════════════════════════════
elif tool=="summary":
    st.markdown("## 📋 Smart Academic Summary")
    c1,c2=st.columns(2)
    with c1:
        sum_depth=st.selectbox("Depth",["Quick overview","Standard","Detailed"])
        incl_kw=st.checkbox("Key terms & definitions",value=True)
    with c2:
        incl_fo=st.checkbox("Extract all formulas",value=True)
        incl_mm=st.checkbox("Mind map structure",value=True)

    if st.button("📋 Generate Summary",type="primary",use_container_width=True):
        if not check_ready(): st.stop()
        se=st.empty(); pe=st.empty()
        try:
            sp(se,pe,"🧠 AI summarizing…",30)
            fi=f"Focus on: {focus_topic}." if focus_topic else ""
            prompt=f"""Create a {sum_depth} academic summary of this PDF. {fi}
NEVER say "from the document" — state all facts directly.
Return raw JSON only, no fences:
{{"title":"...","subject":"...","overview":"2-3 sentence overview","sections":[{{"heading":"...","summary":"3-5 sentences","key_points":["point 1","point 2","point 3"]}}],"key_terms":[{{"term":"...","definition":"...","example":"..."}}],"formulas":[{{"name":"...","formula":"...","meaning":"...","variables":"..."}}],"mind_map":{{"center":"main topic","branches":[{{"topic":"branch","subtopics":["sub1","sub2","sub3"]}}]}},"key_conclusions":["conclusion 1","conclusion 2","conclusion 3","conclusion 4"]}}"""
            raw=call_gemini(api_key,prompt,st.session_state.pdf_b64,8192)
            sp(se,pe,"✅ Parsing…",80)
            data=safe_parse(raw); st.session_state.summary_data=data
            se.empty(); pe.empty()
        except (ValueError,Exception) as e:
            se.empty(); pe.empty(); st.error(str(e))

    if st.session_state.summary_data:
        data=st.session_state.summary_data
        docx=build_summary_docx(data)
        st.download_button("⬇️ Download Summary (.docx)",data=docx,file_name="summary.docx",
                           mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                           use_container_width=True)
        st.markdown(f'<div class="section-card"><div class="section-title">📌 Overview</div><div style="font-size:.9rem;color:#8899bb;line-height:1.8">{data.get("overview","")}</div></div>',unsafe_allow_html=True)
        for sec in data.get("sections",[]):
            st.markdown(f'<div class="summary-section"><div class="summary-heading">{sec.get("heading","")}</div><div class="summary-text">{sec.get("summary","")}</div></div>',unsafe_allow_html=True)
            for kp in sec.get("key_points",[]): st.markdown(f'<div style="padding:.15rem .5rem .15rem 1rem;font-size:.84rem;color:#8ab4d4">▸ {kp}</div>',unsafe_allow_html=True)
        c1,c2=st.columns(2)
        with c1:
            if incl_kw and data.get("key_terms"):
                st.markdown('<div class="section-card"><div class="section-title">📚 Key Terms</div>',unsafe_allow_html=True)
                for kt in data["key_terms"]:
                    st.markdown(f'<div style="margin-bottom:.7rem"><span class="key-term">{kt.get("term","")}</span><div style="font-size:.8rem;color:#8899bb;margin-top:.25rem">{kt.get("definition","")}</div></div>',unsafe_allow_html=True)
                st.markdown('</div>',unsafe_allow_html=True)
        with c2:
            if incl_fo and data.get("formulas"):
                st.markdown('<div class="section-card"><div class="section-title">📐 Formulas</div>',unsafe_allow_html=True)
                for f in data["formulas"]:
                    st.markdown(f'<div style="margin-bottom:.8rem"><div style="font-family:monospace;font-size:.95rem;color:#60a5fa;background:#0a1628;padding:.35rem .7rem;border-radius:6px;margin-bottom:.25rem">{f.get("formula","")}</div><div style="font-size:.76rem;color:#5a7099">{f.get("name","")} — {f.get("meaning","")}</div></div>',unsafe_allow_html=True)
                st.markdown('</div>',unsafe_allow_html=True)
        if incl_mm and data.get("mind_map"):
            mm=data["mind_map"]
            st.markdown(f'<div class="section-card"><div class="section-title">🗺️ Mind Map</div><div style="text-align:center;font-family:Syne,sans-serif;font-size:1.1rem;font-weight:700;color:#3a7bd5;padding:.7rem;background:#0a1628;border-radius:8px;margin-bottom:.8rem">{mm.get("center","")}</div>',unsafe_allow_html=True)
            br_cols=st.columns(min(len(mm.get("branches",[])),4))
            for i,br in enumerate(mm.get("branches",[])):
                with br_cols[i%len(br_cols)]:
                    st.markdown(f'<div style="background:#0a1220;border:1px solid #1e3060;border-radius:8px;padding:.7rem;margin-bottom:.5rem"><div style="font-weight:600;color:#60a5fa;font-size:.83rem;margin-bottom:.35rem">{br.get("topic","")}</div>',unsafe_allow_html=True)
                    for st_ in br.get("subtopics",[]): st.markdown(f'<div style="font-size:.76rem;color:#5a7099;padding:1px 0">· {st_}</div>',unsafe_allow_html=True)
                    st.markdown('</div>',unsafe_allow_html=True)
            st.markdown('</div>',unsafe_allow_html=True)
        st.markdown('<div class="section-card"><div class="section-title">✅ Key Conclusions</div>',unsafe_allow_html=True)
        for c in data.get("key_conclusions",[]): st.markdown(f'<div style="padding:.25rem 0;font-size:.88rem;color:#8ab4d4">✓ &nbsp;{c}</div>',unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════
# 5. FLASHCARDS
# ═════════════════════════════════════════════════════════════
elif tool=="flashcards":
    st.markdown("## 🃏 Flashcard Study Set")
    c1,c2=st.columns(2)
    with c1: fc_type=st.selectbox("Card type",["Definition","Concept & Explanation","Formula & Application","Mixed"])
    with c2: fc_lvl=st.selectbox("Level",["Introductory","Intermediate","Advanced"])

    if st.button("🃏 Generate Flashcards",type="primary",use_container_width=True):
        if not check_ready(): st.stop()
        se=st.empty(); pe=st.empty()
        try:
            sp(se,pe,"🧠 Creating flashcards…",40)
            fi=f"Focus on: {focus_topic}." if focus_topic else ""
            prompt=f"""Create {num_fc} study flashcards. Type: {fc_type}. Level: {fc_lvl}. {fi}
NEVER say "from the document" — write cards as standalone academic content.
Return raw JSON only:
{{"subject":"subject","cards":[{{"num":1,"front":"Question or term","back":"Complete answer or definition","type":"Definition","topic":"topic","hint":"memory hint"}}]}}
Generate exactly {num_fc} cards."""
            raw=call_gemini(api_key,prompt,st.session_state.pdf_b64,4096)
            sp(se,pe,"✅ Parsing…",85)
            data=safe_parse(raw); st.session_state.fc_data=data
            st.session_state.fc_idx=0; st.session_state.fc_show=False
            se.empty(); pe.empty()
        except (ValueError,Exception) as e:
            se.empty(); pe.empty(); st.error(str(e))

    if st.session_state.fc_data:
        data=st.session_state.fc_data; cards=data.get("cards",[]); idx=st.session_state.fc_idx; show=st.session_state.fc_show
        if cards:
            card=cards[idx%len(cards)]; pct=int((idx+1)/len(cards)*100)
            st.markdown(f'<div class="progress-bar"><div class="progress-fill" style="width:{pct}%"></div></div>',unsafe_allow_html=True)
            st.markdown(f'<div style="text-align:center;font-size:.76rem;color:#5a7099;margin-bottom:.5rem">Card {idx+1} of {len(cards)} · {card.get("topic","")} · <span style="color:#3a7bd5">{card.get("type","")}</span></div>',unsafe_allow_html=True)
            st.markdown(f'<div class="flashcard"><div class="fc-label">{"✅ ANSWER" if show else "❓ QUESTION — click Flip to reveal"}</div><div class="fc-text">{card.get("back","") if show else card.get("front","")}</div>{"<div style='font-size:.75rem;color:#5a7099;margin-top:.7rem'>💡 "+card.get("hint","")+"</div>" if show and card.get("hint") else ""}</div>',unsafe_allow_html=True)
            bc1,bc2,bc3,bc4=st.columns(4)
            with bc1:
                if st.button("⬅️ Prev",use_container_width=True):
                    st.session_state.fc_idx=max(0,idx-1); st.session_state.fc_show=False; st.rerun()
            with bc2:
                if st.button("🔄 Flip",use_container_width=True,type="primary"):
                    st.session_state.fc_show=not show; st.rerun()
            with bc3:
                if st.button("➡️ Next",use_container_width=True):
                    st.session_state.fc_idx=min(len(cards)-1,idx+1); st.session_state.fc_show=False; st.rerun()
            with bc4:
                if st.button("🔀 Shuffle",use_container_width=True):
                    random.shuffle(cards); st.session_state.fc_data["cards"]=cards
                    st.session_state.fc_idx=0; st.session_state.fc_show=False; st.rerun()
        txt=f"FLASHCARDS — {data.get('subject','')}\n{'='*50}\n\n"
        for c in cards: txt+=f"Card {c.get('num','')} [{c.get('type','')}] — {c.get('topic','')}\nQ: {c.get('front','')}\nA: {c.get('back','')}\n{'💡 '+c['hint'] if c.get('hint') else ''}\n\n"
        st.download_button("⬇️ Download Flashcards (.txt)",data=txt.encode(),file_name="flashcards.txt",mime="text/plain")
        with st.expander("📋 View All Cards"):
            for c in cards:
                with st.expander(f"Card {c.get('num','')} · {str(c.get('front',''))[:60]}"):
                    st.markdown(f"**Q:** {c.get('front','')}"); st.markdown(f"**A:** {c.get('back','')}")
                    if c.get("hint"): st.markdown(f"💡 *{c['hint']}*")

# ═════════════════════════════════════════════════════════════
# 6. AI TUTOR CHAT
# ═════════════════════════════════════════════════════════════
elif tool=="qa":
    st.markdown("## 💬 AI Tutor — Ask Anything")
    if not st.session_state.pdf_b64:
        st.warning("📄 Upload a PDF in the sidebar to start chatting.")
    else:
        st.markdown('<div style="font-size:.8rem;color:#5a7099;margin-bottom:.6rem">Quick questions:</div>',unsafe_allow_html=True)
        qcols=st.columns(4)
        quick_qs=["Summarise the main topics","What are the key formulas?","List all definitions","Key conclusions","Create a study plan","Explain the most complex concept","What topics appear in exams?","Give me 3 practice questions"]
        for i,qq in enumerate(quick_qs):
            with qcols[i%4]:
                if st.button(qq,key=f"qq{i}",use_container_width=True):
                    if api_key: st.session_state.chat.append({"role":"user","content":qq})

        for msg in st.session_state.chat:
            if msg["role"]=="user":
                st.markdown(f'<div class="qa-msg qa-user"><div class="qa-label">You</div>{msg["content"]}</div>',unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="qa-msg qa-ai"><div class="qa-label">🎓 AI Tutor</div>{msg["content"]}</div>',unsafe_allow_html=True)

        if st.session_state.chat and st.session_state.chat[-1]["role"]=="user" and api_key:
            with st.spinner("Thinking…"):
                try:
                    history="\n".join([f"{'Student' if m['role']=='user' else 'Professor'}: {m['content']}" for m in st.session_state.chat[-6:]])
                    prompt=f"""You are an expert university professor and tutor. A student is asking questions.
Answer academically but clearly. Include formulas, examples, and calculations where relevant.
NEVER say "from the document" — answer directly as a knowledgeable professor.
Be thorough, patient, and educational — like office hours with a brilliant professor.
Conversation:\n{history}\nAnswer the latest student question based on the uploaded content."""
                    response=call_gemini(api_key,prompt,st.session_state.pdf_b64,2048,json_mode=False)
                    st.session_state.chat.append({"role":"assistant","content":response}); st.rerun()
                except ValueError as e: st.error(str(e))

        c1,c2=st.columns([5,1])
        with c1: user_input=st.text_input("Ask your AI tutor…","",placeholder="e.g. Explain Newton's second law with a calculation",label_visibility="collapsed",key="chat_input")
        with c2: send=st.button("Send 📨",use_container_width=True,type="primary")
        if send and user_input.strip():
            if not api_key: st.warning("Enter API key.")
            else: st.session_state.chat.append({"role":"user","content":user_input.strip()}); st.rerun()
        if st.session_state.chat:
            if st.button("🗑️ Clear chat"): st.session_state.chat=[]; st.rerun()
