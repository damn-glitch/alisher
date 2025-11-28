import streamlit as st
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json
import os

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
        "kickstart", "yandex", "data challenge", "AI", "zaintech", "programming", "code"
    ],
    "Entrepreneurship": [
        "ICE24", "united nations", "startup", "carso", "choice of country", "payit",
        "digital bridge", "business"
    ],
    "Academic": [
        "dean's list", "research scholar", "undergraduate", "RIT", "ambassador"
    ],
    "Chess": [
        "chess", "arena", "FIDE", "master", "candidate", "legends"
    ]
}

def categorize_award(title):
    """Categorize an award based on keywords in its title."""
    title_lower = title.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in title_lower:
                return category
    return "Extra"

def get_categorized_awards():
    """Get all awards categorized by area."""
    categories = {
        "Sports": [],
        "Science": [],
        "Technology": [],
        "Entrepreneurship": [],
        "Academic": [],
        "Chess": [],
        "Extra": []
    }

    for award in profile_data.get('honors_and_awards', []):
        category = categorize_award(award.get('title', ''))
        categories[category].append(award)

    return categories


# Advanced Post-Modern CSS Design
def load_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700;800;900&family=Outfit:wght@300;400;500;600;700;800&display=swap');

        /* Global Styles */
        * {
            font-family: 'Outfit', 'Inter', sans-serif;
        }

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

        /* Hide Streamlit Branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(10, 10, 15, 0.95) 0%, rgba(26, 26, 46, 0.95) 100%);
            backdrop-filter: blur(30px);
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }

        section[data-testid="stSidebar"] .stButton > button {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%);
            color: rgba(255, 255, 255, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 18px 20px;
            width: 100%;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            font-weight: 500;
            margin-bottom: 8px;
            font-size: 0.95rem;
            letter-spacing: 0.02em;
        }

        section[data-testid="stSidebar"] .stButton > button:hover {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%);
            border: 1px solid rgba(139, 92, 246, 0.4);
            transform: translateX(8px);
            box-shadow: 0 8px 32px rgba(139, 92, 246, 0.2), inset 0 0 20px rgba(139, 92, 246, 0.05);
        }

        /* Glassmorphism Cards */
        .glass-card {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-radius: 24px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            padding: 32px;
            margin: 24px 0;
            box-shadow: 0 8px 40px rgba(0, 0, 0, 0.3), inset 0 0 60px rgba(255, 255, 255, 0.02);
            transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }

        .glass-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.03), transparent);
            transition: left 0.7s ease;
        }

        .glass-card:hover::before {
            left: 100%;
        }

        .glass-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 60px rgba(139, 92, 246, 0.15), inset 0 0 60px rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(139, 92, 246, 0.3);
        }

        /* Hero Section */
        .hero-name {
            font-family: 'Space Grotesk', sans-serif;
            font-size: clamp(3.5rem, 10vw, 7rem);
            font-weight: 700;
            background: linear-gradient(135deg, #818cf8 0%, #a78bfa 25%, #c4b5fd 50%, #f0abfc 75%, #818cf8 100%);
            background-size: 300% 300%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-align: center;
            animation: shimmer 4s ease infinite;
            letter-spacing: -0.03em;
            line-height: 1.1;
            margin-bottom: 0;
            text-shadow: 0 0 80px rgba(139, 92, 246, 0.5);
        }

        @keyframes shimmer {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .hero-title {
            font-family: 'Space Grotesk', sans-serif;
            font-size: clamp(1rem, 2.5vw, 1.5rem);
            color: rgba(255, 255, 255, 0.7);
            text-align: center;
            margin-top: 16px;
            letter-spacing: 0.3em;
            text-transform: uppercase;
            font-weight: 300;
        }

        /* Metric Cards */
        .metric-card {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            padding: 28px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.08);
            transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }

        .metric-card::after {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(139, 92, 246, 0.1) 0%, transparent 70%);
            opacity: 0;
            transition: opacity 0.5s ease;
        }

        .metric-card:hover::after {
            opacity: 1;
        }

        .metric-card:hover {
            transform: translateY(-8px) scale(1.02);
            border: 1px solid rgba(139, 92, 246, 0.4);
            box-shadow: 0 20px 50px rgba(139, 92, 246, 0.2);
        }

        .metric-number {
            font-size: 2.8rem;
            font-weight: 700;
            background: linear-gradient(135deg, #818cf8 0%, #c4b5fd 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
            position: relative;
            z-index: 1;
        }

        .metric-label {
            color: rgba(255, 255, 255, 0.6);
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.15em;
            font-weight: 500;
            position: relative;
            z-index: 1;
        }

        /* Section Headers */
        .section-header {
            font-family: 'Space Grotesk', sans-serif;
            font-size: clamp(2rem, 4vw, 3rem);
            font-weight: 600;
            background: linear-gradient(135deg, #fff 0%, rgba(255, 255, 255, 0.8) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 48px 0 32px 0;
            position: relative;
            padding-bottom: 16px;
        }

        .section-header:after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 80px;
            height: 4px;
            background: linear-gradient(90deg, #818cf8 0%, #c4b5fd 50%, transparent 100%);
            border-radius: 2px;
        }

        /* Achievement Cards */
        .achievement-card {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.02) 0%, rgba(255, 255, 255, 0.01) 100%);
            backdrop-filter: blur(15px);
            border-radius: 20px;
            padding: 24px;
            margin-bottom: 16px;
            border: 1px solid rgba(255, 255, 255, 0.06);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }

        .achievement-card:hover {
            transform: translateX(8px);
            border: 1px solid rgba(139, 92, 246, 0.3);
            box-shadow: 0 10px 40px rgba(139, 92, 246, 0.15);
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%);
        }

        /* Category Cards */
        .category-card {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%);
            backdrop-filter: blur(15px);
            border-radius: 24px;
            padding: 28px;
            margin-bottom: 20px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .category-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 50px rgba(139, 92, 246, 0.2);
        }

        .category-header {
            display: flex;
            align-items: center;
            gap: 16px;
            margin-bottom: 20px;
            padding-bottom: 16px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        .category-icon {
            font-size: 2.5rem;
            filter: drop-shadow(0 0 20px rgba(139, 92, 246, 0.5));
        }

        .category-title {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.5rem;
            font-weight: 600;
            background: linear-gradient(135deg, #fff 0%, rgba(255, 255, 255, 0.8) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .category-count {
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(99, 102, 241, 0.2) 100%);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.85rem;
            color: #c4b5fd;
            font-weight: 600;
        }

        /* Award Item */
        .award-item {
            padding: 16px;
            margin: 10px 0;
            background: rgba(255, 255, 255, 0.02);
            border-radius: 12px;
            border-left: 3px solid rgba(139, 92, 246, 0.5);
            transition: all 0.3s ease;
        }

        .award-item:hover {
            background: rgba(139, 92, 246, 0.08);
            border-left: 3px solid #a78bfa;
            transform: translateX(5px);
        }

        .award-title {
            color: rgba(255, 255, 255, 0.95);
            font-weight: 500;
            font-size: 0.95rem;
            margin-bottom: 6px;
        }

        .award-meta {
            color: rgba(255, 255, 255, 0.5);
            font-size: 0.8rem;
        }

        /* Skills Grid */
        .skill-tag {
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(99, 102, 241, 0.1) 100%);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(139, 92, 246, 0.2);
            color: rgba(255, 255, 255, 0.9);
            padding: 10px 18px;
            border-radius: 30px;
            text-align: center;
            font-weight: 500;
            font-size: 0.9rem;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: default;
            display: inline-block;
            margin: 4px;
        }

        .skill-tag:hover {
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.25) 0%, rgba(99, 102, 241, 0.25) 100%);
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 8px 25px rgba(139, 92, 246, 0.3);
            border: 1px solid rgba(139, 92, 246, 0.5);
        }

        /* Floating Elements */
        .floating {
            animation: float 6s ease-in-out infinite;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-15px); }
        }

        /* Glow Effect */
        .glow {
            box-shadow: 0 0 40px rgba(139, 92, 246, 0.4),
                        0 0 80px rgba(139, 92, 246, 0.2),
                        0 0 120px rgba(139, 92, 246, 0.1);
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }

        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.02);
        }

        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #818cf8 0%, #a78bfa 100%);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #a78bfa 0%, #c4b5fd 100%);
        }

        /* Text Styles */
        .text-gradient {
            background: linear-gradient(135deg, #818cf8 0%, #c4b5fd 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .text-white {
            color: rgba(255, 255, 255, 0.9);
        }

        .text-muted {
            color: rgba(255, 255, 255, 0.5);
        }

        /* Sidebar Header */
        .sidebar-header {
            color: white;
            text-align: center;
            padding: 24px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            margin-bottom: 24px;
        }

        .sidebar-name {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.4rem;
            font-weight: 600;
            background: linear-gradient(135deg, #818cf8 0%, #c4b5fd 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }

        .sidebar-title {
            color: rgba(255, 255, 255, 0.5);
            font-size: 0.85rem;
            letter-spacing: 0.15em;
            text-transform: uppercase;
        }

        /* Timeline */
        .timeline-item {
            position: relative;
            padding-left: 30px;
            margin-bottom: 24px;
        }

        .timeline-item::before {
            content: '';
            position: absolute;
            left: 0;
            top: 8px;
            width: 12px;
            height: 12px;
            background: linear-gradient(135deg, #818cf8 0%, #a78bfa 100%);
            border-radius: 50%;
            box-shadow: 0 0 20px rgba(139, 92, 246, 0.5);
        }

        .timeline-item::after {
            content: '';
            position: absolute;
            left: 5px;
            top: 24px;
            width: 2px;
            height: calc(100% + 8px);
            background: linear-gradient(180deg, rgba(139, 92, 246, 0.5) 0%, transparent 100%);
        }

        .timeline-item:last-child::after {
            display: none;
        }

        /* Stats Counter Animation */
        @keyframes countUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .stat-animated {
            animation: countUp 0.6s ease-out forwards;
        }

        /* Pulse Animation */
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        .pulse {
            animation: pulse 2s ease-in-out infinite;
        }

        /* Tab Styles */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: transparent;
        }

        .stTabs [data-baseweb="tab"] {
            background: rgba(255, 255, 255, 0.03);
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: rgba(255, 255, 255, 0.7);
            padding: 12px 24px;
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(99, 102, 241, 0.2) 100%);
            border: 1px solid rgba(139, 92, 246, 0.4);
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)


# Load CSS
load_css()

# Sidebar Navigation
with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-header">
        <div class="sidebar-name">{profile_data.get('name', 'Alisher Beisembekov')}</div>
        <div class="sidebar-title">Portfolio Navigation</div>
    </div>
    """, unsafe_allow_html=True)

    # Navigation buttons
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.current_page = 'home'
    if st.button("💼 Career", use_container_width=True):
        st.session_state.current_page = 'career'
    if st.button("🔬 Research", use_container_width=True):
        st.session_state.current_page = 'research'
    if st.button("💻 Projects", use_container_width=True):
        st.session_state.current_page = 'projects'
    if st.button("🏆 Achievements", use_container_width=True):
        st.session_state.current_page = 'achievements'
    if st.button("📊 Analytics", use_container_width=True):
        st.session_state.current_page = 'analytics'

    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; padding: 20px 0;">
        <p style="color: rgba(255, 255, 255, 0.5); margin-bottom: 15px; font-size: 0.85rem; letter-spacing: 0.1em;">CONNECT</p>
        <div style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap;">
            <a href="{profile_data.get('url', 'https://www.linkedin.com/in/alisher-beisembekov/')}" target="_blank" style="color: rgba(255, 255, 255, 0.6); text-decoration: none; font-size: 1.5rem; transition: all 0.3s ease;">💼</a>
            <a href="https://github.com/damn-glitch" target="_blank" style="color: rgba(255, 255, 255, 0.6); text-decoration: none; font-size: 1.5rem; transition: all 0.3s ease;">💻</a>
            <a href="https://www.smartr.me/me/alisher.beisembekov" target="_blank" style="color: rgba(255, 255, 255, 0.6); text-decoration: none; font-size: 1.5rem; transition: all 0.3s ease;">🌐</a>
            <a href="https://www.credly.com/users/alisher-beisembekov/badges" target="_blank" style="color: rgba(255, 255, 255, 0.6); text-decoration: none; font-size: 1.5rem; transition: all 0.3s ease;">🏅</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Page content based on selection
if st.session_state.current_page == 'home':
    # Hero Section
    st.markdown(f'<h1 class="hero-name floating">{profile_data.get("name", "Alisher Beisembekov")}</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-title">Polymath • Tech Innovator • World Record Holder</p>', unsafe_allow_html=True)

    # Quick Stats from profile data
    st.markdown("---")
    cols = st.columns(4)

    # Calculate stats from profile
    total_awards = len(profile_data.get('honors_and_awards', []))
    total_projects = len([p for p in profile_data.get('projects', []) if p.get('name')])
    total_certs = len(profile_data.get('certifications', []))
    total_publications = len(profile_data.get('publications', []))

    metrics = [
        ("Awards", f"{total_awards}+", "🏆"),
        ("Projects", f"{total_projects}+", "💡"),
        ("Certifications", f"{total_certs}+", "🎓"),
        ("Publications", f"{total_publications}", "📚")
    ]

    for col, (label, value, icon) in zip(cols, metrics):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 2.5rem; margin-bottom: 12px; filter: drop-shadow(0 0 10px rgba(139, 92, 246, 0.5));">{icon}</div>
                <div class="metric-number">{value}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    # Main Content
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Redefining Possibilities</h2>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        <p class="text-white" style="font-size: 1.1rem; line-height: 1.9; margin-bottom: 24px;">
        Pioneering the intersection of technology, innovation, and human potential. Building revolutionary
        solutions across AI, blockchain, quantum computing, and beyond. Leading multiple companies while
        pushing the boundaries of what's possible in computer vision, autonomous systems, and intelligent platforms.
        </p>
        """, unsafe_allow_html=True)

        # Current Positions from profile.json
        st.markdown('<h3 class="text-gradient" style="margin-top: 30px; font-size: 1.4rem;">Current Leadership Roles</h3>',
                    unsafe_allow_html=True)

        # Get current positions (positions with "Present" in end_date)
        current_positions = []
        for exp in profile_data.get('experience', []):
            if exp.get('date', {}).get('end_date') == 'Present' and exp.get('title'):
                current_positions.append(exp)

        for position in current_positions[:4]:  # Show top 4 current positions
            company = position.get('company_name', '')
            title = position.get('title', '')
            start_date = position.get('date', {}).get('start_date', '')
            description = position.get('description', '')

            # Clean HTML from description
            if description:
                import re
                description = re.sub('<[^<]+?>', ' ', description)
                description = description[:200] + '...' if len(description) > 200 else description

            st.markdown(f"""
            <div class="achievement-card">
                <h4 class="text-white" style="margin-bottom: 8px; font-size: 1.1rem;">{title}</h4>
                <p class="text-gradient" style="font-weight: 600; margin-bottom: 4px;">{company}</p>
                <p class="text-muted" style="font-size: 0.85rem; margin-bottom: 12px;">{start_date} - Present</p>
                <p class="text-white" style="font-size: 0.9rem; line-height: 1.6; opacity: 0.8;">{description}</p>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        # Languages from profile.json
        st.markdown('<h3 class="text-gradient" style="font-size: 1.2rem;">Languages</h3>', unsafe_allow_html=True)
        for lang in profile_data.get('languages', []):
            proficiency = lang.get('description', '')
            st.markdown(f'''
            <div class="skill-tag" style="display: block; margin: 8px 0;">
                {lang.get('name', '')}
                <span style="font-size: 0.75rem; opacity: 0.7;">({proficiency.split()[0] if proficiency else ''})</span>
            </div>
            ''', unsafe_allow_html=True)

        # Education from profile.json
        st.markdown('<h3 class="text-gradient" style="margin-top: 30px; font-size: 1.2rem;">Education</h3>', unsafe_allow_html=True)
        for edu in profile_data.get('education', [])[:2]:
            st.markdown(f"""
            <div class="achievement-card">
                <h4 class="text-white" style="font-size: 0.95rem;">{edu.get('degree', '')}</h4>
                <p class="text-gradient" style="font-weight: 500; font-size: 0.9rem;">{edu.get('major', '')}</p>
                <p class="text-muted" style="font-size: 0.8rem;">{edu.get('university_name', '')}</p>
                <p class="text-muted" style="font-size: 0.75rem;">{edu.get('date', {}).get('start_date', '')} - {edu.get('date', {}).get('end_date', '')}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_page == 'career':
    st.markdown('<h1 class="hero-name">Career Journey</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-title">Professional Evolution & Leadership</p>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Professional Timeline</h2>', unsafe_allow_html=True)

    # Get all experience from profile.json
    for i, exp in enumerate(profile_data.get('experience', [])):
        if not exp.get('title') or exp.get('title') == exp.get('company_name'):
            continue

        title = exp.get('title', '')
        company = exp.get('company_name', '')
        start_date = exp.get('date', {}).get('start_date', '')
        end_date = exp.get('date', {}).get('end_date', 'Present')
        description = exp.get('description', '')
        location = exp.get('location', '')

        # Clean HTML from description
        if description:
            import re
            description = re.sub('<[^<]+?>', ' ', description)
            description = description[:400] + '...' if len(description) > 400 else description

        period = f"{start_date} - {end_date}" if start_date else ""

        st.markdown(f'''
        <div class="achievement-card">
            <div style="display: flex; align-items: start; gap: 20px;">
                <div style="min-width: 50px; height: 50px; background: linear-gradient(135deg, #818cf8 0%, #a78bfa 100%);
                            border-radius: 14px; display: flex; align-items: center; justify-content: center; color: white;
                            font-weight: bold; font-size: 1.2rem; box-shadow: 0 8px 25px rgba(139, 92, 246, 0.3);">
                    {i + 1}
                </div>
                <div style="flex: 1;">
                    <h3 class="text-white" style="margin-bottom: 6px; font-size: 1.15rem;">{title}</h3>
                    <p class="text-gradient" style="font-weight: 600; font-size: 1rem; margin-bottom: 4px;">{company}</p>
                    <p class="text-muted" style="font-size: 0.85rem;">{period} {f"• {location}" if location else ""}</p>
                    <p class="text-white" style="margin-top: 12px; font-size: 0.9rem; line-height: 1.7; opacity: 0.85;">{description}</p>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_page == 'research':
    st.markdown('<h1 class="hero-name">Research & Publications</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-title">Advancing the Frontiers of Knowledge</p>', unsafe_allow_html=True)

    # Publications from profile.json
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Publications</h2>', unsafe_allow_html=True)

    for pub in profile_data.get('publications', []):
        st.markdown(f'''
        <div class="achievement-card">
            <h3 class="text-white" style="font-size: 1.1rem; margin-bottom: 10px;">{pub.get('title', '')}</h3>
            <p class="text-gradient" style="font-weight: 600; margin-bottom: 8px;">
                {pub.get('publisher', '')} {f"• {pub.get('publication_date', '')}" if pub.get('publication_date') else ""}
            </p>
            <p class="text-white" style="font-size: 0.9rem; line-height: 1.7; opacity: 0.85;">{pub.get('description', '')}</p>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Certifications from profile.json
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Certifications</h2>', unsafe_allow_html=True)

    cols = st.columns(2)
    for i, cert in enumerate(profile_data.get('certifications', [])):
        with cols[i % 2]:
            st.markdown(f'''
            <div class="achievement-card">
                <h4 class="text-white" style="font-size: 0.95rem; margin-bottom: 8px;">{cert.get('title', '')}</h4>
                <p class="text-gradient" style="font-weight: 500; font-size: 0.85rem;">{cert.get('issuer', '')}</p>
                <p class="text-muted" style="font-size: 0.8rem;">{cert.get('issued_date', '').split(' Credential')[0] if cert.get('issued_date') else ''}</p>
            </div>
            ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_page == 'projects':
    st.markdown('<h1 class="hero-name">Innovation Portfolio</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-title">Building Tomorrow\'s Technology</p>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Featured Projects</h2>', unsafe_allow_html=True)

    # Get projects from profile.json
    projects = [p for p in profile_data.get('projects', []) if p.get('name') and p.get('description')]

    for project in projects:
        name = project.get('name', '')
        description = project.get('description', '')
        start_date = project.get('date', {}).get('start_date', '') if project.get('date') else ''
        end_date = project.get('date', {}).get('end_date', '') if project.get('date') else ''

        # Clean description
        if description:
            import re
            description = re.sub(r'[✅🚀🔧📊⚡🧠📈💡]', '', description)
            description = description[:500] + '...' if len(description) > 500 else description

        period = f"{start_date} - {end_date if end_date else 'Present'}" if start_date else ""

        st.markdown(f'''
        <div class="achievement-card">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;">
                <h3 class="text-white" style="font-size: 1.1rem; flex: 1;">{name}</h3>
                <span style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(5, 150, 105, 0.2) 100%);
                            color: #6ee7b7; padding: 6px 14px; border-radius: 20px; font-size: 0.8rem;
                            font-weight: 500; white-space: nowrap;">
                    {period}
                </span>
            </div>
            <p class="text-white" style="font-size: 0.9rem; line-height: 1.7; opacity: 0.85;">{description}</p>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_page == 'achievements':
    st.markdown('<h1 class="hero-name">Achievements</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-title">Excellence Across Multiple Disciplines</p>', unsafe_allow_html=True)

    # Get categorized awards
    categorized_awards = get_categorized_awards()

    # Category icons and colors
    category_config = {
        "Sports": {"icon": "🏋️", "color": "#ef4444", "gradient": "from-red-500 to-orange-500"},
        "Science": {"icon": "🔬", "color": "#8b5cf6", "gradient": "from-purple-500 to-indigo-500"},
        "Technology": {"icon": "💻", "color": "#3b82f6", "gradient": "from-blue-500 to-cyan-500"},
        "Entrepreneurship": {"icon": "🚀", "color": "#10b981", "gradient": "from-green-500 to-emerald-500"},
        "Academic": {"icon": "🎓", "color": "#f59e0b", "gradient": "from-amber-500 to-yellow-500"},
        "Chess": {"icon": "♟️", "color": "#6366f1", "gradient": "from-indigo-500 to-purple-500"},
        "Extra": {"icon": "✨", "color": "#ec4899", "gradient": "from-pink-500 to-rose-500"}
    }

    # Overview Stats
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Achievement Overview</h2>', unsafe_allow_html=True)

    cols = st.columns(len([c for c, awards in categorized_awards.items() if awards]))
    col_idx = 0

    for category, awards in categorized_awards.items():
        if awards:
            config = category_config.get(category, {"icon": "🏆", "color": "#818cf8"})
            with cols[col_idx]:
                st.markdown(f'''
                <div class="metric-card">
                    <div style="font-size: 2.5rem; margin-bottom: 8px;">{config["icon"]}</div>
                    <div class="metric-number">{len(awards)}</div>
                    <div class="metric-label">{category}</div>
                </div>
                ''', unsafe_allow_html=True)
            col_idx += 1

    st.markdown('</div>', unsafe_allow_html=True)

    # Tabs for each category
    tab_names = [f"{category_config[cat]['icon']} {cat}" for cat, awards in categorized_awards.items() if awards]
    tabs = st.tabs(tab_names)

    tab_idx = 0
    for category, awards in categorized_awards.items():
        if awards:
            with tabs[tab_idx]:
                config = category_config.get(category, {"icon": "🏆", "color": "#818cf8"})

                st.markdown(f'''
                <div class="category-card">
                    <div class="category-header">
                        <span class="category-icon">{config["icon"]}</span>
                        <span class="category-title">{category} Achievements</span>
                        <span class="category-count">{len(awards)} awards</span>
                    </div>
                ''', unsafe_allow_html=True)

                for award in awards:
                    title = award.get('title', '')
                    issuer = award.get('issuer', '')
                    date = award.get('issued_date', '')
                    description = award.get('description', '')

                    st.markdown(f'''
                    <div class="award-item">
                        <div class="award-title">{title}</div>
                        <div class="award-meta">{issuer} {f"• {date}" if date else ""}</div>
                        {f'<p class="text-white" style="font-size: 0.85rem; margin-top: 8px; opacity: 0.7;">{description[:200]}...</p>' if description and len(description) > 10 else ''}
                    </div>
                    ''', unsafe_allow_html=True)

                st.markdown('</div>', unsafe_allow_html=True)
            tab_idx += 1

elif st.session_state.current_page == 'analytics':
    st.markdown('<h1 class="hero-name">Analytics Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-title">Data-Driven Success Metrics</p>', unsafe_allow_html=True)

    # Calculate statistics from profile
    categorized_awards = get_categorized_awards()
    total_awards = len(profile_data.get('honors_and_awards', []))
    total_projects = len([p for p in profile_data.get('projects', []) if p.get('name')])
    total_experience = len([e for e in profile_data.get('experience', []) if e.get('title')])
    total_certs = len(profile_data.get('certifications', []))

    # Overall Statistics
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Lifetime Statistics</h2>', unsafe_allow_html=True)

    cols = st.columns(4)
    stats = [
        ("Total Awards", total_awards, "🏆"),
        ("Projects", total_projects, "💡"),
        ("Certifications", total_certs, "🎓"),
        ("Positions Held", total_experience, "💼")
    ]

    for col, (label, value, icon) in zip(cols, stats):
        with col:
            st.markdown(f'''
            <div class="metric-card glow">
                <div style="font-size: 2.5rem; margin-bottom: 8px;">{icon}</div>
                <div class="metric-number">{value}</div>
                <div class="metric-label">{label}</div>
            </div>
            ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Achievement Distribution Chart
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Achievement Distribution</h2>', unsafe_allow_html=True)

    # Create pie chart for achievement categories
    category_counts = {cat: len(awards) for cat, awards in categorized_awards.items() if awards}

    fig = go.Figure(data=[go.Pie(
        labels=list(category_counts.keys()),
        values=list(category_counts.values()),
        hole=0.5,
        marker=dict(
            colors=['#ef4444', '#8b5cf6', '#3b82f6', '#10b981', '#f59e0b', '#6366f1', '#ec4899'],
            line=dict(color='rgba(255,255,255,0.1)', width=2)
        ),
        textfont=dict(color='white', size=14),
        hovertemplate="<b>%{label}</b><br>%{value} awards<br>%{percent}<extra></extra>"
    )])

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=400,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(size=12)
        ),
        margin=dict(t=20, b=80, l=20, r=20)
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Awards Timeline
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Awards Timeline</h2>', unsafe_allow_html=True)

    # Count awards by year
    year_counts = {}
    for award in profile_data.get('honors_and_awards', []):
        date_str = award.get('issued_date', '')
        if date_str:
            # Extract year from date string
            import re
            year_match = re.search(r'20\d{2}', date_str)
            if year_match:
                year = int(year_match.group())
                year_counts[year] = year_counts.get(year, 0) + 1

    if year_counts:
        years = sorted(year_counts.keys())
        counts = [year_counts[y] for y in years]

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=years,
            y=counts,
            marker=dict(
                color=counts,
                colorscale=[[0, '#818cf8'], [0.5, '#a78bfa'], [1, '#c4b5fd']],
                line=dict(color='rgba(255,255,255,0.2)', width=1)
            ),
            hovertemplate="<b>%{x}</b><br>%{y} awards<extra></extra>"
        ))

        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=350,
            xaxis=dict(
                gridcolor='rgba(255,255,255,0.05)',
                tickfont=dict(size=12)
            ),
            yaxis=dict(
                gridcolor='rgba(255,255,255,0.05)',
                title="Awards Count",
                tickfont=dict(size=12)
            ),
            margin=dict(t=20, b=40, l=60, r=20)
        )

        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Skills/Expertise from Certifications
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Expertise Areas</h2>', unsafe_allow_html=True)

    # Extract issuer organizations for expertise
    issuers = {}
    for cert in profile_data.get('certifications', []):
        issuer = cert.get('issuer', '')
        if issuer:
            # Clean up issuer name
            issuer = issuer.split('(')[0].strip()
            issuers[issuer] = issuers.get(issuer, 0) + 1

    if issuers:
        sorted_issuers = sorted(issuers.items(), key=lambda x: x[1], reverse=True)[:8]

        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            y=[i[0] for i in sorted_issuers],
            x=[i[1] for i in sorted_issuers],
            orientation='h',
            marker=dict(
                color=[i[1] for i in sorted_issuers],
                colorscale=[[0, '#818cf8'], [1, '#c4b5fd']],
                line=dict(color='rgba(255,255,255,0.2)', width=1)
            ),
            hovertemplate="<b>%{y}</b><br>%{x} certifications<extra></extra>"
        ))

        fig3.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=350,
            xaxis=dict(
                gridcolor='rgba(255,255,255,0.05)',
                title="Certifications",
                tickfont=dict(size=11)
            ),
            yaxis=dict(
                gridcolor='rgba(255,255,255,0.05)',
                tickfont=dict(size=11)
            ),
            margin=dict(t=20, b=40, l=150, r=20)
        )

        st.plotly_chart(fig3, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown(f"""
<div style="margin-top: 80px; padding: 40px 0; text-align: center; border-top: 1px solid rgba(255,255,255,0.08);">
    <p class="text-muted" style="font-size: 0.9rem; margin-bottom: 20px;">
        © 2025 {profile_data.get('name', 'Alisher Beisembekov')}. Building the future through innovation, one breakthrough at a time.
    </p>
    <div style="display: flex; justify-content: center; gap: 24px; flex-wrap: wrap;">
        <a href="{profile_data.get('url', 'https://www.linkedin.com/in/alisher-beisembekov/')}" target="_blank"
           style="color: rgba(255, 255, 255, 0.5); text-decoration: none; transition: all 0.3s ease; font-size: 0.85rem;">LinkedIn</a>
        <a href="https://github.com/damn-glitch" target="_blank"
           style="color: rgba(255, 255, 255, 0.5); text-decoration: none; transition: all 0.3s ease; font-size: 0.85rem;">GitHub</a>
        <a href="https://www.smartr.me/me/alisher.beisembekov" target="_blank"
           style="color: rgba(255, 255, 255, 0.5); text-decoration: none; transition: all 0.3s ease; font-size: 0.85rem;">SmartR</a>
        <a href="https://www.credly.com/users/alisher-beisembekov/badges" target="_blank"
           style="color: rgba(255, 255, 255, 0.5); text-decoration: none; transition: all 0.3s ease; font-size: 0.85rem;">Credly</a>
    </div>
    <p class="text-muted" style="font-size: 0.75rem; margin-top: 20px; opacity: 0.5;">
        {profile_data.get('location', 'Astana, Kazakhstan')} • {profile_data.get('followers', '')} • {profile_data.get('connections', '')}
    </p>
</div>
""", unsafe_allow_html=True)
