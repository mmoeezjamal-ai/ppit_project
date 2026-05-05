"""
Phase 2 — Purely Agentic Image-to-Word Converter
Perception → Decision → Action → Feedback → Memory → Learning
"""
import streamlit as st
import io, json, os, time, datetime
from PIL import Image
import numpy as np

from utils import (analyze_image_quality, recommend_strategy, preprocess_image,
                   run_ocr, run_ocr_best, run_easyocr, easyocr_to_paragraphs,
                   extract_formatted_lines, group_into_paragraphs,
                   generate_docx, classify_line, detect_alignment)

st.set_page_config(page_title="Phase 2 — Agentic", page_icon="🤖", layout="wide")

# ══════════════════════════════════════════════════════════════════════════════
# AGENT CLASSES
# ══════════════════════════════════════════════════════════════════════════════

class AgentMemory:
    """Short-term (session) + Long-term (JSON file) memory."""
    STORE = os.path.join(os.environ.get("TEMP", "/tmp"), "smartdoc_memory.json")

    def __init__(self):
        self.short: dict = {}
        self.long:  dict = self._load()

    def _load(self) -> dict:
        try:
            if os.path.exists(self.STORE):
                with open(self.STORE) as f:
                    return json.load(f)
        except Exception:
            pass
        return {"sessions": 0, "feedback_scores": [],
                "strategy_wins": {"basic": 0, "enhanced": 0, "aggressive": 0},
                "preferences": {}}

    def save(self):
        try:
            with open(self.STORE, "w") as f:
                json.dump(self.long, f, indent=2)
        except Exception:
            pass

    def remember(self, key: str, value, term: str = "short"):
        if term == "short":
            self.short[key] = value
        else:
            self.long[key] = value
            self.save()

    def recall(self, key: str, term: str = "short", default=None):
        store = self.short if term == "short" else self.long
        return store.get(key, default)

    def record_session(self, strategy: str, score: float):
        self.long["sessions"] += 1
        self.long["strategy_wins"][strategy] = \
            self.long["strategy_wins"].get(strategy, 0) + 1
        self.save()

    def record_feedback(self, rating: int, strategy: str):
        self.long["feedback_scores"].append({"rating": rating,
                                             "strategy": strategy,
                                             "ts": datetime.datetime.now().isoformat()})
        self.long["strategy_wins"][strategy] = \
            self.long["strategy_wins"].get(strategy, 0) + rating
        self.save()

    @property
    def best_strategy(self) -> str:
        wins = self.long.get("strategy_wins", {})
        if not wins or max(wins.values()) == 0:
            return "enhanced"
        return max(wins, key=wins.get)

    @property
    def avg_feedback(self) -> float:
        scores = [f["rating"] for f in self.long.get("feedback_scores", [])]
        return round(sum(scores) / len(scores), 1) if scores else 0.0


class PerceptionAgent:
    """Analyzes image quality and selects preprocessing strategy."""

    def run(self, pil_img: Image.Image, memory: AgentMemory,
            override_strategy: str | None = None) -> dict:
        log = []
        ts  = time.time()

        log.append("🔍 Analyzing image quality metrics…")
        metrics = analyze_image_quality(pil_img)

        rec_strategy, rec_reason = recommend_strategy(metrics)
        log.append(f"📊 Quality score: {metrics['quality_score']:.1f}/100")
        log.append(f"💡 Recommended strategy: **{rec_strategy}** — {rec_reason}")

        if metrics.get("is_inverted"):
            log.append("🔄 **Dark background detected** (light text on dark bg) → image will be inverted before OCR")

        if metrics.get("has_ruled_lines"):
            log.append(f"📓 **Colored notebook paper detected** (saturation={metrics.get('sat_mean',0):.1f}) → "
                       "blue ruled lines will be removed, min-channel decomposition applied to preserve colored ink")

        if metrics["is_handwritten"]:
            log.append("✏️ Document type: **Handwritten** (edge ratio low → likely notes)")
        else:
            log.append("🖨️ Document type: **Printed/Typed** (high edge density)")

        if metrics["skew_angle"] > 2:
            log.append(f"⚠️ Skew detected: {metrics['skew_angle']:.1f}° — will auto-correct")
        else:
            log.append(f"✅ Skew: {metrics['skew_angle']:.1f}° — acceptable")

        if metrics["is_multi_column"]:
            log.append("📐 Layout: Multi-column detected")
        else:
            log.append("📐 Layout: Single-column")

        mem_best = memory.best_strategy
        if override_strategy:
            final_strategy = override_strategy
            log.append(f"👤 Human override: using **{final_strategy}** strategy")
        elif memory.long["sessions"] >= 3 and mem_best != rec_strategy:
            final_strategy = mem_best
            log.append(f"🧠 Memory suggests **{mem_best}** (best from past sessions) — using that")
        else:
            final_strategy = rec_strategy

        log.append(f"✅ Final strategy selected: **{final_strategy}**")

        return {
            "metrics":   metrics,
            "strategy":  final_strategy,
            "reasoning": rec_reason,
            "log":       log,
            "duration":  round(time.time() - ts, 3),
        }


