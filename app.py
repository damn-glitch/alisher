import streamlit as st
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json, re, io, os
from typing import Dict, Any, List, Tuple, Optional

# =========================================
# PAGE CONFIG
# =========================================
st.set_page_config(
    page_title="Alisher Beisembekov | Polymath",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================
# SESSION STATE
# =========================================
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"
if "profile" not in st.session_state:
    st.session_state.profile = {}

# =========================================
# UTILS: PDF/JSON IMPORT + PARSING
# =========================================
def _read_pdf_text(file_bytes: bytes) -> str:
    """
    Reads PDF text using PyPDF2/pypdf if available; falls back to simple bytes -> no-op.
    """
    try:
        from PyPDF2 import PdfReader  # pypdf-compatible API
        reader = PdfReader(io.BytesIO(file_bytes))
        pages = []
        for p in reader.pages:
            try:
                pages.append(p.extract_text() or "")
            except Exception:
                pages.append("")
        return "\n".join(pages)
    except Exception:
        # As a fallback, try to decode bytes (will not be useful for real PDFs but keeps app robust)
        try:
            return file_bytes.decode("utf-8", errors="ignore")
        except Exception:
            return ""

HEADER_SYNONYMS = {
    "about":       ["ABOUT", "SUMMARY", "PROFILE", "ОБО МНЕ", "О СЕБЕ", "ПРО МЕНЯ", "ПРОФИЛЬ"],
    "skills":      ["SKILLS", "НАВЫКИ", "КОМПЕТЕНЦИИ", "STACK", "TECH SKILLS", "SOFT SKILLS"],
    "experience":  ["EXPERIENCE", "WORK EXPERIENCE", "CAREER", "ОПЫТ", "ОПЫТ РАБОТЫ", "КАРЬЕРА"],
    "projects":    ["PROJECTS", "ПРОЕКТЫ", "ПОРТФОЛИО"],
    "education":   ["EDUCATION", "ОБРАЗОВАНИЕ"],
    "publications":["PUBLICATIONS", "ПУБЛИКАЦИИ", "СТАТЬИ", "ПАПЕРЫ"],
    "awards":      ["AWARDS", "НАГРАДЫ", "ДОСТИЖЕНИЯ", "РЕКОГНИШН"],
    "languages":   ["LANGUAGES", "ЯЗЫКИ"],
    "contacts":    ["CONTACTS", "CONTACT", "КОНТАКТЫ"],
    "socials":     ["SOCIALS", "LINKS", "СОЦСЕТИ", "СОЦИАЛЬНЫЕ СЕТИ", "ССЫЛКИ"],
    "patents":     ["PATENTS", "ПАТЕНТЫ"],
    "speaking":    ["SPEAKING", "ДОКЛАДЫ", "ВЫСТУПЛЕНИЯ", "TALKS", "КОНФЕРЕНЦИИ"],
    "media":       ["MEDIA", "PRESS", "СМИ"],
}

def _normalize(text: str) -> str:
    text = text.replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    # unify bullets
    text = text.replace("•", "- ").replace("–", "- ").replace("—", "- ")
    return text

def _is_header(line: str) -> Tuple[bool, Optional[str]]:
    raw = line.strip().strip(":").upper()
    for key, variants in HEADER_SYNONYMS.items():
        for v in variants:
            if raw == v or raw.startswith(v + " "):
                return True, key
    # Markdown-like
    if re.match(r"^#{1,3}\s+\S+", line.strip()):
        return True, None
    return False, None

def _split_sections(text: str) -> Dict[str, str]:
    """
    Roughly split into sections by known headers.
    Returns dict section_key -> text.
    Unknown blocks go into 'about' if empty, else appended to 'about'.
    """
    lines = text.splitlines()
    current_key = None
    sections: Dict[str, List[str]] = {}
    for line in lines:
        is_hdr, key = _is_header(line)
        if is_hdr and key:
            current_key = key
            sections.setdefault(current_key, [])
            continue
        if is_hdr and not key:
            # unknown header shape -> stash to about separator
            current_key = "about"
            sections.setdefault(current_key, [])
            continue
        # ordinary line
        if current_key is None:
            current_key = "about"
            sections.setdefault(current_key, [])
        sections[current_key].append(line)

    return {k: _normalize("\n".join(v)).strip() for k, v in sections.items()}

def _split_items(block: str) -> List[str]:
    """
    Split a text block into bullet-like items.
    """
    if not block:
        return []
    # First split by double newline to isolate paragraphs
    parts = [p.strip() for p in re.split(r"\n\s*\n", block) if p.strip()]
    items: List[str] = []
    for p in parts:
        # If paragraph already looks like a list, split by lines that start with '- '
        bullets = [ln.strip()[2:].strip() for ln in p.split("\n") if ln.strip().startswith("- ")]
        if bullets:
            items.extend(bullets)
        else:
            items.append(p)
    # De-duplicate, keep order
    seen = set()
    uniq = []
    for it in items:
        key = it.lower()
        if key not in seen:
            uniq.append(it)
            seen.add(key)
    return uniq

def _guess_name(text: str) -> str:
    """
    Try to guess a name: a line with 2–3 capitalized words early in the doc.
    """
    for line in text.splitlines()[:20]:
        s = line.strip()
        if 4 <= len(s) <= 80:
            # 2–4 words starting with uppercase letters (RU/EN)
            if re.match(r"^([A-ZА-ЯЁ][A-Za-zА-Яа-яё\-']+\s+){1,3}[A-ZА-ЯЁ][A-Za-zА-Яа-яё\-']+$", s):
                return s
    return "Alisher Beisembekov"

def _extract_contacts(block: str) -> Dict[str, str]:
    d = {}
    if not block:
        return d
    email = re.search(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}", block)
    phone = re.search(r"(\+?\d[\d \-()]{7,}\d)", block)
    if email: d["email"] = email.group(0)
    if phone: d["phone"] = phone.group(0)
    # simple location guess
    loc = re.search(r"(?:Location|Город|City|Страна|Country)[:\s]+([^\n]+)", block, re.IGNORECASE)
    if loc: d["location"] = loc.group(1).strip()
    return d

def _extract_socials(block: str) -> Dict[str, str]:
    d = {}
    if not block:
        return d
    urls = re.findall(r"(https?://[^\s]+)", block)
    for u in urls:
        if "linkedin" in u: d["LinkedIn"] = u
        elif "github" in u: d["GitHub"] = u
        elif "t.me" in u or "telegram" in u: d["Telegram"] = u
        elif "twitter" in u or "x.com" in u: d["Twitter"] = u
        elif "instagram" in u: d["Instagram"] = u
        else:
            # keep first other link as Portfolio
            d.setdefault("Website", u)
    return d

def _parse_experience(block: str) -> List[Dict[str, Any]]:
    """
    Very robust but heuristic parser. Accepts bullet lines or paragraphs.
    Format examples recognized:
      - Senior ML Engineer — Company (2022–Present): did X, Y, Z...
      - Company — Title (2019–2021)  Achievements: ...
    """
    items = _split_items(block)
    res = []
    for it in items:
        title = company = period = ""
        # pattern 1: Title — Company (YYYY–YYYY|Present)
        m = re.search(r"^(?P<title>[^–—\-()]+)\s*[–—\-]\s*(?P<company>[^()]+?)\s*\((?P<period>[^)]+)\)", it)
        if not m:
            # pattern 2: Company — Title (YYYY–YYYY)
            m = re.search(r"^(?P<company>[^–—\-()]+)\s*[–—\-]\s*(?P<title>[^()]+?)\s*\((?P<period>[^)]+)\)", it)
        if m:
            title = m.group("title").strip()
            company = m.group("company").strip()
            period = m.group("period").strip()
        else:
            # fallback: first sentence -> title, second -> company/period
            lines = [ln.strip() for ln in re.split(r"[.;]\s+|\n", it) if ln.strip()]
            if lines:
                title = lines[0]
            if len(lines) > 1:
                company = lines[1]
            # period guess
            pm = re.search(r"(20\d{2}\s*[–\-]\s*(?:20\d{2}|Present|н\.в\.))", it, re.IGNORECASE)
            if pm: period = pm.group(1)

        # achievements: split by " - " lines after the header part
        ach = []
        sub = it
        head = f"{title} — {company}" if (title and company) else (title or company)
        if head:
            idx = it.find(head)
            if idx >= 0:
                sub = it[idx + len(head):]
        ach = [s.strip() for s in re.findall(r"-\s+(.+)", sub)] or []
        res.append({
            "title": title or "Role",
            "company": company or "Company",
            "period": period or "",
            "description": it.strip()[:300],
            "achievements": ach[:6]
        })
    return res

def _parse_projects(block: str) -> List[Dict[str, Any]]:
    items = _split_items(block)
    res = []
    for it in items:
        # Extract name (before colon) and description
        name = it.split(":")[0].split("—")[0].strip()
        desc = it[len(name):].lstrip(":—- ").strip()
        # status guess
        status = "Production" if re.search(r"\b(prod|production|запуск|live)\b", it, re.IGNORECASE) else \
                 "Beta" if re.search(r"\bbeta|pilot|пилот\b", it, re.IGNORECASE) else "Research"
        # collect tech tags (#word or [Tech])
        tech = re.findall(r"#([A-Za-z0-9_+\-/.]+)", it)
        if not tech:
            tech = re.findall(r"\[([^\]]+)\]", it)[:10]
        res.append({
            "name": name or "Project",
            "category": "",
            "status": status,
            "description": desc or it[:250],
            "tech": tech[:8],
            "metrics": {},
            "color": "#667eea"
        })
    return res[:12]

def _parse_publications(block: str) -> List[Dict[str, Any]]:
    items = _split_items(block)
    pubs = []
    for it in items:
        year = 0
        ym = re.search(r"(20\d{2})", it)
        if ym: year = int(ym.group(1))
        journal = ""
        jm = re.search(r"[\“\"']([^\"”']+)[\”\"']|\b(in|в)\s+([A-Z][A-Za-z\s&\-]+)", it)
        if jm:
            # either quoted title -> not journal, or "in Journal"
            if jm.group(1):
                journal = ""
            elif jm.group(3):
                journal = jm.group(3).strip()
        title = it
        pubs.append({
            "title": title,
            "journal": journal,
            "year": year or datetime.now().year,
            "citations": 0,
            "impact": 0.0
        })
    return pubs[:20]

def _parse_awards(block: str) -> List[Dict[str, Any]]:
    items = _split_items(block)
    res = []
    for it in items:
        year = 0
        ym = re.search(r"(20\d{2})", it)
        if ym: year = int(ym.group(1))
        # split by " — " or ":"
        parts = re.split(r"\s[—\-:]\s", it, maxsplit=1)
        title = parts[0].strip()
        desc = parts[1].strip() if len(parts) > 1 else it
        res.append({
            "title": title,
            "org": "",
            "year": year or datetime.now().year,
            "category": "",
            "description": desc
        })
    return res[:20]

def _parse_languages(block: str) -> List[str]:
    if not block:
        return []
    # split by comma or newline
    langs = re.split(r"[,/;\n]", block)
    return [l.strip(" .•-") for l in langs if l.strip()]

def _parse_skills(block: str) -> Dict[str, List[str]]:
    items = _split_items(block)
    # classify roughly
    tech, lead, res = [], [], []
    for it in items:
        # split possible comma-separated lists
        parts = re.split(r"[,/;•]", it)
        parts = [p.strip() for p in parts if p.strip()]
        for p in parts:
            pl = p.lower()
            if any(k in pl for k in ["lead", "team", "manage", "mentor", "владение людьми", "руковод", "лидер"]):
                lead.append(p)
            elif any(k in pl for k in ["research", "science", "науч", "исслед", "paper"]):
                res.append(p)
            else:
                tech.append(p)
    # dedup
    def ded(x): 
        seen=set(); out=[]
        for i in x:
            if i.lower() not in seen:
                out.append(i); seen.add(i.lower())
        return out
    return {
        "Technology": ded(tech)[:24],
        "Leadership": ded(lead)[:16],
        "Research":   ded(res)[:16],
    }

def parse_profile_from_text(text: str) -> Dict[str, Any]:
    text = _normalize(text)
    sections = _split_sections(text)

    profile: Dict[str, Any] = {
        "name": _guess_name(text),
        "headline": "",
        "about": sections.get("about", ""),
        "contacts": _extract_contacts(sections.get("contacts", "")),
        "socials": _extract_socials(sections.get("socials", sections.get("contacts", ""))),
        "skills": _parse_skills(sections.get("skills", "")),
        "languages": _parse_languages(sections.get("languages", "")) or ["Русский", "Казахский", "English"],
        "positions_current": [],
        "career": _parse_experience(sections.get("experience", "")),
        "projects": _parse_projects(sections.get("projects", "")),
        "research_areas": [],  # можно дополнить вручную
        "publications": _parse_publications(sections.get("publications", "")),
        "awards": _parse_awards(sections.get("awards", "")),
        "achievements_other": [],
        "analytics": {},
        "raw_import_preview": text[:50000],
    }

    # Текущие позиции: возьмём из карьеры все с "Present/н.в."
    current = [c for c in profile["career"] if re.search(r"(Present|н\.в\.)", c.get("period",""), re.IGNORECASE)]
    profile["positions_current"] = current[:3]

    # Headline — короткая выжимка из about
    if profile["about"]:
        profile["headline"] = (profile["about"].split("\n")[0] or "").strip()[:140]

    # achievements_other (патенты/доклады/медиа), если такие секции есть
    other_blocks = []
    if sections.get("patents"):
        other_blocks.append({"title":"Patents", "icon":"📋", "items": _split_items(sections["patents"])})
    if sections.get("speaking"):
        other_blocks.append({"title":"Speaking Engagements", "icon":"🎤", "items": _split_items(sections["speaking"])})
    if sections.get("media"):
        other_blocks.append({"title":"Media Features", "icon":"📰", "items": _split_items(sections["media"])})

    profile["achievements_other"] = other_blocks

    return profile

def merge_profile(base: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deep merge: new overrides base; lists are replaced if non-empty.
    """
    out = dict(base)
    for k, v in new.items():
        if isinstance(v, dict):
            out[k] = merge_profile(out.get(k, {}), v)
        elif isinstance(v, list):
            out[k] = v if v else out.get(k, [])
        elif v not in (None, ""):
            out[k] = v
    return out

def default_profile() -> Dict[str, Any]:
    # Conservative defaults (визуально гармоничные, без выдуманных заслуг)
    return {
        "name": "Alisher Beisembekov",
        "headline": "Polymath • Innovator • Visionary",
        "about": "Brief summary about you. Upload PDF/JSON to overwrite.",
        "contacts": {},
        "socials": {},
        "skills": {
            "Technology": ["AI/ML", "Python", "Cloud"],
            "Leadership": ["Strategy", "Product", "Mentorship"],
            "Research":   ["Publications", "Patents"]
        },
        "languages": ["Русский", "Казахский", "English"],
        "positions_current": [],
        "career": [],
        "projects": [],
        "research_areas": [],
        "publications": [],
        "awards": [],
        "achievements_other": [],
        "analytics": {
            "lifetime_stats": [
                ("Projects", "—", "💡", ""),
                ("Publications", "—", "📚", ""),
                ("Awards", "—", "🏆", ""),
                ("Students Mentored", "—", "🎓", ""),
            ],
            "growth": {
                "years": [2019, 2020, 2021, 2022, 2023, 2024],
                "projects": [2, 4, 7, 12, 18, 24],
                "publications": [0, 1, 3, 6, 9, 12],
                "team_size": [1, 3, 6, 10, 15, 22],
            },
            "skills_distribution": {"AI/ML":80, "Cloud":70, "Leadership":75, "Research":65}
        }
    }

def compute_dynamic_stats(profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Построить метрики из профиля: counts и графики
    """
    pubs = len(profile.get("publications", []))
    projs = len(profile.get("projects", []))
    awards = len(profile.get("awards", []))
    patents_cnt = 0
    for cat in profile.get("achievements_other", []):
        if cat.get("title","").lower().startswith("patent"):
            patents_cnt = len(cat.get("items", []))
    lifetime_stats = [
        ("Patents", str(patents_cnt) if patents_cnt else "—", "📋", ""),
        ("Publications", str(pubs) if pubs else "—", "📚", ""),
        ("Projects", str(projs) if projs else "—", "💡", ""),
        ("Awards", str(awards) if awards else "—", "🏆", ""),
    ]
    out = dict(profile.get("analytics", {}))
    out["lifetime_stats"] = lifetime_stats
    # keep growth & skills if present
    if "growth" not in out:
        out["growth"] = default_profile()["analytics"]["growth"]
    if "skills_distribution" not in out:
        # aggregate from profile.skills
        sd = {}
        for cat, arr in profile.get("skills", {}).items():
            sd[cat] = min(95, 60 + len(arr) * 2)
        out["skills_distribution"] = sd or default_profile()["analytics"]["skills_distribution"]
    return out

def import_profile_from_uploader(uploaded_file) -> Optional[Dict[str, Any]]:
    if uploaded_file is None:
        return None
    name = uploaded_file.name.lower()
    if name.endswith(".json"):
        try:
            data = json.load(uploaded_file)
            return data
        except Exception:
            st.error("Не удалось прочитать JSON. Проверьте формат.")
            return None
    if name.endswith(".pdf"):
        try:
            text = _read_pdf_text(uploaded_file.read())
            prof = parse_profile_from_text(text)
            return prof
        except Exception:
            st.error("Не удалось извлечь текст из PDF.")
            return None
    st.warning("Поддерживаются файлы .pdf и .json")
    return None

def try_autoload_from_path(path: str = "/mnt/data/All info alish.pdf") -> Optional[Dict[str, Any]]:
    try:
        if os.path.exists(path):
            with open(path, "rb") as f:
                text = _read_pdf_text(f.read())
            return parse_profile_from_text(text)
    except Exception:
        pass
    return None

# =========================================
# CSS
# =========================================
def load_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        * { font-family: 'Inter', sans-serif; }
        .stApp { background: linear-gradient(135deg, #0F0C29 0%, #302B63 50%, #24243e 100%); background-attachment: fixed; }
        #MainMenu {visibility: hidden;} footer {visibility: hidden;}
        section[data-testid="stSidebar"] { background: rgba(15, 12, 41, 0.8); backdrop-filter: blur(20px); border-right: 1px solid rgba(255, 255, 255, 0.1); }
        section[data-testid="stSidebar"] .stButton > button {
            background: rgba(255, 255, 255, 0.05); color: rgba(255, 255, 255, 0.9);
            border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 15px; padding: 15px; width: 100%;
            transition: all 0.3s ease; font-weight: 500; margin-bottom: 10px;
        }
        section[data-testid="stSidebar"] .stButton > button:hover {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.3) 0%, rgba(118, 75, 162, 0.3) 100%);
            border: 1px solid rgba(255, 255, 255, 0.3); transform: translateX(5px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }
        .animated-bg { position: fixed; width: 100%; height: 100%; top: 0; left: 0; z-index: -1;
            background: linear-gradient(270deg, #0F0C29, #302B63, #24243e, #0F0C29); background-size: 800% 800%; animation: gradientShift 20s ease infinite; }
        @keyframes gradientShift { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
        .glass-card { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1); padding: 30px; margin: 20px 0; box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37); transition: all 0.3s ease; }
        .glass-card:hover { transform: translateY(-5px); box-shadow: 0 15px 35px 0 rgba(31, 38, 135, 0.5); border: 1px solid rgba(255, 255, 255, 0.2); }
        .hero-name { font-family: 'Space Grotesk', sans-serif; font-size: clamp(3rem, 8vw, 6rem); font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 20%, #f093fb 40%, #f5576c 60%, #fda085 80%, #667eea 100%);
            background-size: 200% 200%; -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; animation: gradientText 5s ease infinite;
            letter-spacing: -0.02em; line-height: 1.1; margin-bottom: 0; }
        @keyframes gradientText { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
        .hero-title { font-family: 'Space Grotesk', sans-serif; font-size: clamp(1.2rem, 3vw, 1.8rem); color: rgba(255, 255, 255, 0.9);
            text-align: center; margin-top: 10px; letter-spacing: 0.2em; text-transform: uppercase; font-weight: 300; }
        .metric-card { background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%); backdrop-filter: blur(10px); border-radius: 16px; padding: 25px;
            text-align: center; border: 1px solid rgba(255, 255, 255, 0.1); transition: all 0.3s ease; }
        .metric-card:hover { transform: translateY(-5px) scale(1.02); border: 1px solid rgba(255, 255, 255, 0.3); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3); }
        .metric-number { font-size: 2.5rem; font-weight: 700; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 5px; }
        .metric-label { color: rgba(255, 255, 255, 0.7); font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.1em; }
        .section-header { font-family: 'Space Grotesk', sans-serif; font-size: clamp(2rem, 4vw, 3rem); font-weight: 600;
            background: linear-gradient(135deg, #fff 0%, rgba(255,255,255,0.7) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            margin: 40px 0 30px 0; position: relative; padding-bottom: 15px; }
        .section-header:after { content: ''; position: absolute; bottom: 0; left: 0; width: 100px; height: 3px; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); border-radius: 2px; }
        .achievement-card { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(10px); border-radius: 16px; padding: 25px; margin-bottom: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1); transition: all 0.3s ease; position: relative; overflow: hidden; }
        .achievement-card:before { content: ''; position: absolute; top: 0; left: -100%; width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent); transition: left 0.5s ease; }
        .achievement-card:hover:before { left: 100%; }
        .achievement-card:hover { transform: translateX(5px); border: 1px solid rgba(255, 255, 255, 0.2); box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3); }
        .skill-tag { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1); color: rgba(255, 255, 255, 0.9);
            padding: 12px 20px; border-radius: 25px; text-align: center; font-weight: 500; transition: all 0.3s ease; cursor: default; display: inline-block; margin: 5px; }
        .skill-tag:hover { background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%); transform: translateY(-3px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3); border: 1px solid rgba(255, 255, 255, 0.3); }
        .floating { animation: float 6s ease-in-out infinite; } @keyframes float { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-20px); } }
        .glow { box-shadow: 0 0 30px rgba(102, 126, 234, 0.6), 0 0 60px rgba(102, 126, 234, 0.4), 0 0 90px rgba(102, 126, 234, 0.2); }
        ::-webkit-scrollbar { width: 10px; } ::-webkit-scrollbar-track { background: rgba(255, 255, 255, 0.05); }
        ::-webkit-scrollbar-thumb { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 5px; }
        ::-webkit-scrollbar-thumb:hover { background: linear-gradient(135deg, #764ba2 0%, #667eea 100%); }
        .text-gradient { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .text-white { color: rgba(255, 255, 255, 0.9); } .text-muted { color: rgba(255, 255, 255, 0.6); }
        .sidebar-header { color: white; text-align: center; padding: 20px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 20px; }
        .sidebar-name { font-family: 'Space Grotesk', sans-serif; font-size: 1.5rem; font-weight: 600; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 5px; }
        .sidebar-title { color: rgba(255, 255, 255, 0.7); font-size: 0.9rem; letter-spacing: 0.1em; }
    </style>
    <div class="animated-bg"></div>
    """, unsafe_allow_html=True)

load_css()

# =========================================
# SIDEBAR NAV + IMPORT/EXPORT
# =========================================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <div class="sidebar-name">Alisher Beisembekov</div>
        <div class="sidebar-title">Portfolio Navigation</div>
    </div>
    """, unsafe_allow_html=True)

    # Import Profile
    st.markdown("### 📥 Импорт профиля")
    uploaded = st.file_uploader("Загрузите PDF (например, All info alish.pdf) или JSON", type=["pdf", "json"])
    if uploaded is not None:
        prof_new = import_profile_from_uploader(uploaded)
        if prof_new:
            st.session_state.profile = merge_profile(default_profile(), prof_new)
            st.success("Профиль импортирован!")

    # Try autoload from path (first run)
    if not st.session_state.profile:
        auto = try_autoload_from_path("/mnt/data/All info alish.pdf")
        if auto:
            st.session_state.profile = merge_profile(default_profile(), auto)
            st.info("Профиль автоматически импортирован из /mnt/data/All info alish.pdf")

    # Navigation
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.current_page = "home"
    if st.button("💼 Career", use_container_width=True):
        st.session_state.current_page = "career"
    if st.button("🔬 Research", use_container_width=True):
        st.session_state.current_page = "research"
    if st.button("💻 Projects", use_container_width=True):
        st.session_state.current_page = "projects"
    if st.button("🏆 Achievements", use_container_width=True):
        st.session_state.current_page = "achievements"
    if st.button("📊 Analytics", use_container_width=True):
        st.session_state.current_page = "analytics"

    st.markdown("---")
    # Export Profile
    st.markdown("### 💾 Экспорт профиля")
    prof_to_download = st.session_state.profile or default_profile()
    st.download_button(
        "Скачать profile.json",
        data=json.dumps(prof_to_download, ensure_ascii=False, indent=2),
        file_name="profile.json",
        mime="application/json",
        use_container_width=True
    )

    # Connect (dynamic)
    socials = (st.session_state.profile or {}).get("socials", {})
    if socials:
        st.markdown("""<div style="text-align: center; padding: 10px 0;">
        <p style="color: rgba(255, 255, 255, 0.6); margin-bottom: 10px;">Connect</p>
        <div style="display: flex; justify-content: center; gap: 15px;">""", unsafe_allow_html=True)
        for label, url in socials.items():
            icon = "💼" if "LinkedIn" in label else ("🐱" if "GitHub" in label else ("✈️" if "Telegram" in label else "🌐"))
            st.markdown(f'<a href="{url}" target="_blank" style="color: rgba(255, 255, 255, 0.7); text-decoration: none;">{icon}</a>', unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)
    else:
        st.markdown("""<div style="text-align: center; padding: 20px 0;">
            <p style="color: rgba(255, 255, 255, 0.6); margin-bottom: 15px;">Connect</p>
            <div style="display: flex; justify-content: center; gap: 15px;">
                <a href="#" style="color: rgba(255, 255, 255, 0.7); text-decoration: none;">📧</a>
                <a href="#" style="color: rgba(255, 255, 255, 0.7); text-decoration: none;">💼</a>
                <a href="#" style="color: rgba(255, 255, 255, 0.7); text-decoration: none;">🐦</a>
                <a href="#" style="color: rgba(255, 255, 255, 0.7); text-decoration: none;">📷</a>
            </div>
        </div>""", unsafe_allow_html=True)

# =========================================
# DATA ACCESSORS
# =========================================
PROFILE = merge_profile(default_profile(), st.session_state.profile or {})
PROFILE["analytics"] = compute_dynamic_stats(PROFILE)

# =========================================
# PAGES
# =========================================
def render_home():
    name = PROFILE.get("name", "Alisher Beisembekov")
    headline = PROFILE.get("headline") or "Polymath • Innovator • Visionary"
    about = PROFILE.get("about", "")

    st.markdown(f'<h1 class="hero-name floating">{name}</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="hero-title">{headline}</p>', unsafe_allow_html=True)

    # Quick Stats (dynamic)
    patents_cnt = 0
    for cat in PROFILE.get("achievements_other", []):
        if cat.get("title","").lower().startswith("patent"):
            patents_cnt = len(cat.get("items", []))
    metrics_data = [
        ("Patents", f"{patents_cnt}" if patents_cnt else "—", "📋"),
        ("Publications", str(len(PROFILE.get("publications", []))) or "—", "📚"),
        ("Projects", str(len(PROFILE.get("projects", []))) or "—", "💡"),
        ("Awards", str(len(PROFILE.get("awards", []))) or "—", "🏆"),
    ]
    st.markdown("---")
    cols = st.columns(4)
    for col, (label, value, icon) in zip(cols, metrics_data):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 2rem; margin-bottom: 10px;">{icon}</div>
                <div class="metric-number">{value}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Redefining Possibilities</h2>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        if about:
            st.markdown(f"""
            <p class="text-white" style="font-size: 1.1rem; line-height: 1.8;">{about}</p>
            """, unsafe_allow_html=True)

        # Current Positions
        st.markdown('<h3 class="text-gradient" style="margin-top: 30px;">Current Positions</h3>', unsafe_allow_html=True)
        cur = PROFILE.get("positions_current") or PROFILE.get("career", [])[:3]
        for position in cur:
            st.markdown(f"""
            <div class="achievement-card">
                <h4 class="text-white">{position.get("title","")}</h4>
                <p class="text-gradient" style="font-weight: 600;">{position.get("company","")}</p>
                <p class="text-muted">{position.get("period","")}</p>
                <p class="text-white" style="margin-top: 10px;">{position.get("description","")}</p>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        # Core Expertise
        st.markdown('<h3 class="text-gradient">Core Expertise</h3>', unsafe_allow_html=True)
        skills = PROFILE.get("skills", {})
        for category, arr in skills.items():
            st.markdown(f'<p class="text-white" style="font-weight: 600; margin-top: 20px;">{category}</p>', unsafe_allow_html=True)
            for skill in arr[:12]:
                st.markdown(f'<div class="skill-tag">{skill}</div>', unsafe_allow_html=True)

        # Languages
        st.markdown('<h3 class="text-gradient" style="margin-top: 30px;">Languages</h3>', unsafe_allow_html=True)
        for lang in PROFILE.get("languages", []):
            st.markdown(f'<div class="skill-tag" style="margin: 5px 0;">{lang}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def render_career():
    st.markdown('<h1 class="hero-name">Career Journey</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-title">Professional Evolution</p>', unsafe_allow_html=True)

    positions = PROFILE.get("career", [])
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Professional Timeline</h2>', unsafe_allow_html=True)

    for i, position in enumerate(positions):
        color = "#667eea" if i < 3 else "#764ba2"
        ach_tags = "".join([f'<span class="skill-tag">{a}</span>' for a in (position.get("achievements") or [])])
        st.markdown(f'''
        <div class="achievement-card">
            <div style="display: flex; align-items: start; gap: 20px;">
                <div style="min-width: 60px; height: 60px; background: linear-gradient(135deg, {color} 0%, #764ba2 100%); 
                            border-radius: 15px; display: flex; align-items: center; justify-content: center; color: white; 
                            font-weight: bold; font-size: 1.5rem;">
                    {i+1}
                </div>
                <div style="flex: 1;">
                    <h3 class="text-white">{position.get("title","")}</h3>
                    <p class="text-gradient" style="font-weight: 600; font-size: 1.1rem;">{position.get("company","")}</p>
                    <p class="text-muted">{position.get("period","")}</p>
                    <p class="text-white" style="margin: 15px 0;">{position.get("description","")}</p>
                    <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 15px;">
                        {ach_tags}
                    </div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Career Stats (from analytics.lifetime_stats)
    st.markdown('<h2 class="section-header">Career Impact</h2>', unsafe_allow_html=True)
    stats = PROFILE["analytics"].get("lifetime_stats", [])
    cols = st.columns(4)
    for col, (label, value, icon, growth) in zip(cols, stats[:4]):
        with col:
            st.markdown(f'''
            <div class="metric-card glow">
                <div style="font-size: 2.5rem;">{icon}</div>
                <div class="metric-number">{value}</div>
                <div class="metric-label">{label}</div>
            </div>
            ''', unsafe_allow_html=True)

def render_research():
    st.markdown('<h1 class="hero-name">Research & Innovation</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-title">Advancing the Frontiers of Knowledge</p>', unsafe_allow_html=True)

    areas = PROFILE.get("research_areas", [])
    if areas:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-header">Research Domains</h2>', unsafe_allow_html=True)
        cols = st.columns(2)
        for i, area in enumerate(areas):
            with cols[i % 2]:
                st.markdown(f'''
                <div class="achievement-card">
                    <div style="text-align: center;">
                        <div style="font-size: 4rem; margin-bottom: 15px;">{area.get("icon","🧠")}</div>
                        <h3 class="text-gradient">{area.get("area","")}</h3>
                        <p class="text-white" style="margin: 15px 0;">{area.get("focus","")}</p>
                        <div style="display: flex; justify-content: space-around; margin-top: 20px;">
                            <div>
                                <p class="metric-number" style="font-size: 1.8rem;">{area.get("papers",0)}</p>
                                <p class="text-muted">Papers</p>
                            </div>
                            <div>
                                <p class="metric-number" style="font-size: 1.8rem;">{area.get("citations",0)}</p>
                                <p class="text-muted">Citations</p>
                            </div>
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Selected Publications</h2>', unsafe_allow_html=True)
    publications = PROFILE.get("publications", [])
    for pub in publications:
        st.markdown(f'''
        <div class="achievement-card">
            <h3 class="text-white">{pub.get("title","")}</h3>
            <p class="text-gradient" style="font-weight: 600; margin: 10px 0;">{pub.get("journal","")} • {pub.get("year","")}</p>
            <div style="display: flex; gap: 30px; margin-top: 15px;">
                <span class="text-white">📚 Citations: <strong>{pub.get("citations",0)}</strong></span>
                <span class="text-white">📊 Impact Factor: <strong>{pub.get("impact",0)}</strong></span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    if not publications:
        st.info("Загрузите PDF/JSON с разделом «Publications/Публикации», чтобы показать список работ.")
    st.markdown('</div>', unsafe_allow_html=True)

def render_projects():
    st.markdown('<h1 class="hero-name">Innovation Portfolio</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-title">Building Tomorrow\'s Technology</p>', unsafe_allow_html=True)

    projects = PROFILE.get("projects", [])
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Featured Projects</h2>', unsafe_allow_html=True)
    for project in projects:
        metrics_html = "".join([
            f'<div><p class="text-gradient" style="font-weight: 700; font-size: 1.2rem;">{value}</p>'
            f'<p class="text-muted" style="font-size: 0.9rem;">{key}</p></div>'
            for key, value in (project.get("metrics") or {}).items()
        ])
        tech_html = "".join([f'<span class="skill-tag">{t}</span>' for t in project.get("tech", [])])
        st.markdown(f'''
        <div class="achievement-card">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div style="flex: 1;">
                    <h3 class="text-white">{project.get("name","")}</h3>
                    <span style="background: {project.get("color","#00ff88")}; color: #000; padding: 5px 15px; 
                                border-radius: 20px; font-weight: 600; font-size: 0.9rem; 
                                display: inline-block; margin: 10px 0;">
                        {project.get("status","")}
                    </span>
                    <p class="text-gradient" style="font-weight: 600; margin: 10px 0;">{project.get("category","")}</p>
                    <p class="text-white" style="margin: 15px 0;">{project.get("description","")}</p>
                    <div style="margin: 20px 0;">
                        <p class="text-muted" style="margin-bottom: 10px;">Technologies:</p>
                        <div style="display: flex; flex-wrap: wrap; gap: 10px;">{tech_html}</div>
                    </div>
                    <div style="display: flex; gap: 30px; margin-top: 20px;">{metrics_html}</div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    if not projects:
        st.info("Загрузите PDF/JSON с разделом «Projects/Проекты», чтобы показать портфолио.")
    st.markdown('</div>', unsafe_allow_html=True)

def render_achievements():
    st.markdown('<h1 class="hero-name">Achievements & Recognition</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-title">Excellence Across Disciplines</p>', unsafe_allow_html=True)

    awards = PROFILE.get("awards", [])
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Major Awards</h2>', unsafe_allow_html=True)
    if awards:
        for award in awards:
            st.markdown(f'''
            <div class="achievement-card">
                <div style="display: flex; align-items: start; gap: 20px;">
                    <div style="font-size: 3rem;">🏆</div>
                    <div style="flex: 1;">
                        <h3 class="text-white">{award.get("title","")}</h3>
                        <p class="text-gradient" style="font-weight: 600; font-size: 1.1rem;">{award.get("org","")} • {award.get("year","")}</p>
                        <p class="text-muted" style="margin: 10px 0;">{award.get("category","")}</p>
                        <p class="text-white">{award.get("description","")}</p>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
    else:
        st.info("Добавьте раздел «Awards/Награды» в PDF/JSON для отображения.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Other categories
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Additional Recognition</h2>', unsafe_allow_html=True)
    cats = PROFILE.get("achievements_other", [])
    if cats:
        cols = st.columns(2)
        for i, category in enumerate(cats):
            with cols[i % 2]:
                items_html = "".join([f'<li class="text-white" style="margin: 10px 0;">• {item}</li>' for item in category.get("items", [])])
                st.markdown(f'''
                <div class="achievement-card">
                    <div style="text-align: center; margin-bottom: 20px;">
                        <div style="font-size: 3rem;">{category.get("icon","⭐")}</div>
                        <h3 class="text-gradient">{category.get("title","")}</h3>
                    </div>
                    <ul style="list-style: none; padding: 0;">{items_html}</ul>
                </div>
                ''', unsafe_allow_html=True)
    else:
        st.info("Добавьте разделы Patents/Speaking/Media в PDF/JSON для расширенных достижений.")
    st.markdown('</div>', unsafe_allow_html=True)

def render_analytics():
    st.markdown('<h1 class="hero-name">Performance Analytics</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-title">Data-Driven Success Metrics</p>', unsafe_allow_html=True)

    # Overall Statistics
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Lifetime Statistics</h2>', unsafe_allow_html=True)

    stats = PROFILE["analytics"].get("lifetime_stats", [])
    cols = st.columns(4)
    for i, (label, value, icon, growth) in enumerate(stats[:8]):
        with cols[i % 4]:
            st.markdown(f'''
            <div class="metric-card">
                <div style="font-size: 2rem;">{icon}</div>
                <div class="metric-number">{value}</div>
                <div class="metric-label">{label}</div>
                <p class="text-gradient" style="font-size: 0.9rem; margin-top: 10px;">{growth}</p>
            </div>
            ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Growth Charts
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Growth Trajectory</h2>', unsafe_allow_html=True)

    growth = PROFILE["analytics"].get("growth", {})
    years = growth.get("years", [2019, 2020, 2021, 2022, 2023, 2024])
    projects = growth.get("projects", [5, 12, 20, 28, 38, 45])
    publications = growth.get("publications", [2, 5, 10, 15, 22, 28])
    team_size = growth.get("team_size", [5, 15, 35, 60, 100, 150])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=projects, name='Projects', line=dict(color='#667eea', width=3), marker=dict(size=10)))
    fig.add_trace(go.Scatter(x=years, y=publications, name='Publications', line=dict(color='#764ba2', width=3), marker=dict(size=10)))
    fig.add_trace(go.Scatter(x=years, y=team_size, name='Team Size', line=dict(color='#f093fb', width=3), marker=dict(size=10), yaxis='y2'))
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), height=400,
        showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis=dict(title="Count", gridcolor='rgba(255,255,255,0.1)'),
        yaxis2=dict(title="Team Size", overlaying='y', side='right', gridcolor='rgba(255,255,255,0.1)'),
        xaxis=dict(title="Year", gridcolor='rgba(255,255,255,0.1)')
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Skills Distribution
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Skills Distribution</h2>', unsafe_allow_html=True)

    sd = PROFILE["analytics"].get("skills_distribution", {})
    if sd:
        skills_data = pd.DataFrame({"Skill": list(sd.keys()), "Level": list(sd.values())})
        fig2 = px.bar(skills_data, x='Level', y='Skill', orientation='h', color='Level', color_continuous_scale=['#667eea', '#764ba2'])
        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), height=300,
            showlegend=False, xaxis=dict(gridcolor='rgba(255,255,255,0.1)'), yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Секция навыков будет построена после импорта профиля.")
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================
# ROUTER
# =========================================
page = st.session_state.current_page
if page == "home":
    render_home()
elif page == "career":
    render_career()
elif page == "research":
    render_research()
elif page == "projects":
    render_projects()
elif page == "achievements":
    render_achievements()
elif page == "analytics":
    render_analytics()
else:
    render_home()

# =========================================
# FOOTER
# =========================================
st.markdown("""
<div style="margin-top: 60px; padding: 30px 0; text-align: center; border-top: 1px solid rgba(255,255,255,0.1);">
    <p class="text-muted">© {year} Alisher Beisembekov. Crafting the future, one innovation at a time.</p>
</div>
""".format(year=datetime.now().year), unsafe_allow_html=True)
