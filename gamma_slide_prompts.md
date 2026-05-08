# SmartDoc OCR — 20 Gamma Slide Prompts
## PPIT Phase 2 Final Presentation | FAST-NUCES BSAI

---

## HOW TO USE WITH GAMMA.APP

1. Go to **gamma.app** → "Create new" → "Generate"
2. Select **"Generate from text"**
3. Paste each slide prompt below into Gamma's prompt box (one slide at a time for best control), OR paste this entire document at once for a full deck
4. Set **Theme**: Dark navy professional (background `#0f172a`, accent `#3b82f6`, text white)
5. **Image generation**: For each slide, copy the `IMAGE PROMPT` block into Gamma's image generator OR DALL-E/Midjourney for higher quality

**Tone & Theme**: Professional, confident, evidence-driven. Show that the project succeeded with strong working results.

---

## ✅ SLIDE 1 — Title Slide

**Gamma Prompt:**

Create a striking **title slide** with hero layout, dark navy background. Center-aligned content.

- **Main title (huge, bold):** SmartDoc OCR
- **Subtitle:** Agentic Image-to-Word Converter
- **Tag line (smaller):** From Static Tool → Intelligent Agent
- **Course:** Professional Practices in IT (PPIT) — Final Project Phase 2
- **University:** FAST-NUCES, Islamabad — BSAI
- **Team:** Moeez Jamal-22i0513 · Ali Farqaleet-22i0579 · Ammad Nasir-22i0477
- **Date:** Spring 2026
- Bottom-right small badge: "Live Demo · GitHub · Deployed on Streamlit Cloud"

**IMAGE PROMPT:** *A futuristic 3D render of a paper document transforming into a glowing blue robotic AI agent. Soft cyan light rays, dark navy background, document pages flying around the robot, ultra modern minimalist tech aesthetic, depth of field, high detail, professional product render style.*

---

## ✅ SLIDE 2 — Phase 1 Recap + Why We Needed Phase 2

**Gamma Prompt:**

Create a **two-column comparison slide** titled **"Phase 1 Was Solid — But It Was Just a Tool"**.

**LEFT COLUMN (green tint) — "Phase 1 Achievements ✅":**
- Built a working Streamlit app: Image → Word converter
- 6-stage preprocessing: upscale → grayscale → denoise → CLAHE → adaptive threshold → deskew
- Heading detection (`#`, ALL CAPS), bullet detection (`•`, `-`, `1.`), L/C/R alignment, bold via font height
- Stack: Python · Tesseract 5.4 · OpenCV 4.13 · python-docx · Streamlit
- ✅ Deployed live on Streamlit Cloud
- ✅ Phase 1 verified with 12-point test suite

**RIGHT COLUMN (orange tint) — "Where Phase 1 Falls Short ⚠️":**
- **Static logic** — same pipeline for every image (good or bad)
- **No autonomy** — user must pick all settings manually
- **No memory** — every session starts from scratch
- **No explanation** — black-box formatting decisions
- **No learning** — never improves over time

**Bottom strip (full-width, navy):** *"Phase 1 = Tool. Phase 2 = Agent. We had to evolve."*

**IMAGE PROMPT:** *A split-screen illustration: left side shows a simple linear conveyor belt with a document moving through fixed gears (representing static Phase 1); right side shows a glowing neural agent brain with multiple feedback loops and decision arrows (representing dynamic Phase 2). Dark navy background, electric blue and amber accents, isometric infographic style.*

---

## ✅ SLIDE 3 — Computing as a Profession + Ethics vs Morals

**Gamma Prompt:**

Create a slide titled **"Building Software is a Professional Responsibility"** with a **3-card top row** + a **2-column bottom comparison**.

**TOP — Three Responsibility Pillars (icon cards):**
1. 👥 **USERS** — Their documents pass through our app. Wrong OCR = wasted time + lost trust.
2. 🌍 **SOCIETY** — Tools democratize digitization. Poor quality widens the digital divide.
3. 🔒 **DATA** — Users trust us with personal/academic content. We must protect it.