class OCRAgent:
    """Dual-engine OCR: Tesseract (printed text) or EasyOCR (handwriting)."""

    def run(self, preprocessed: Image.Image, engine: str = "tesseract",
            original_img: Image.Image = None) -> dict:
        log = []
        ts  = time.time()

        # ── EasyOCR path ──────────────────────────────────────────────────────
        if engine == "easyocr":
            log.append("🧠 Using **EasyOCR** (deep learning — better for handwriting)…")
            log.append("⏳ Loading model on first run (~15 s) — cached for subsequent runs")
            src = original_img if original_img is not None else preprocessed
            results = run_easyocr(src)
            if not results:
                return {"data": None, "easy_results": None, "words": 0, "avg_conf": 0,
                        "engine": "easyocr", "log": ["❌ EasyOCR failed — is easyocr installed?"],
                        "duration": 0, "success": False}
            words = [r[1].strip() for r in results if r[1].strip() and r[2] > 0.15]
            avg_c = round(sum(r[2] for r in results) / len(results) * 100, 1)
            log.append(f"📝 Text regions detected: **{len(results)}**")
            log.append(f"📝 Words extracted: **{len(words)}**")
            log.append(f"📊 Average confidence: **{avg_c}%**")
            if avg_c < 50:
                log.append("⚠️ Low confidence — very difficult handwriting")
            elif avg_c < 70:
                log.append("🟡 Moderate confidence — some words may need correction")
            else:
                log.append("✅ Good confidence — EasyOCR handled this well")
            return {
                "data":         None,
                "easy_results": results,
                "words":        len(words),
                "avg_conf":     avg_c,
                "engine":       "easyocr",
                "log":          log,
                "duration":     round(time.time() - ts, 3),
                "success":      True,
            }

        # ── Tesseract path ────────────────────────────────────────────────────
        log.append("⚙️ Using **Tesseract** — testing PSM modes: 6, 4, 11, 3…")
        data, best_psm, _ = run_ocr_best(preprocessed)
        if data is None:
            return {"data": None, "easy_results": None, "words": 0, "avg_conf": 0,
                    "engine": "tesseract", "log": ["❌ Tesseract OCR failed"],
                    "duration": 0, "success": False}
        words = [w.strip() for w, c in zip(data["text"], data["conf"])
                 if w.strip() and int(c) > 10]
        confs = [int(c) for c in data["conf"] if int(c) > 0]
        avg_c = round(sum(confs) / len(confs), 1) if confs else 0
        log.append(f"🏆 Best PSM: **{best_psm}**")
        log.append(f"📝 Words extracted: **{len(words)}**")
        log.append(f"📊 Average confidence: **{avg_c}%**")
        if avg_c < 50:
            log.append("⚠️ Low confidence — try switching to **EasyOCR** for handwriting")
        elif avg_c < 70:
            log.append("🟡 Moderate confidence — results may need review")
        else:
            log.append("✅ High confidence — OCR reliable")
        return {
            "data":         data,
            "easy_results": None,
            "words":        len(words),
            "avg_conf":     avg_c,
            "psm":          best_psm,
            "engine":       "tesseract",
            "log":          log,
            "duration":     round(time.time() - ts, 3),
            "success":      True,
        }


