"""
SmartDoc OCR — Home / Navigation Page
FAST-NUCES BSAI · PPIT Project Phase 1 & 2
"""
import streamlit as st

st.set_page_config(
    page_title="SmartDoc OCR | FAST-NUCES",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;}

.home-hero{
  background:linear-gradient(135deg,#0f172a 0%,#1e3a5f 50%,#1d4ed8 100%);
  color:white;padding:3rem 2rem;border-radius:16px;text-align:center;
  margin-bottom:2rem;box-shadow:0 8px 32px rgba(15,23,42,.25);}
.home-hero h1{font-size:2.8rem;font-weight:800;margin:0;letter-spacing:-1px;}
.home-hero h2{font-size:1.1rem;font-weight:400;margin:8px 0 0;opacity:.85;}
.home-hero p{font-size:.9rem;margin:4px 0 0;opacity:.7;}

.phase-card{border-radius:14px;padding:2rem;margin:8px;
            box-shadow:0 2px 12px rgba(0,0,0,.08);height:100%;}
.phase1-card{background:linear-gradient(135deg,#f0f9ff,#e0f2fe);
             border:2px solid #38bdf8;}
.phase2-card{background:linear-gradient(135deg,#f5f3ff,#ede9fe);
             border:2px solid #8b5cf6;}
.phase-badge{display:inline-block;border-radius:20px;padding:4px 14px;
             font-size:.8rem;font-weight:700;margin-bottom:12px;}
.badge1{background:#0ea5e9;color:white;}
.badge2{background:#7c3aed;color:white;}
.feature-tag{display:inline-block;background:rgba(255,255,255,.7);
             border-radius:4px;padding:2px 8px;font-size:.78rem;
             margin:2px;color:#374151;border:1px solid #e5e7eb;}
.clo-card{background:#f8faff;border:1px solid #c7d7f8;border-radius:8px;
          padding:10px 14px;margin:4px 0;font-size:.85rem;}
.footer{text-align:center;font-size:.8rem;color:#9ca3af;margin-top:2rem;
        border-top:1px solid #f1f5f9;padding-top:1rem;}
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="home-hero">
  <h1>📄 SmartDoc OCR</h1>
  <h2>Agentic Image-to-Word Converter</h2>
  <p>FAST-NUCES &nbsp;·&nbsp; BSAI &nbsp;·&nbsp; Professional Practices in IT &nbsp;·&nbsp; 2026</p>
</div>
""", unsafe_allow_html=True)

# ── Phase cards ───────────────────────────────────────────────────────────────
c1, c2 = st.columns(2, gap="large")

with c1:
    st.markdown("""
    <div class="phase-card phase1-card">
      <span class="phase-badge badge1">PHASE 1 — MVP</span>
      <h3 style="margin:0 0 8px;color:#0c4a6e;">📄 Static OCR Converter</h3>
      <p style="color:#475569;font-size:.9rem;margin-bottom:12px;">
        Upload an image → Tesseract extracts text →
        Formatting detected → Download .docx
      </p>
      <div>
        <span class="feature-tag">✅ Tesseract OCR</span>
        <span class="feature-tag">✅ Preprocessing pipeline</span>
        <span class="feature-tag">✅ Heading detection</span>
        <span class="feature-tag">✅ Bullet detection</span>
        <span class="feature-tag">✅ L/C/R alignment</span>
        <span class="feature-tag">✅ Bold text</span>
        <span class="feature-tag">✅ .docx export</span>
        <span class="feature-tag">✅ Multi-image</span>
      </div>
      <p style="color:#64748b;font-size:.8rem;margin-top:12px;">
        Static · Fixed rules · No memory · No learning
      </p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/1_📄_Phase1_Converter.py", label="→ Open Phase 1 Converter", icon="📄")

with c2:
    st.markdown("""
    <div class="phase-card phase2-card">
      <span class="phase-badge badge2">PHASE 2 — AGENTIC</span>
      <h3 style="margin:0 0 8px;color:#3b0764;">🤖 Agentic Converter</h3>
      <p style="color:#475569;font-size:.9rem;margin-bottom:12px;">
        Perception Agent → OCR Agent → Formatting Decision Agent
        → Document Agent → Feedback → Memory → Learning
      </p>
      <div>
        <span class="feature-tag">🔍 Perception Agent</span>
        <span class="feature-tag">⚖️ Decision Agent</span>
        <span class="feature-tag">🧠 Memory (short+long)</span>
        <span class="feature-tag">🔄 Feedback loop</span>
        <span class="feature-tag">👤 Human-in-the-loop</span>
        <span class="feature-tag">📋 Audit log</span>
        <span class="feature-tag">🏆 Strategy learning</span>
        <span class="feature-tag">🔍 Decision reasoning</span>
      </div>
      <p style="color:#64748b;font-size:.8rem;margin-top:12px;">
        Adaptive · Goal-based + Learning agent · Semi-autonomous
      </p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/2_🤖_Phase2_Agent.py", label="→ Open Phase 2 Agentic System", icon="🤖")

# ── Comparison table ──────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 📊 Phase 1 vs Phase 2 — At a Glance")

tbl = {
    "Feature":          ["Control","Intelligence","Preprocessing","Feedback loop",
                         "Memory","Decision explanation","Autonomy","Learning"],
    "Phase 1 (Static)": ["User-driven","Fixed rules","Fixed pipeline","❌ None",
                         "❌ None","❌ Hidden","❌ None","❌ None"],
    "Phase 2 (Agentic)":["Agent + Human override","Adaptive heuristics","Strategy selection",
                         "✅ ⭐ Rating","✅ Short + Long term","✅ Per-line reasoning",
                         "✅ Semi-autonomous","✅ Session-based"],
}
st.table(tbl)

# ── CLO mapping ───────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 🎓 Course Learning Outcomes (NCEAC)")
col1,col2 = st.columns(2)
with col1:
    for clo, desc in [
        ("CLO 4","Professional ethics · IEEE/ACM codes applied in agent design"),
        ("CLO 5","IPR: Open-source licensing (Apache 2.0, MIT) · GDPR mindset"),
    ]:
        st.markdown(f'<div class="clo-card"><b>{clo}:</b> {desc}</div>', unsafe_allow_html=True)
with col2:
    for clo, desc in [
        ("CLO 6","PECA 2016 awareness · Privacy: session-only, no data stored"),
        ("CLO 8","Agentic AI industry trend · Career skills: OCR + agent design"),
    ]:
        st.markdown(f'<div class="clo-card"><b>{clo}:</b> {desc}</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  SmartDoc OCR &nbsp;·&nbsp; FAST-NUCES BSAI &nbsp;·&nbsp;
  PPIT Final Project Phase 1 &amp; 2 &nbsp;·&nbsp; 2026<br>
  Stack: Python · Streamlit · Tesseract · OpenCV · python-docx · GitHub
</div>
""", unsafe_allow_html=True)