**BOTTOM — Morals vs Ethics:**
| 💭 Morals (Personal) | ⚖️ Ethics (Professional) |
|---|---|
| "I feel uncomfortable storing user data" | Don't store user data — required by GDPR mindset |
| "I think free software is good" | Used Apache 2.0 / MIT licensed dependencies — properly attributed |
| Subjective, varies by person | Codified, applies to all professionals |

**Bottom callout box:** *Our SmartDoc OCR design follows **professional responsibility**, not personal convenience: quality > speed, privacy > features, transparency > simplicity.*

**IMAGE PROMPT:** *A professional balance scale held by glowing digital hands. On the left side: a heart symbol (morals/personal). On the right side: a shield with a checkmark (ethics/professional). Dark navy background, blue and gold light, photorealistic 3D render with soft glow, clean editorial style.*

---

## ✅ SLIDE 4 — Professional Ethics + ACM/IEEE Code Applied

**Gamma Prompt:**

Create a slide titled **"How SmartDoc OCR Honors the ACM & IEEE Code of Ethics"** with a **table layout** + a quality/security/safety side panel.

**MAIN TABLE:**
| Principle | Code | Where We Applied It |
|---|---|---|
| 🌟 Public Interest | ACM 1.1 | Free, open-source tool — helps students & professionals globally |
| 💎 High Quality | ACM 2.1 | 6-stage preprocessing + 12-point verification suite + multi-PSM OCR |
| 🔐 Privacy | ACM 1.6 | Session-only processing, zero persistence, no tracking |
| 🤝 Honesty | ACM 1.3 | Confidence scores displayed, limits disclosed (handwriting accuracy) |
| 🎯 Competence | IEEE 6 | Tesseract 5.4, OpenCV 4.13, EasyOCR — all proven, audited libraries |

**RIGHT PANEL — Built-in Safeguards:**
- **Code:** Modular `utils.py` shared between Phase 1 & 2
- **Security:** File-type validation (jpg/png/bmp/tiff only), 100 MB cap, HTTPS via Streamlit Cloud
- **Safety:** Confidence warnings (<50% red, <70% yellow, ≥70% green); audit log downloadable; human override at every step

**Footer:** *"We don't just follow the code — we engineered our system to enforce it."*

**IMAGE PROMPT:** *A glowing geometric shield with the IEEE and ACM logos floating in front of it, surrounded by orbiting holographic icons (lock, eye, checkmark, code brackets). Dark navy background with electric blue light rays, modern tech illustration style, high detail.*

---

## ✅ SLIDE 5 — Ethical Theories + Our Real Decision (Speed vs Quality)

**Gamma Prompt:**

Create a slide titled **"Ethics in Action — A Real Decision From Our Project"** with **two horizontal sections**.

**TOP SECTION — Ethical Lenses Applied:**
- 📊 **Utilitarianism** *(greatest good for greatest number)*: Free deployment + 6-stage preprocessing benefits ALL users regardless of image quality → ✅ adopted
- 📜 **Deontology** *(duty-based)*: We have a DUTY to deliver accurate output and protect user data — non-negotiable → ✅ adopted
- 🧠 **Human-Centered Design**: User overrides agent, sees confidence, controls download → ✅ embedded

**BOTTOM SECTION — The Real Decision We Made:**

> **Decision: Speed vs Quality in Preprocessing**

| Option | Time | Accuracy | Verdict |
|---|---|---|---|
| ❌ Direct Tesseract on raw image | ~0.5 s | 40–50% | **Rejected** — too unreliable for users |
| ✅ 6-stage preprocessing pipeline | ~3–5 s | **65–75%** *(measured on test set)* | **Adopted** — user accuracy > developer convenience |

**Bottom highlight:** *Ethical principle: "The interests of the user outweigh our convenience as developers."*

**IMAGE PROMPT:** *A philosopher's hand drawing a glowing decision tree on a transparent digital interface. Two paths diverge — one labeled "Fast" leading to a broken document icon, the other labeled "Quality" leading to a clean Word document. Dark navy background, blue cinematic lighting, semi-realistic conceptual illustration.*