class FormattingDecisionAgent:
    """Makes formatting decisions with explicit reasoning per line."""

    def run(self, ocr_data: dict, page_w: int,
            bold_threshold: float = 1.28,
            heading_threshold: float = 1.5) -> dict:
        log = []
        ts  = time.time()
        log.append("🧠 Analysing text structure and layout…")

        lines   = extract_formatted_lines(ocr_data, page_w)
        paras   = group_into_paragraphs(lines)

        decisions = []
        for line in lines:
            reason = []
            if line["is_heading"] and line["text"].startswith("#"):
                reason.append(f"# prefix → Heading H{line['h_level']}")
            elif line["is_heading"] and line["text"].isupper():
                reason.append(f"ALL CAPS ({len(line['text'].split())} words) → Heading")
            if line["is_bullet"]:
                reason.append("Bullet marker detected → List item")
            if line["is_bold"] and not line["is_heading"]:
                reason.append(
                    f"Height {line['avg_h']:.0f}px > {line['mean_h']*bold_threshold:.0f}px → Bold"
                )
            if line["alignment"] != "left":
                reason.append(f"Position-based → {line['alignment'].capitalize()} aligned")
            if not reason:
                reason.append("Default → Normal text")

            decisions.append({**line, "reason": " · ".join(reason)})

        h_cnt  = sum(1 for d in decisions if d["is_heading"])
        b_cnt  = sum(1 for d in decisions if d["is_bullet"])
        bo_cnt = sum(1 for d in decisions if d["is_bold"])
        c_cnt  = sum(1 for d in decisions if d["alignment"] == "center")

        log.append(f"📰 Headings detected: **{h_cnt}**")
        log.append(f"📌 Bullet points: **{b_cnt}**")
        log.append(f"🔤 Bold segments: **{bo_cnt}**")
        log.append(f"↔️ Center-aligned lines: **{c_cnt}**")
        log.append(f"📄 Paragraph groups: **{len(paras)}**")

        return {
            "lines":     decisions,
            "paras":     paras,
            "headings":  h_cnt,
            "bullets":   b_cnt,
            "bold":      bo_cnt,
            "log":       log,
            "duration":  round(time.time() - ts, 3),
        }


class DocumentAgent:
    """Generates the .docx from formatted paragraphs."""

    def run(self, paras: list, title: str) -> dict:
        ts  = time.time()
        doc = generate_docx([paras], title)
        buf = io.BytesIO()
        doc.save(buf)
        buf.seek(0)
        return {
            "buffer":   buf,
            "size":     len(buf.getvalue()),
            "duration": round(time.time() - ts, 3),
        }


# ══════════════════════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;}

