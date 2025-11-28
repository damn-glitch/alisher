import streamlit as st
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json
import os
import re

# Page Configuration
st.set_page_config(
    page_title="Alisher Beisembekov | Polymath & Tech Innovator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load profile data from JSON
@st.cache_data
def load_profile_data():
    profile_path = os.path.join(os.path.dirname(__file__), 'profile.json')
    with open(profile_path, 'r', encoding='utf-8') as f:
        return json.load(f)

profile_data = load_profile_data()

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# Helper function to clean HTML
def clean_html(text):
    if not text:
        return ""
    text = re.sub('<[^<]+?>', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# Achievement Categories - keywords for classification
CATEGORY_KEYWORDS = {
    "Sports": [
        "boxing", "biceps", "curl", "powerlifting", "martial", "muai thai", "hand-to-hand",
        "fighting", "sport", "IPC", "NPA", "IPAF", "asia cup", "champion", "titans"
    ],
    "Science": [
        "astronomy", "astrophysics", "IAAC", "physics", "chemistry", "biology", "math",
        "IYMC", "lomonosov", "electron", "experimental", "kolmogorov", "biotechnology"
    ],
    "Technology": [
        "google", "microsoft", "hackathon", "hackerrank", "hashcode", "codejam",
        "kickstart", "yandex", "data challenge", "AI", "zaintech", "programming", "code", "euler"
    ],
    "Entrepreneurship": [
        "ICE24", "united nations", "startup", "carso", "choice of country", "payit",
        "digital bridge", "business"
    ],
    "Academic": [
        "dean's list", "research scholar", "undergraduate", "RIT", "ambassador"
    ],
    "Chess": [
        "chess", "arena", "FIDE", "candidate master", "legends"
    ]
}

def categorize_award(title):
    title_lower = title.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in title_lower:
                return category
    return "Extra"

def get_categorized_awards():
    categories = {cat: [] for cat in list(CATEGORY_KEYWORDS.keys()) + ["Extra"]}
    for award in profile_data.get('honors_and_awards', []):
        category = categorize_award(award.get('title', ''))
        categories[category].append(award)
    return categories


# Advanced CSS with diverse section styles
def load_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700;800;900&family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

        * { font-family: 'Outfit', 'Inter', sans-serif; }

        .stApp {
            background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #1a1a2e 100%);
            background-attachment: fixed;
            background-size: 400% 400%;
            animation: gradientBG 15s ease infinite;
        }

        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        #MainMenu, footer, header { visibility: hidden; }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(10, 10, 15, 0.98) 0%, rgba(26, 26, 46, 0.98) 100%);
            backdrop-filter: blur(30px);
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }

        section[data-testid="stSidebar"] .stButton > button {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%);
            color: rgba(255, 255, 255, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 14px;
            padding: 16px 18px;
            width: 100%;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            font-weight: 500;
            margin-bottom: 6px;
            font-size: 0.9rem;
        }

        section[data-testid="stSidebar"] .stButton > button:hover {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
            border: 1px solid rgba(139, 92, 246, 0.5);
            transform: translateX(6px);
            box-shadow: 0 8px 32px rgba(139, 92, 246, 0.25);
        }

        /* Hero Styles */
        .hero-name {
            font-family: 'Space Grotesk', sans-serif;
            font-size: clamp(3rem, 9vw, 6rem);
            font-weight: 700;
            background: linear-gradient(135deg, #818cf8 0%, #a78bfa 25%, #c4b5fd 50%, #f0abfc 75%, #818cf8 100%);
            background-size: 300% 300%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            animation: shimmer 4s ease infinite;
            letter-spacing: -0.03em;
            line-height: 1.1;
            margin-bottom: 0;
        }

        @keyframes shimmer {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .hero-title {
            font-family: 'Space Grotesk', sans-serif;
            font-size: clamp(0.9rem, 2vw, 1.3rem);
            color: rgba(255, 255, 255, 0.6);
            text-align: center;
            margin-top: 12px;
            letter-spacing: 0.25em;
            text-transform: uppercase;
            font-weight: 300;
        }

        /* Section Styles - DIVERSE */
        .section-glass {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.04) 0%, rgba(255, 255, 255, 0.01) 100%);
            backdrop-filter: blur(20px);
            border-radius: 24px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            padding: 32px;
            margin: 20px 0;
            transition: all 0.4s ease;
        }

        .section-glass:hover {
            border-color: rgba(139, 92, 246, 0.3);
            box-shadow: 0 20px 60px rgba(139, 92, 246, 0.1);
        }

        .section-gradient-purple {
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(99, 102, 241, 0.08) 100%);
            border-radius: 24px;
            border: 1px solid rgba(139, 92, 246, 0.2);
            padding: 32px;
            margin: 20px 0;
        }

        .section-gradient-blue {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.12) 0%, rgba(6, 182, 212, 0.08) 100%);
            border-radius: 24px;
            border: 1px solid rgba(59, 130, 246, 0.2);
            padding: 32px;
            margin: 20px 0;
        }

        .section-gradient-green {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.12) 0%, rgba(52, 211, 153, 0.08) 100%);
            border-radius: 24px;
            border: 1px solid rgba(16, 185, 129, 0.2);
            padding: 32px;
            margin: 20px 0;
        }

        .section-gradient-orange {
            background: linear-gradient(135deg, rgba(249, 115, 22, 0.12) 0%, rgba(251, 146, 60, 0.08) 100%);
            border-radius: 24px;
            border: 1px solid rgba(249, 115, 22, 0.2);
            padding: 32px;
            margin: 20px 0;
        }

        .section-gradient-pink {
            background: linear-gradient(135deg, rgba(236, 72, 153, 0.12) 0%, rgba(244, 114, 182, 0.08) 100%);
            border-radius: 24px;
            border: 1px solid rgba(236, 72, 153, 0.2);
            padding: 32px;
            margin: 20px 0;
        }

        .section-dark {
            background: rgba(0, 0, 0, 0.4);
            border-radius: 24px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            padding: 32px;
            margin: 20px 0;
        }

        .section-bordered {
            background: transparent;
            border-radius: 24px;
            border: 2px solid rgba(139, 92, 246, 0.3);
            padding: 32px;
            margin: 20px 0;
            position: relative;
        }

        .section-bordered::before {
            content: '';
            position: absolute;
            top: -2px; left: -2px; right: -2px; bottom: -2px;
            background: linear-gradient(135deg, #818cf8, #a78bfa, #c4b5fd, #818cf8);
            border-radius: 26px;
            z-index: -1;
            opacity: 0.3;
            background-size: 300% 300%;
            animation: shimmer 4s ease infinite;
        }

        /* Section Headers - DIVERSE */
        .section-header {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.8rem;
            font-weight: 600;
            background: linear-gradient(135deg, #fff 0%, rgba(255, 255, 255, 0.8) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0 0 24px 0;
            padding-bottom: 12px;
            border-bottom: 2px solid rgba(139, 92, 246, 0.3);
        }

        .section-header-icon {
            font-size: 2rem;
            margin-right: 12px;
            vertical-align: middle;
        }

        .section-header-purple { border-color: rgba(139, 92, 246, 0.5); }
        .section-header-blue { border-color: rgba(59, 130, 246, 0.5); }
        .section-header-green { border-color: rgba(16, 185, 129, 0.5); }
        .section-header-orange { border-color: rgba(249, 115, 22, 0.5); }
        .section-header-pink { border-color: rgba(236, 72, 153, 0.5); }

        /* Cards - DIVERSE */
        .card-default {
            background: rgba(255, 255, 255, 0.03);
            border-radius: 16px;
            padding: 20px;
            margin: 12px 0;
            border: 1px solid rgba(255, 255, 255, 0.06);
            transition: all 0.3s ease;
        }

        .card-default:hover {
            transform: translateX(6px);
            border-color: rgba(139, 92, 246, 0.3);
            background: rgba(139, 92, 246, 0.05);
        }

        .card-elevated {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.06) 0%, rgba(255, 255, 255, 0.02) 100%);
            border-radius: 20px;
            padding: 24px;
            margin: 16px 0;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .card-elevated:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 60px rgba(139, 92, 246, 0.2);
        }

        .card-compact {
            background: rgba(255, 255, 255, 0.02);
            border-radius: 12px;
            padding: 14px 18px;
            margin: 8px 0;
            border-left: 3px solid rgba(139, 92, 246, 0.5);
            transition: all 0.3s ease;
        }

        .card-compact:hover {
            background: rgba(139, 92, 246, 0.08);
            border-left-color: #a78bfa;
        }

        .card-highlight {
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(99, 102, 241, 0.1) 100%);
            border-radius: 20px;
            padding: 28px;
            margin: 16px 0;
            border: 1px solid rgba(139, 92, 246, 0.3);
            position: relative;
            overflow: hidden;
        }

        .card-highlight::after {
            content: '';
            position: absolute;
            top: 0; right: 0;
            width: 100px; height: 100px;
            background: radial-gradient(circle, rgba(139, 92, 246, 0.3) 0%, transparent 70%);
        }

        /* Metric Cards */
        .metric-card {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.06) 0%, rgba(255, 255, 255, 0.02) 100%);
            border-radius: 20px;
            padding: 24px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.08);
            transition: all 0.4s ease;
        }

        .metric-card:hover {
            transform: translateY(-6px) scale(1.02);
            border-color: rgba(139, 92, 246, 0.4);
            box-shadow: 0 15px 40px rgba(139, 92, 246, 0.2);
        }

        .metric-number {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #818cf8 0%, #c4b5fd 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .metric-label {
            color: rgba(255, 255, 255, 0.6);
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            margin-top: 6px;
        }

        /* Tags and Badges */
        .tag {
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(99, 102, 241, 0.15) 100%);
            border: 1px solid rgba(139, 92, 246, 0.25);
            color: rgba(255, 255, 255, 0.9);
            padding: 8px 16px;
            border-radius: 25px;
            font-size: 0.85rem;
            font-weight: 500;
            display: inline-block;
            margin: 4px;
            transition: all 0.3s ease;
        }

        .tag:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(139, 92, 246, 0.3);
        }

        .badge-success {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(52, 211, 153, 0.2) 100%);
            color: #6ee7b7;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }

        .badge-info {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(96, 165, 250, 0.2) 100%);
            color: #93c5fd;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }

        .badge-warning {
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.2) 0%, rgba(251, 191, 36, 0.2) 100%);
            color: #fcd34d;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }

        /* Timeline */
        .timeline-container { position: relative; padding-left: 30px; }

        .timeline-line {
            position: absolute;
            left: 8px;
            top: 0;
            bottom: 0;
            width: 2px;
            background: linear-gradient(180deg, #818cf8 0%, #a78bfa 50%, transparent 100%);
        }

        .timeline-item {
            position: relative;
            margin-bottom: 24px;
            padding-left: 20px;
        }

        .timeline-dot {
            position: absolute;
            left: -22px;
            top: 6px;
            width: 14px;
            height: 14px;
            background: linear-gradient(135deg, #818cf8 0%, #a78bfa 100%);
            border-radius: 50%;
            box-shadow: 0 0 20px rgba(139, 92, 246, 0.5);
        }

        /* Grid layouts */
        .grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }
        .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
        .grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }

        @media (max-width: 768px) {
            .grid-2, .grid-3, .grid-4 { grid-template-columns: 1fr; }
        }

        /* Text utilities */
        .text-gradient {
            background: linear-gradient(135deg, #818cf8 0%, #c4b5fd 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .text-white { color: rgba(255, 255, 255, 0.9); }
        .text-muted { color: rgba(255, 255, 255, 0.5); }
        .text-sm { font-size: 0.85rem; }
        .text-xs { font-size: 0.75rem; }
        .font-mono { font-family: 'JetBrains Mono', monospace; }

        /* Animations */
        .floating { animation: float 6s ease-in-out infinite; }
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-12px); }
        }

        .pulse { animation: pulse 2s ease-in-out infinite; }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.6; }
        }

        /* Scrollbar */
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: rgba(255, 255, 255, 0.02); }
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #818cf8 0%, #a78bfa 100%);
            border-radius: 4px;
        }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] { gap: 8px; background: transparent; }
        .stTabs [data-baseweb="tab"] {
            background: rgba(255, 255, 255, 0.03);
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: rgba(255, 255, 255, 0.7);
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(99, 102, 241, 0.2) 100%);
            border-color: rgba(139, 92, 246, 0.4);
            color: white;
        }

        /* Sidebar styles */
        .sidebar-header {
            text-align: center;
            padding: 20px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            margin-bottom: 20px;
        }
        .sidebar-name {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.3rem;
            font-weight: 600;
            background: linear-gradient(135deg, #818cf8 0%, #c4b5fd 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .sidebar-location {
            color: rgba(255, 255, 255, 0.5);
            font-size: 0.8rem;
            margin-top: 4px;
        }

        /* Patent card special */
        .patent-card {
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(251, 191, 36, 0.05) 100%);
            border: 1px solid rgba(245, 158, 11, 0.2);
            border-radius: 16px;
            padding: 20px;
            margin: 12px 0;
            transition: all 0.3s ease;
        }
        .patent-card:hover {
            transform: translateX(6px);
            border-color: rgba(245, 158, 11, 0.5);
        }
        .patent-id {
            font-family: 'JetBrains Mono', monospace;
            color: #fcd34d;
            font-size: 0.85rem;
        }
    </style>
    """, unsafe_allow_html=True)


load_css()

# Sidebar
with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-header">
        <div class="sidebar-name">{profile_data.get('name', 'Alisher Beisembekov')}</div>
        <div class="sidebar-location">📍 {profile_data.get('location', 'Astana, Kazakhstan')}</div>
    </div>
    """, unsafe_allow_html=True)

    pages = [
        ("🏠", "Home", "home"),
        ("💼", "Career", "career"),
        ("🔬", "Research", "research"),
        ("💻", "Projects", "projects"),
        ("🏆", "Achievements", "achievements"),
        ("📜", "Patents", "patents"),
        ("📊", "Analytics", "analytics"),
    ]

    for icon, label, page in pages:
        if st.button(f"{icon} {label}", use_container_width=True):
            st.session_state.current_page = page

    st.markdown("---")

    # Quick stats in sidebar
    st.markdown(f"""
    <div style="padding: 15px; background: rgba(255,255,255,0.03); border-radius: 12px; margin-bottom: 15px;">
        <div style="color: rgba(255,255,255,0.5); font-size: 0.75rem; margin-bottom: 8px;">QUICK STATS</div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
            <div style="text-align: center;">
                <div class="text-gradient" style="font-size: 1.3rem; font-weight: 700;">{len(profile_data.get('honors_and_awards', []))}</div>
                <div class="text-muted text-xs">Awards</div>
            </div>
            <div style="text-align: center;">
                <div class="text-gradient" style="font-size: 1.3rem; font-weight: 700;">{len(profile_data.get('patents', []))}</div>
                <div class="text-muted text-xs">Patents</div>
            </div>
            <div style="text-align: center;">
                <div class="text-gradient" style="font-size: 1.3rem; font-weight: 700;">{len([p for p in profile_data.get('projects', []) if p.get('name')])}</div>
                <div class="text-muted text-xs">Projects</div>
            </div>
            <div style="text-align: center;">
                <div class="text-gradient" style="font-size: 1.3rem; font-weight: 700;">{len(profile_data.get('certifications', []))}</div>
                <div class="text-muted text-xs">Certs</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Social links
    st.markdown(f"""
    <div style="text-align: center; padding: 15px 0;">
        <div style="display: flex; justify-content: center; gap: 16px;">
            <a href="{profile_data.get('url', '#')}" target="_blank" style="font-size: 1.3rem; text-decoration: none;">💼</a>
            <a href="https://github.com/damn-glitch" target="_blank" style="font-size: 1.3rem; text-decoration: none;">💻</a>
            <a href="https://www.credly.com/users/alisher-beisembekov/badges" target="_blank" style="font-size: 1.3rem; text-decoration: none;">🏅</a>
        </div>
        <div class="text-muted text-xs" style="margin-top: 10px;">
            {profile_data.get('followers', '')} · {profile_data.get('connections', '')}
        </div>
    </div>
    """, unsafe_allow_html=True)


# ==================== HOME PAGE ====================
if st.session_state.current_page == 'home':
    # Hero
    st.markdown(f'<h1 class="hero-name floating">{profile_data.get("name", "Alisher Beisembekov")}</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-title">Polymath · Tech Innovator · World Record Holder</p>', unsafe_allow_html=True)

    # Stats Row
    st.markdown("---")
    cols = st.columns(5)
    stats = [
        ("🏆", len(profile_data.get('honors_and_awards', [])), "Awards"),
        ("📜", len(profile_data.get('patents', [])), "Patents"),
        ("💻", len([p for p in profile_data.get('projects', []) if p.get('name')]), "Projects"),
        ("📚", len(profile_data.get('publications', [])), "Publications"),
        ("🎓", len(profile_data.get('certifications', [])), "Certifications"),
    ]
    for col, (icon, val, label) in zip(cols, stats):
        with col:
            st.markdown(f'''
            <div class="metric-card">
                <div style="font-size: 2rem; margin-bottom: 8px;">{icon}</div>
                <div class="metric-number">{val}</div>
                <div class="metric-label">{label}</div>
            </div>
            ''', unsafe_allow_html=True)

    # About Section
    st.markdown('<div class="section-gradient-purple">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header section-header-purple"><span class="section-header-icon">👤</span>About</h2>', unsafe_allow_html=True)

    description = profile_data.get('description', '')
    st.markdown(f'''
    <p class="text-white" style="font-size: 1.05rem; line-height: 1.8;">{description}</p>
    ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Two columns: Current Roles + Education/Languages
    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown('<div class="section-glass">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-header"><span class="section-header-icon">🚀</span>Current Roles</h2>', unsafe_allow_html=True)

        current_positions = [e for e in profile_data.get('experience', [])
                           if e.get('date', {}).get('end_date') == 'Present' and e.get('title')]

        for pos in current_positions[:5]:
            title = pos.get('title', '')
            company = pos.get('company_name', '')
            start = pos.get('date', {}).get('start_date', '')
            desc = clean_html(pos.get('description', ''))[:180]

            st.markdown(f'''
            <div class="card-elevated">
                <h4 class="text-white" style="margin: 0 0 6px 0;">{title}</h4>
                <p class="text-gradient" style="font-weight: 600; margin: 0 0 4px 0;">{company}</p>
                <span class="badge-success">{start} - Present</span>
                <p class="text-muted text-sm" style="margin-top: 12px;">{desc}...</p>
            </div>
            ''', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Education
        st.markdown('<div class="section-gradient-blue">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-header section-header-blue"><span class="section-header-icon">🎓</span>Education</h2>', unsafe_allow_html=True)

        for edu in profile_data.get('education', []):
            st.markdown(f'''
            <div class="card-compact">
                <div class="text-white" style="font-weight: 600;">{edu.get('degree', '')}</div>
                <div class="text-gradient text-sm">{edu.get('major', '')}</div>
                <div class="text-muted text-xs">{edu.get('university_name', '')}</div>
                <div class="text-muted text-xs">{edu.get('date', {}).get('start_date', '')} - {edu.get('date', {}).get('end_date', '')}</div>
            </div>
            ''', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Languages
        st.markdown('<div class="section-gradient-green">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-header section-header-green"><span class="section-header-icon">🌍</span>Languages</h2>', unsafe_allow_html=True)

        langs_html = ""
        for lang in profile_data.get('languages', []):
            prof = lang.get('description', '').split()[0] if lang.get('description') else ''
            langs_html += f'<span class="tag">{lang.get("name", "")} <span class="text-muted text-xs">({prof})</span></span>'

        st.markdown(f'<div>{langs_html}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Recent Activities
    activities = profile_data.get('activities', [])
    if activities:
        st.markdown('<div class="section-dark">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-header"><span class="section-header-icon">📰</span>Recent Activities</h2>', unsafe_allow_html=True)

        cols = st.columns(4)
        for i, activity in enumerate(activities[:8]):
            with cols[i % 4]:
                title = activity.get('title', '')[:60]
                subtitle = activity.get('subtitle', '')[:40]
                st.markdown(f'''
                <div class="card-compact" style="min-height: 80px;">
                    <div class="text-white text-sm" style="font-weight: 500;">{title}</div>
                    <div class="text-muted text-xs">{subtitle}</div>
                </div>
                ''', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


# ==================== CAREER PAGE ====================
elif st.session_state.current_page == 'career':
    st.markdown('<h1 class="hero-name">Career Journey</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-title">Professional Evolution & Leadership</p>', unsafe_allow_html=True)

    # Career Stats
    experiences = [e for e in profile_data.get('experience', []) if e.get('title') and e.get('title') != e.get('company_name')]
    current_roles = len([e for e in experiences if e.get('date', {}).get('end_date') == 'Present'])

    cols = st.columns(4)
    career_stats = [
        ("💼", len(experiences), "Total Positions"),
        ("🚀", current_roles, "Current Roles"),
        ("🏢", len(set(e.get('company_name', '') for e in experiences)), "Companies"),
        ("📅", "6+", "Years Experience"),
    ]
    for col, (icon, val, label) in zip(cols, career_stats):
        with col:
            st.markdown(f'''
            <div class="metric-card">
                <div style="font-size: 1.8rem;">{icon}</div>
                <div class="metric-number">{val}</div>
                <div class="metric-label">{label}</div>
            </div>
            ''', unsafe_allow_html=True)

    # Timeline section
    st.markdown('<div class="section-glass">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header"><span class="section-header-icon">📈</span>Professional Timeline</h2>', unsafe_allow_html=True)

    st.markdown('<div class="timeline-container"><div class="timeline-line"></div>', unsafe_allow_html=True)

    for exp in experiences:
        title = exp.get('title', '')
        company = exp.get('company_name', '')
        start = exp.get('date', {}).get('start_date', '')
        end = exp.get('date', {}).get('end_date', 'Present')
        location = exp.get('location', '')
        desc = clean_html(exp.get('description', ''))[:350]

        is_current = end == 'Present'
        badge = '<span class="badge-success">Current</span>' if is_current else f'<span class="badge-info">{end}</span>'

        st.markdown(f'''
        <div class="timeline-item">
            <div class="timeline-dot"></div>
            <div class="card-elevated">
                <div style="display: flex; justify-content: space-between; align-items: start; flex-wrap: wrap; gap: 10px;">
                    <div>
                        <h3 class="text-white" style="margin: 0 0 4px 0; font-size: 1.1rem;">{title}</h3>
                        <p class="text-gradient" style="font-weight: 600; margin: 0;">{company}</p>
                    </div>
                    <div style="text-align: right;">
                        {badge}
                        <div class="text-muted text-xs" style="margin-top: 4px;">{start} - {end}</div>
                        {f'<div class="text-muted text-xs">📍 {location}</div>' if location else ''}
                    </div>
                </div>
                {f'<p class="text-white text-sm" style="margin-top: 14px; line-height: 1.6; opacity: 0.85;">{desc}...</p>' if desc else ''}
            </div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown('</div></div>', unsafe_allow_html=True)


# ==================== RESEARCH PAGE ====================
elif st.session_state.current_page == 'research':
    st.markdown('<h1 class="hero-name">Research & Knowledge</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-title">Publications · Certifications · Expertise</p>', unsafe_allow_html=True)

    # Publications Section
    st.markdown('<div class="section-gradient-purple">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header section-header-purple"><span class="section-header-icon">📚</span>Publications</h2>', unsafe_allow_html=True)

    for pub in profile_data.get('publications', []):
        st.markdown(f'''
        <div class="card-highlight">
            <h3 class="text-white" style="margin: 0 0 10px 0; font-size: 1.1rem;">{pub.get('title', '')}</h3>
            <div style="margin-bottom: 12px;">
                <span class="badge-warning">{pub.get('publisher', '')}</span>
                {f'<span class="text-muted" style="margin-left: 10px;">{pub.get("publication_date", "")}</span>' if pub.get('publication_date') else ''}
            </div>
            <p class="text-white text-sm" style="line-height: 1.7; opacity: 0.85;">{pub.get('description', '')}</p>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Certifications Section
    st.markdown('<div class="section-gradient-blue">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header section-header-blue"><span class="section-header-icon">🎖️</span>Certifications</h2>', unsafe_allow_html=True)

    cols = st.columns(2)
    for i, cert in enumerate(profile_data.get('certifications', [])):
        with cols[i % 2]:
            issued = cert.get('issued_date', '').split(' Credential')[0] if cert.get('issued_date') else ''
            st.markdown(f'''
            <div class="card-default">
                <h4 class="text-white" style="margin: 0 0 6px 0; font-size: 0.95rem;">{cert.get('title', '')}</h4>
                <div class="text-gradient text-sm" style="font-weight: 500;">{cert.get('issuer', '')}</div>
                <div class="text-muted text-xs">{issued}</div>
                {f'<div class="font-mono text-xs text-muted" style="margin-top: 6px;">ID: {cert.get("credential", "")}</div>' if cert.get('credential') else ''}
            </div>
            ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Skills from certifications
    st.markdown('<div class="section-dark">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header"><span class="section-header-icon">🛠️</span>Expertise Areas</h2>', unsafe_allow_html=True)

    issuers = {}
    for cert in profile_data.get('certifications', []):
        issuer = cert.get('issuer', '').split('(')[0].strip()
        if issuer:
            issuers[issuer] = issuers.get(issuer, 0) + 1

    tags_html = ""
    for issuer, count in sorted(issuers.items(), key=lambda x: x[1], reverse=True):
        tags_html += f'<span class="tag">{issuer} <span class="text-muted">({count})</span></span>'

    st.markdown(f'<div>{tags_html}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ==================== PROJECTS PAGE ====================
elif st.session_state.current_page == 'projects':
    st.markdown('<h1 class="hero-name">Innovation Portfolio</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-title">Building Tomorrow\'s Technology</p>', unsafe_allow_html=True)

    projects = [p for p in profile_data.get('projects', []) if p.get('name')]
    projects_with_desc = [p for p in projects if p.get('description')]

    # Stats
    cols = st.columns(3)
    proj_stats = [
        ("💡", len(projects), "Total Projects"),
        ("📝", len(projects_with_desc), "Documented"),
        ("🚀", len([p for p in projects if p.get('date', {}).get('end_date') in [None, 'Present', ''] if p.get('date')]), "Active"),
    ]
    for col, (icon, val, label) in zip(cols, proj_stats):
        with col:
            st.markdown(f'''
            <div class="metric-card">
                <div style="font-size: 1.8rem;">{icon}</div>
                <div class="metric-number">{val}</div>
                <div class="metric-label">{label}</div>
            </div>
            ''', unsafe_allow_html=True)

    # Featured Projects (with descriptions)
    st.markdown('<div class="section-gradient-green">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header section-header-green"><span class="section-header-icon">⭐</span>Featured Projects</h2>', unsafe_allow_html=True)

    for project in projects_with_desc[:12]:
        name = project.get('name', '')
        desc = clean_html(project.get('description', ''))
        desc = re.sub(r'[✅🚀🔧📊⚡🧠📈💡🔗]', '', desc)[:400]

        date_info = project.get('date', {})
        start = date_info.get('start_date', '') if date_info else ''
        end = date_info.get('end_date', '') if date_info else ''
        period = f"{start} - {end if end else 'Present'}" if start else ""

        st.markdown(f'''
        <div class="card-elevated">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;">
                <h3 class="text-white" style="margin: 0; font-size: 1.05rem; flex: 1;">{name}</h3>
                {f'<span class="badge-success">{period}</span>' if period else ''}
            </div>
            <p class="text-white text-sm" style="line-height: 1.7; opacity: 0.85;">{desc}...</p>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Other Projects Grid
    other_projects = [p for p in projects if not p.get('description') and p.get('name')]
    if other_projects:
        st.markdown('<div class="section-dark">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-header"><span class="section-header-icon">📂</span>Other Projects</h2>', unsafe_allow_html=True)

        cols = st.columns(3)
        for i, proj in enumerate(other_projects):
            with cols[i % 3]:
                date_info = proj.get('date', {})
                period = f"{date_info.get('start_date', '')}" if date_info and date_info.get('start_date') else ""
                st.markdown(f'''
                <div class="card-compact">
                    <div class="text-white text-sm" style="font-weight: 500;">{proj.get('name', '')}</div>
                    <div class="text-muted text-xs">{period}</div>
                </div>
                ''', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


# ==================== ACHIEVEMENTS PAGE ====================
elif st.session_state.current_page == 'achievements':
    st.markdown('<h1 class="hero-name">Achievements</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-title">Excellence Across Multiple Disciplines</p>', unsafe_allow_html=True)

    categorized = get_categorized_awards()

    category_config = {
        "Sports": {"icon": "🏋️", "section": "section-gradient-orange", "header": "section-header-orange"},
        "Science": {"icon": "🔬", "section": "section-gradient-purple", "header": "section-header-purple"},
        "Technology": {"icon": "💻", "section": "section-gradient-blue", "header": "section-header-blue"},
        "Entrepreneurship": {"icon": "🚀", "section": "section-gradient-green", "header": "section-header-green"},
        "Academic": {"icon": "🎓", "section": "section-gradient-pink", "header": "section-header-pink"},
        "Chess": {"icon": "♟️", "section": "section-dark", "header": ""},
        "Extra": {"icon": "✨", "section": "section-glass", "header": ""},
    }

    # Overview
    st.markdown('<div class="section-bordered">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header"><span class="section-header-icon">📊</span>Achievement Overview</h2>', unsafe_allow_html=True)

    active_cats = [(cat, awards) for cat, awards in categorized.items() if awards]
    cols = st.columns(len(active_cats))

    for col, (cat, awards) in zip(cols, active_cats):
        config = category_config.get(cat, {"icon": "🏆"})
        with col:
            st.markdown(f'''
            <div class="metric-card">
                <div style="font-size: 2rem;">{config["icon"]}</div>
                <div class="metric-number">{len(awards)}</div>
                <div class="metric-label">{cat}</div>
            </div>
            ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Each category in its own styled section
    for category, awards in categorized.items():
        if not awards:
            continue

        config = category_config.get(category, {"icon": "🏆", "section": "section-glass", "header": ""})

        st.markdown(f'<div class="{config["section"]}">', unsafe_allow_html=True)
        st.markdown(f'<h2 class="section-header {config["header"]}"><span class="section-header-icon">{config["icon"]}</span>{category} ({len(awards)} awards)</h2>', unsafe_allow_html=True)

        cols = st.columns(2)
        for i, award in enumerate(awards):
            with cols[i % 2]:
                title = award.get('title', '')
                issuer = award.get('issuer', '')
                date = award.get('issued_date', '')
                desc = award.get('description', '')

                st.markdown(f'''
                <div class="card-default">
                    <div class="text-white" style="font-weight: 500; margin-bottom: 4px;">{title}</div>
                    <div class="text-muted text-xs">{issuer} {f"· {date}" if date else ""}</div>
                    {f'<p class="text-muted text-xs" style="margin-top: 8px;">{desc[:120]}...</p>' if desc and len(desc) > 10 else ''}
                </div>
                ''', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


# ==================== PATENTS PAGE ====================
elif st.session_state.current_page == 'patents':
    st.markdown('<h1 class="hero-name">Patent Portfolio</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-title">Intellectual Property & Innovations</p>', unsafe_allow_html=True)

    patents = profile_data.get('patents', [])

    # Stats
    cols = st.columns(3)
    patent_stats = [
        ("📜", len(patents), "Total Patents"),
        ("🇰🇿", len([p for p in patents if 'KZ' in p.get('patent_id', '')]), "Kazakhstan"),
        ("💡", len(patents), "Innovations"),
    ]
    for col, (icon, val, label) in zip(cols, patent_stats):
        with col:
            st.markdown(f'''
            <div class="metric-card">
                <div style="font-size: 1.8rem;">{icon}</div>
                <div class="metric-number">{val}</div>
                <div class="metric-label">{label}</div>
            </div>
            ''', unsafe_allow_html=True)

    st.markdown('<div class="section-gradient-orange">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header section-header-orange"><span class="section-header-icon">📜</span>Registered Patents</h2>', unsafe_allow_html=True)

    cols = st.columns(2)
    for i, patent in enumerate(patents):
        with cols[i % 2]:
            st.markdown(f'''
            <div class="patent-card">
                <h4 class="text-white" style="margin: 0 0 10px 0;">{patent.get('title', '')}</h4>
                <div class="patent-id">{patent.get('patent_id', '')}</div>
            </div>
            ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ==================== ANALYTICS PAGE ====================
elif st.session_state.current_page == 'analytics':
    st.markdown('<h1 class="hero-name">Analytics Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-title">Data-Driven Insights</p>', unsafe_allow_html=True)

    categorized = get_categorized_awards()

    # Summary Stats
    st.markdown('<div class="section-glass">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header"><span class="section-header-icon">📈</span>Summary Statistics</h2>', unsafe_allow_html=True)

    cols = st.columns(5)
    summary = [
        ("🏆", len(profile_data.get('honors_and_awards', [])), "Awards"),
        ("📜", len(profile_data.get('patents', [])), "Patents"),
        ("💻", len([p for p in profile_data.get('projects', []) if p.get('name')]), "Projects"),
        ("🎓", len(profile_data.get('certifications', [])), "Certifications"),
        ("💼", len([e for e in profile_data.get('experience', []) if e.get('title')]), "Positions"),
    ]
    for col, (icon, val, label) in zip(cols, summary):
        with col:
            st.markdown(f'''
            <div class="metric-card">
                <div style="font-size: 1.6rem;">{icon}</div>
                <div class="metric-number">{val}</div>
                <div class="metric-label">{label}</div>
            </div>
            ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Charts Row
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-gradient-purple">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-header section-header-purple"><span class="section-header-icon">🎯</span>Achievement Distribution</h2>', unsafe_allow_html=True)

        cat_counts = {cat: len(awards) for cat, awards in categorized.items() if awards}

        fig = go.Figure(data=[go.Pie(
            labels=list(cat_counts.keys()),
            values=list(cat_counts.values()),
            hole=0.5,
            marker=dict(colors=['#f97316', '#8b5cf6', '#3b82f6', '#10b981', '#ec4899', '#6366f1', '#64748b']),
            textfont=dict(color='white'),
        )])
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=350,
            margin=dict(t=20, b=20, l=20, r=20),
            showlegend=True,
            legend=dict(orientation="h", y=-0.1, x=0.5, xanchor="center")
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-gradient-blue">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-header section-header-blue"><span class="section-header-icon">📅</span>Awards Timeline</h2>', unsafe_allow_html=True)

        year_counts = {}
        for award in profile_data.get('honors_and_awards', []):
            date_str = award.get('issued_date', '')
            match = re.search(r'20\d{2}', date_str)
            if match:
                year = int(match.group())
                year_counts[year] = year_counts.get(year, 0) + 1

        if year_counts:
            years = sorted(year_counts.keys())
            counts = [year_counts[y] for y in years]

            fig2 = go.Figure()
            fig2.add_trace(go.Bar(
                x=years, y=counts,
                marker=dict(color=counts, colorscale=[[0, '#3b82f6'], [1, '#93c5fd']])
            ))
            fig2.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                height=350,
                margin=dict(t=20, b=40, l=40, r=20),
                xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.05)', title="Count")
            )
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # Certification Sources
    st.markdown('<div class="section-dark">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header"><span class="section-header-icon">🎖️</span>Certification Sources</h2>', unsafe_allow_html=True)

    issuers = {}
    for cert in profile_data.get('certifications', []):
        issuer = cert.get('issuer', '').split('(')[0].strip()
        if issuer:
            issuers[issuer] = issuers.get(issuer, 0) + 1

    if issuers:
        sorted_issuers = sorted(issuers.items(), key=lambda x: x[1], reverse=True)[:8]

        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            y=[i[0] for i in sorted_issuers],
            x=[i[1] for i in sorted_issuers],
            orientation='h',
            marker=dict(color=[i[1] for i in sorted_issuers], colorscale=[[0, '#818cf8'], [1, '#c4b5fd']])
        ))
        fig3.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=300,
            margin=dict(t=20, b=40, l=120, r=20),
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)', title="Certifications"),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)')
        )
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)


# Footer
st.markdown(f"""
<div style="margin-top: 60px; padding: 30px 0; text-align: center; border-top: 1px solid rgba(255,255,255,0.08);">
    <p class="text-muted" style="margin-bottom: 15px;">
        © 2025 {profile_data.get('name', 'Alisher Beisembekov')} · Built with data from LinkedIn
    </p>
    <div style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap;">
        <a href="{profile_data.get('url', '#')}" target="_blank" class="text-muted" style="text-decoration: none;">LinkedIn</a>
        <a href="https://github.com/damn-glitch" target="_blank" class="text-muted" style="text-decoration: none;">GitHub</a>
        <a href="https://www.credly.com/users/alisher-beisembekov/badges" target="_blank" class="text-muted" style="text-decoration: none;">Credly</a>
    </div>
    <p class="text-muted text-xs" style="margin-top: 15px; opacity: 0.5;">
        Last updated: {profile_data.get('crawled_at', '')}
    </p>
</div>
""", unsafe_allow_html=True)