---

## ✅ SLIDE 6 — 4-Step Ethical Decision Process + Industry-Grade Practices

**Gamma Prompt:**

Create a slide titled **"From Ethical Theory → Industry-Standard Practice"** with a **4-step horizontal flowchart on top** and a **side-by-side comparison below**.

**TOP — 4-Step Ethical Process (real example: "Should we store user images for training?"):**
1. **Identify Issue** → Users upload sensitive academic/personal documents
2. **Analyze Stakeholders** → Users want privacy · Developers want training data · Regulators (PECA 2016, GDPR) require consent
3. **Evaluate Alternatives** → A) Store silently ❌  B) Ask consent ⏳ (future)  C) Session-only ✅
4. **Justified Decision** → **Zero persistence**. No consent needed = no violation. Stated clearly in UI.

**BOTTOM — Student Project vs Industry Software House:**
| Practice | Our Project | Industry Standard | Our Status |
|---|---|---|---|
| Version control | Git + GitHub | Git + CI/CD | ✅ Met |
| Code review | Peer review | Formal PR + tests | ✅ Adapted |
| Modular architecture | utils.py shared | Microservices | ✅ Met |
| Reproducibility | requirements.txt + packages.txt | Docker + IaC | ✅ Met |
| AI ethics | Confidence shown, limits disclosed | Formal review board | ✅ Adapted |

**IMAGE PROMPT:** *A clean 4-step flowchart rendered as glowing connected hexagonal nodes, each containing a different icon (magnifier, people, scales, checkmark). Below it, a split scene of a student team coding vs a corporate office. Dark navy background, neon blue connecting lines, modern infographic style.*

---

## ✅ SLIDE 7 — Legal Framework: PECA 2016, GDPR & IPR

**Gamma Prompt:**

Create a slide titled **"Legal Compliance — Pakistani & Global Standards"** with **3 stacked sections**.

**SECTION 1 — Data Protection (GDPR mindset + PECA 2016):**
- 🔒 In-memory processing only — no DB, no logs of content
- 🇵🇰 **PECA 2016 §3** (unauthorized access): no user accounts, no data retained
- 🇵🇰 **PECA 2016 §9** (data damage): we don't modify originals, only read
- 🇪🇺 **GDPR data minimization**: collect zero personal data → automatically compliant

**SECTION 2 — Intellectual Property (IPR):**
| Library | License | Status |
|---|---|---|
| Tesseract OCR | Apache 2.0 | ✅ Attributed |
| OpenCV | Apache 2.0 | ✅ Attributed |
| python-docx | MIT | ✅ Attributed |
| Streamlit | Apache 2.0 | ✅ Attributed |
| EasyOCR | Apache 2.0 | ✅ Attributed |

Our code: original work by [Team] · MIT licensed · public on GitHub.

**SECTION 3 — IPR Violations We Avoided:**
- ❌ Did NOT use proprietary APIs (Adobe, ABBYY) without licenses
- ❌ Did NOT copy code without understanding/attribution
- ❌ Did NOT scrape paid datasets

**IMAGE PROMPT:** *A digital legal gavel striking a holographic globe surrounded by floating document icons and shield icons. Pakistan flag and EU flag visible as small accents. Dark navy background, gold and blue light, semi-realistic cinematic style.*

---

## ✅ SLIDE 8 — Computer Crimes, Contracts & Risk Mitigation

**Gamma Prompt:**

Create a slide titled **"Risks, Contracts & How We Mitigate Them"** with a **risk matrix table** and a **right-side contracts panel**.

**LEFT — Risk Matrix:**
| Risk | Likelihood | Our Mitigation |
|---|---|---|
| 📂 Data theft of uploads | Low | Session-only, HTTPS, no storage |
| ©️ User uploads copyrighted material | Medium | T&C disclaim; cannot prevent technically |
| 🦠 Malicious file disguised as image | Low | File-type validation + 100 MB cap |
| 📉 OCR misread → wrong document | Medium | Confidence scores + warnings + user review |
| 🕵️ Code theft | Low | MIT license enforces attribution |

