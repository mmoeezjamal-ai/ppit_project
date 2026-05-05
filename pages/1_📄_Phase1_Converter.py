import streamlit as st
import io
from PIL import Image
from utils import (preprocess_image, run_ocr, extract_formatted_lines,
                   group_into_paragraphs, generate_docx)

st.set_page_config(page_title="Phase 1 — Image→Word", page_icon="📄", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
.hero{background:linear-gradient(135deg,#0d2137,#1a4a7a,#2563a8);color:white;
      padding:1.8rem 2rem;border-radius:12px;margin-bottom:1.2rem;text-align:center;}
.hero h1{font-size:2rem;font-weight:700;margin:0;}
.hero p{font-size:.9rem;margin:5px 0 0;opacity:.85;}
.step-card{background:#f0f6ff;border-left:4px solid #2563a8;
           padding:9px 13px;border-radius:6px;margin:5px 0;font-size:.9rem;}
.success-card{background:#d1fae5;border:1px solid #6ee7b7;border-radius:10px;
              padding:16px;color:#065f46;font-weight:600;text-align:center;}
.badge{display:inline-block;background:#dbeafe;color:#1e40af;
       border-radius:4px;padding:2px 8px;font-size:.78rem;margin:2px;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>📄 Phase 1 — Image → Word Converter</h1>
  <p>Static OCR pipeline · Tesseract · Formatting detection · .docx export</p>
</div>""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    enhance   = st.checkbox("🔧 Enhance image quality", value=True)
    show_pre  = st.checkbox("👁️ Show preprocessed image", value=False)
    show_raw  = st.checkbox("📋 Show raw OCR text", value=True)
    doc_title = st.text_input("📝 Document title", value="Converted Document")
    st.markdown("---")
    st.markdown("""**Phase 1 — Static Pipeline**
    
    Upload → Preprocess → OCR → Format → Download
    
    No memory · No learning · No agent decisions""")

# ── Upload ────────────────────────────────────────────────────────────────────
st.markdown("### 📁 Upload Images")
uploaded = st.file_uploader(
    "JPG / PNG / JPEG images",
    type=["jpg","jpeg","png","bmp","tiff"],
    accept_multiple_files=True,
)

if not uploaded:
    c1,c2,c3,c4 = st.columns(4)
    c1.info("📰 Headings\n\n`#` prefix or ALL CAPS")
    c2.info("📌 Bullets\n\n`•` `-` `1.` patterns")
    c3.info("↔️ Alignment\n\nLeft / Center / Right")
    c4.info("🔤 Bold\n\nFont-size heuristic")
    st.stop()

if not st.button("🚀 Convert to Word", type="primary", use_container_width=True):
    st.info(f"✅ {len(uploaded)} image(s) ready — press Convert.")
    st.stop()

# ── Processing ────────────────────────────────────────────────────────────────
progress   = st.progress(0, text="Starting…")
all_pages  = []
tot        = {"paras": 0, "headings": 0, "bullets": 0, "bold": 0}

for idx, f in enumerate(uploaded):
    progress.progress(idx / len(uploaded), text=f"Processing {f.name}…")
    pil   = Image.open(f).convert("RGB")
    pw    = pil.width

    with st.expander(f"📷 Page {idx+1} — {f.name}", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Original**")
            st.image(pil, use_container_width=True)

        pre = preprocess_image(pil, strategy="enhanced" if enhance else "basic")
        if show_pre:
            with c2:
                st.markdown("**Preprocessed**")
                st.image(pre, use_container_width=True)

        with st.spinner("Running OCR…"):
            data = run_ocr(pre)

        if data is None:
            st.error("OCR failed — skipping.")
            all_pages.append([])
            continue

        fmt_lines = extract_formatted_lines(data, pw)
        paras     = group_into_paragraphs(fmt_lines)
        all_pages.append(paras)

        hc = sum(1 for p in paras for l in p if l["is_heading"])
        bc = sum(1 for p in paras for l in p if l["is_bullet"])
        bo = sum(1 for p in paras for l in p if l["is_bold"])
        tot["paras"] += len(paras); tot["headings"] += hc
        tot["bullets"] += bc;      tot["bold"] += bo

        if not show_pre:
            with c2:
                raw = "\n".join(" ".join(l["text"] for l in p) for p in paras)
                st.markdown("**Extracted Text**")
                st.text_area("", raw, height=400, key=f"r{idx}", label_visibility="collapsed")

        m1,m2,m3,m4 = st.columns(4)
        m1.metric("Paragraphs", len(paras))
        m2.metric("Headings",   hc)
        m3.metric("Bullets",    bc)
        m4.metric("Bold lines", bo)

progress.progress(0.95, text="Generating document…")
try:
    doc = generate_docx(all_pages, doc_title)
    buf = io.BytesIO(); doc.save(buf); buf.seek(0)
    progress.progress(1.0, text="Done!")
    st.markdown('<div class="success-card">✅ Word document ready!</div>', unsafe_allow_html=True)
    s1,s2,s3,s4,s5 = st.columns(5)
    s1.metric("Pages",      len(uploaded))
    s2.metric("Paragraphs", tot["paras"])
    s3.metric("Headings",   tot["headings"])
    s4.metric("Bullets",    tot["bullets"])
    s5.metric("Bold",       tot["bold"])
    st.download_button("⬇️ Download .docx", buf,
                       f"{doc_title.replace(' ','_')}.docx",
                       "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                       use_container_width=True, type="primary")
    st.balloons()
except Exception as e:
    st.error(f"Error: {e}"); st.exception(e)