.hero2{background:linear-gradient(135deg,#0f172a,#1e3a5f,#1d4ed8);
       color:white;padding:1.8rem 2rem;border-radius:12px;
       margin-bottom:1.2rem;text-align:center;}
.hero2 h1{font-size:2rem;font-weight:700;margin:0;}
.hero2 p{font-size:.9rem;margin:5px 0 0;opacity:.85;}

.agent-card{background:#f8faff;border:1.5px solid #c7d7f8;
            border-radius:10px;padding:16px 18px;margin:10px 0;}
.agent-title{font-size:1rem;font-weight:700;color:#1e3a5f;
             border-bottom:2px solid #3b82f6;padding-bottom:5px;margin-bottom:10px;}
.metric-row{display:flex;gap:10px;flex-wrap:wrap;margin:8px 0;}
.metric-pill{background:#eff6ff;border:1px solid #bfdbfe;border-radius:20px;
             padding:4px 12px;font-size:.82rem;color:#1e40af;font-weight:600;}
.log-line{font-size:.85rem;color:#374151;padding:2px 0;border-bottom:1px solid #f1f5f9;}
.decision-row{font-size:.8rem;color:#475569;padding:3px 0;}
.status-bar{background:#1e293b;color:#e2e8f0;border-radius:8px;
            padding:10px 16px;display:flex;gap:24px;margin-bottom:16px;font-size:.85rem;}
.status-item{display:inline-block;}
.status-val{font-weight:700;color:#60a5fa;}
.success-card{background:#d1fae5;border:1px solid #6ee7b7;border-radius:10px;
              padding:16px;color:#065f46;font-weight:600;text-align:center;}
.mem-card{background:#fefce8;border:1px solid #fde68a;border-radius:8px;padding:12px 16px;}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SESSION INIT
# ══════════════════════════════════════════════════════════════════════════════

if "memory" not in st.session_state:
    st.session_state.memory    = AgentMemory()
if "audit_log" not in st.session_state:
    st.session_state.audit_log = []
if "result"    not in st.session_state:
    st.session_state.result    = None

memory:AgentMemory = st.session_state.memory

# ══════════════════════════════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="hero2">
  <h1>🤖 Phase 2 — Agentic Image-to-Word Converter</h1>
  <p>Perception · Decision · Action · Feedback · Memory · Learning</p>
  <p style="font-size:.8rem;opacity:.7;">
    Goal-based + Learning Agent &nbsp;|&nbsp; Semi-Autonomous &nbsp;|&nbsp;
    Human-in-the-Loop &nbsp;|&nbsp; Transparent Decisions
  </p>
</div>""", unsafe_allow_html=True)

# ── Status bar ────────────────────────────────────────────────────────────────
sessions  = memory.long.get("sessions", 0)
avg_fb    = memory.avg_feedback
best_strat= memory.best_strategy

st.markdown(f"""
<div class="status-bar">
  <span class="status-item">🟢 Agent <span class="status-val">Online</span></span>
  <span class="status-item">🧠 Memory
    <span class="status-val">{sessions} sessions</span></span>
  <span class="status-item">⭐ Avg feedback
    <span class="status-val">{avg_fb}/5</span></span>
  <span class="status-item">🏆 Best strategy
    <span class="status-val">{best_strat}</span></span>
  <span class="status-item">⚙️ Mode
    <span class="status-val">Semi-Autonomous</span></span>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR — HUMAN-IN-THE-LOOP CONTROLS
# ══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("### 🕹️ Human-in-the-Loop Controls")
    st.caption("Override agent decisions at any step.")

    ocr_engine = st.radio(
        "OCR Engine",
        ["🤖 Tesseract (fast, printed text)", "🧠 EasyOCR (slow, handwriting)"],
        help="EasyOCR uses deep learning — much better for handwritten notes. First run takes ~15s to load model."
    )
    ocr_engine = "easyocr" if "EasyOCR" in ocr_engine else "tesseract"

    if ocr_engine == "easyocr":
        st.info("EasyOCR runs on the **original image** (no preprocessing needed). First run loads the model (~15 s).")

    override_strategy = st.selectbox(
        "Preprocessing strategy",
        ["🤖 Let agent decide", "basic", "enhanced", "aggressive"],
        help="Override the Perception Agent's strategy selection"
    )
    override_strategy = None if "agent" in override_strategy else override_strategy

    bold_thresh = st.slider("Bold detection threshold", 1.1, 2.0, 1.28, 0.05,
                             help="Height ratio above mean to classify as bold")
    heading_thresh = st.slider("Heading size threshold", 1.2, 2.0, 1.5, 0.05,
                                help="Height ratio for H1 vs H2 classification")

    doc_title = st.text_input("Document title", "Agentic Converted Document")

    st.markdown("---")
    st.markdown("### 🧠 Memory Dashboard")

    st.markdown(f"""
    <div class="mem-card">
      <b>Sessions learned:</b> {sessions}<br>
      <b>Avg rating:</b> {avg_fb}/5<br>
      <b>Best strategy:</b> {best_strat}<br>
      <b>Strategy wins:</b><br>
      {''.join(f"&nbsp;&nbsp;{k}: {v}<br>" for k,v in memory.long.get('strategy_wins',{}).items())}
    </div>""", unsafe_allow_html=True)

    if st.button("🗑️ Reset Memory", use_container_width=True):
        try:
            os.remove(AgentMemory.STORE)
        except Exception:
            pass
        st.session_state.memory = AgentMemory()
        st.rerun()

    st.markdown("---")
    st.markdown("""**Phase 2 — Agentic Pipeline**

    Perception → OCR → Formatting  
    Decision → Action → Feedback  
    Memory + Human-in-the-Loop""")

# ══════════════════════════════════════════════════════════════════════════════
# UPLOAD
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("### 📁 Upload Image")
uploaded_file = st.file_uploader(
    "Upload one scanned page / handwritten note",
    type=["jpg","jpeg","png","bmp","tiff"]
)

if not uploaded_file:
    col1,col2,col3 = st.columns(3)
    col1.info("**🧠 Perception Agent**\nAnalyzes image quality, brightness, contrast, skew, document type")
    col2.info("**⚖️ Decision Agent**\nMakes formatting decisions with explicit reasoning per line")
    col3.info("**📚 Memory Module**\nLearns from feedback, remembers best strategies across sessions")
    st.markdown("---")
    st.markdown("### 🔄 Agentic vs Phase 1")
    df_data = {
        "Feature": ["Control","Intelligence","Preprocessing","Feedback","Memory","Decision Log","Autonomy"],
        "Phase 1 (Static)": ["User-driven","Fixed rules","Fixed pipeline","None","None","Hidden","None"],
        "Phase 2 (Agentic)": ["Agent + Human","Adaptive + Learning","Strategy selection","⭐ Rating loop","Short + Long term","Transparent","Semi-autonomous"],
    }
    st.table(df_data)
    st.stop()

if not st.button("🚀 Run Agent Pipeline", type="primary", use_container_width=True):
    st.info("✅ Image ready — press **Run Agent Pipeline**.")
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# AGENT PIPELINE EXECUTION
# ══════════════════════════════════════════════════════════════════════════════

pil_img = Image.open(uploaded_file).convert("RGB")
page_w  = pil_img.width
pipeline_start = time.time()

audit = []

st.markdown("---")
st.markdown("## 🔄 Agent Pipeline")

col_img, col_pipe = st.columns([1, 1.5])
with col_img:
    st.markdown("**Uploaded image**")
    st.image(pil_img, use_container_width=True)

with col_pipe:

    # ── STEP 1: PERCEPTION ────────────────────────────────────────────────────
    with st.container():
        st.markdown('<div class="agent-card">', unsafe_allow_html=True)
        st.markdown('<div class="agent-title">🔍 Step 1 — Perception Agent</div>', unsafe_allow_html=True)

        with st.spinner("Perception Agent analyzing…"):
            perc_agent = PerceptionAgent()
            perc_result = perc_agent.run(pil_img, memory, override_strategy)

        m = perc_result["metrics"]
        # Quality bars
        def pct(v, mx): return min(int(v/mx*100),100)

        st.markdown(f"""
        <div class="metric-row">
          <span class="metric-pill">Brightness {m['brightness']:.0f}/255</span>
          <span class="metric-pill">Contrast {m['contrast']:.0f}</span>
          <span class="metric-pill">Sharpness {m['sharpness']:.0f}</span>
          <span class="metric-pill">Noise {m['noise']:.1f}</span>
          <span class="metric-pill">Skew {m['skew_angle']:.1f}°</span>
          <span class="metric-pill">Quality {m['quality_score']:.0f}/100</span>
        </div>""", unsafe_allow_html=True)

        for line in perc_result["log"]:
            st.markdown(f'<div class="log-line">{line}</div>', unsafe_allow_html=True)
        st.caption(f"⏱️ {perc_result['duration']}s")
        st.markdown('</div>', unsafe_allow_html=True)

    audit.append({"step": "Perception", "strategy": perc_result["strategy"],
                  "quality": m["quality_score"], "ts": datetime.datetime.now().isoformat()})

    # ── STEP 2: PREPROCESSING ─────────────────────────────────────────────────
    with st.container():
        st.markdown('<div class="agent-card">', unsafe_allow_html=True)
        st.markdown('<div class="agent-title">🔧 Step 2 — Preprocessing Agent</div>', unsafe_allow_html=True)

        with st.spinner(f"Applying **{perc_result['strategy']}** strategy…"):
            preprocessed = preprocess_image(pil_img, strategy=perc_result["strategy"])

        st.markdown(f'<div class="log-line">✅ Strategy applied: <b>{perc_result["strategy"]}</b></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="log-line">📐 Output size: {preprocessed.size[0]}×{preprocessed.size[1]}px</div>', unsafe_allow_html=True)

        if st.checkbox("👁️ Preview preprocessed image", key="prev_pre"):
            st.image(preprocessed, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── STEP 3: OCR ───────────────────────────────────────────────────────────
    with st.container():
        st.markdown('<div class="agent-card">', unsafe_allow_html=True)
        st.markdown('<div class="agent-title">📝 Step 3 — OCR Agent</div>', unsafe_allow_html=True)

        with st.spinner("OCR Agent extracting text…"):
            ocr_agent  = OCRAgent()
            ocr_result = ocr_agent.run(preprocessed,
                                       engine=ocr_engine,
                                       original_img=pil_img)

        if not ocr_result["success"]:
            st.error("OCR failed."); st.stop()

        for line in ocr_result["log"]:
            st.markdown(f'<div class="log-line">{line}</div>', unsafe_allow_html=True)
        st.caption(f"⏱️ {ocr_result['duration']}s")
        st.markdown('</div>', unsafe_allow_html=True)

    audit.append({"step": "OCR", "words": ocr_result["words"],
                  "avg_conf": ocr_result["avg_conf"], "ts": datetime.datetime.now().isoformat()})

    # ── STEP 4: FORMATTING DECISION ───────────────────────────────────────────
    with st.container():
        st.markdown('<div class="agent-card">', unsafe_allow_html=True)
        st.markdown('<div class="agent-title">⚖️ Step 4 — Formatting Decision Agent</div>', unsafe_allow_html=True)

        with st.spinner("Decision Agent analysing structure…"):
            if ocr_result["engine"] == "easyocr" and ocr_result["easy_results"]:
                easy_paras = easyocr_to_paragraphs(ocr_result["easy_results"], page_w)
                fmt_result = {
                    "paragraphs": easy_paras,
                    "headings":   sum(1 for p in easy_paras if p["is_heading"]),
                    "bullets":    sum(1 for p in easy_paras if p["is_bullet"]),
                    "log":        [f"📝 EasyOCR: {len(easy_paras)} text regions formatted",
                                   f"🔖 {sum(1 for p in easy_paras if p['is_heading'])} headings detected",
                                   f"• {sum(1 for p in easy_paras if p['is_bullet'])} bullets detected"],
                    "lines":      [{"clean": p["text"], "reason": f"EasyOCR region — {'Heading' if p['is_heading'] else 'Bullet' if p['is_bullet'] else 'Body'}"}
                                   for p in easy_paras],
                    "duration":   0,
                }
            else:
                fmt_agent  = FormattingDecisionAgent()
                fmt_result = fmt_agent.run(ocr_result["data"], page_w,
                                           bold_threshold=bold_thresh,
                                           heading_threshold=heading_thresh)

        for line in fmt_result["log"]:
            st.markdown(f'<div class="log-line">{line}</div>', unsafe_allow_html=True)

        with st.expander("📋 View full decision log"):
            for d in fmt_result["lines"][:40]:
                st.markdown(
                    f'<div class="decision-row">'
                    f'<b>{d["clean"][:55]}{"…" if len(d["clean"])>55 else ""}</b>'
                    f'<br><span style="color:#6b7280">{d["reason"]}</span>'
                    f'</div>', unsafe_allow_html=True
                )

        st.caption(f"⏱️ {fmt_result['duration']}s")
        st.markdown('</div>', unsafe_allow_html=True)

    audit.append({"step": "FormattingDecision",
                  "headings": fmt_result["headings"], "bullets": fmt_result["bullets"],
                  "ts": datetime.datetime.now().isoformat()})

    # ── STEP 5: DOCUMENT GENERATION ───────────────────────────────────────────
    with st.container():
        st.markdown('<div class="agent-card">', unsafe_allow_html=True)
        st.markdown('<div class="agent-title">📄 Step 5 — Document Agent</div>', unsafe_allow_html=True)

        with st.spinner("Document Agent generating .docx…"):
            doc_agent   = DocumentAgent()
            doc_result  = doc_agent.run(fmt_result["paras"], doc_title)

        st.markdown(f'<div class="log-line">✅ Document generated: <b>{doc_result["size"]:,} bytes</b></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="log-line">📄 Paragraphs: <b>{len(fmt_result["paras"])}</b> &nbsp;|&nbsp; Headings: <b>{fmt_result["headings"]}</b> &nbsp;|&nbsp; Bullets: <b>{fmt_result["bullets"]}</b></div>', unsafe_allow_html=True)
        st.caption(f"⏱️ {doc_result['duration']}s")
        st.markdown('</div>', unsafe_allow_html=True)

total_time = round(time.time() - pipeline_start, 2)
audit.append({"step": "DocumentGeneration", "size": doc_result["size"],
              "total_time": total_time, "ts": datetime.datetime.now().isoformat()})

# Store in session
st.session_state.result     = doc_result
st.session_state.audit_log  = audit
st.session_state.last_strategy = perc_result["strategy"]
memory.record_session(perc_result["strategy"], m["quality_score"])

# ══════════════════════════════════════════════════════════════════════════════
# RESULTS + FEEDBACK
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown(f'<div class="success-card">✅ Agent pipeline complete in <b>{total_time}s</b>!</div>',
            unsafe_allow_html=True)

m1,m2,m3,m4,m5 = st.columns(5)
m1.metric("Words extracted",  ocr_result["words"])
m2.metric("OCR Confidence",   f"{ocr_result['avg_conf']}%")
m3.metric("Headings",         fmt_result["headings"])
m4.metric("Bullets",          fmt_result["bullets"])
m5.metric("Total time",       f"{total_time}s")

st.download_button(
    "⬇️ Download Word Document (.docx)",
    doc_result["buffer"],
    f"{doc_title.replace(' ','_')}.docx",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    use_container_width=True, type="primary"
)

# ── STEP 6: FEEDBACK AGENT ────────────────────────────────────────────────────
st.markdown("---")
st.markdown('<div class="agent-card">', unsafe_allow_html=True)
st.markdown('<div class="agent-title">🔄 Step 6 — Feedback Agent (Updates Memory)</div>',
            unsafe_allow_html=True)
st.caption("Rate the quality of this conversion — the agent learns from your feedback.")

rating  = st.slider("⭐ Your rating (1=poor, 5=excellent)", 1, 5, 3)
comment = st.text_input("Optional comment", placeholder="e.g. headings detected correctly…")

if st.button("✅ Submit Feedback → Update Memory", use_container_width=True):
    memory.record_feedback(rating, st.session_state.get("last_strategy", "enhanced"))
    st.success(f"✅ Feedback recorded! Rating {rating}/5 stored. Memory updated. "
               f"Agent has now learned from {memory.long['sessions']} sessions.")
    st.balloons()

st.markdown('</div>', unsafe_allow_html=True)

# ── AUDIT LOG ─────────────────────────────────────────────────────────────────
with st.expander("📋 Full Agent Audit Log (Transparency)"):
    st.caption("All agent decisions logged for explainability and user control.")
    for entry in st.session_state.audit_log:
        st.json(entry)
    audit_bytes = json.dumps(st.session_state.audit_log, indent=2).encode()
    st.download_button("⬇️ Download Audit Log (.json)", audit_bytes,
                       "audit_log.json", "application/json")