**RIGHT — Implicit Terms of Service:**
- ✅ You accept OCR is not 100% accurate (especially handwriting)
- ✅ You will not upload copyrighted/illegal content
- ✅ You understand processing is in-memory only
- ❌ You will not reverse-engineer/attack the service

**WHAT WE PROMISE BACK:**
- Process in memory only — never stored
- Display confidence so you know when to verify
- Maintain service & fix vulnerabilities responsibly
- Attribute all open-source dependencies

**Footer analogy:** *"Like a photocopying shop — we copy your document, we don't keep a copy, and we're not liable for what you copied."*

**IMAGE PROMPT:** *A digital fortress with multiple glowing shield layers protecting a central document icon. Around it, blocked attack vectors are shown as red lines being deflected. Dark navy background, blue and red contrast lighting, modern cybersecurity illustration style.*

---

## ✅ SLIDE 9 — IT Trends, Agentic Era & Career Impact

**Gamma Prompt:**

Create a slide titled **"We're Building for the Agentic Era — And Building Our Careers"** with a **horizontal timeline on top** and a **3-column career skills section below**.

**TOP — AI Evolution Timeline:**
2015 — Rule-based systems → 2018 — ML classifiers → 2021 — LLMs (GPT-3) → **2023 — Autonomous agents** → **2025+ Multi-agent systems**

⭐ **Where SmartDoc OCR sits:** Phase 1 = 2015 era (rule-based) · **Phase 2 = 2023+ era (autonomous agent with memory & feedback)**

**BOTTOM — Skills Gained (3 columns):**

| 💻 Technical (in-demand 2026) | 🤝 Professional | 🎯 AI-Era |
|---|---|---|
| Computer Vision (OpenCV) | Ethical reasoning | Agent architectures |
| OCR engineering (Tesseract + EasyOCR) | Documentation | Human-in-the-loop design |
| Agent design loops | Problem solving | Explainable AI |
| Cloud deployment (Streamlit Cloud) | Git workflow | Memory + learning systems |
| Python OOP & modular code | Team collaboration | Multi-PSM strategy selection |

**Bottom strip:** *"Every major tech company is hiring **AI Agent Engineers** in 2025–2026. This project is our portfolio entry point."*

**IMAGE PROMPT:** *A futuristic timeline visualization with five glowing waypoint markers across a horizontal beam, each emitting a different colored light (representing AI eras). A young engineer silhouette stands at the "2023+" marker holding a glowing laptop. Dark navy space background, blue-to-purple gradient, sci-fi infographic style.*

---

## ✅ SLIDE 10 — Virtual Work, Sustainability & Green Computing

**Gamma Prompt:**

Create a slide titled **"Building Remotely · Building Responsibly · Building Green"** with **two columns**.

**LEFT — Virtual Collaboration:**
- 🌐 **GitHub** = full audit trail of every commit
- 🕒 Asynchronous work — no need to be in same room
- 💬 Issues + PR comments = remote code review
- 📝 Commit history = transparent record of who built what
- ⚖️ Modular task division (preprocessing / OCR / agents / UI)

**RIGHT — Green Computing Choices:**
| Choice | Eco-Impact |
|---|---|
| `opencv-python-headless` (no GUI) | Less RAM = less energy |
| Streamlit Cloud (serverless) | Resources used only when active |
| Session-only processing | No idle DB load |
| Adaptive preprocessing | Heavy work only when needed (quality < 65) |
| On-demand deployment | No always-on backend 24/7 |

**Bottom callout:** *Compared to an always-on GPU server, our serverless on-demand architecture uses **~100× less energy**. Efficient code is green code.*

**IMAGE PROMPT:** *A glowing green leaf emerging from a server rack, with subtle network lines connecting to a cloud icon and laptop icons in different geographic locations. Dark navy background, emerald green and electric blue accents, modern eco-tech illustration.*

---
x