import streamlit as st
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Alisher Beisembekov | Polymath & Tech Innovator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# Advanced Post-Modern CSS Design
def load_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700;800;900&display=swap');

        /* Global Styles */
        * {
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            background: linear-gradient(135deg, #0F0C29 0%, #302B63 50%, #24243e 100%);
            background-attachment: fixed;
        }

        /* Hide Streamlit Branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background: rgba(15, 12, 41, 0.8);
            backdrop-filter: blur(20px);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }

        section[data-testid="stSidebar"] .stButton > button {
            background: rgba(255, 255, 255, 0.05);
            color: rgba(255, 255, 255, 0.9);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 15px;
            width: 100%;
            transition: all 0.3s ease;
            font-weight: 500;
            margin-bottom: 10px;
        }

        section[data-testid="stSidebar"] .stButton > button:hover {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.3) 0%, rgba(118, 75, 162, 0.3) 100%);
            border: 1px solid rgba(255, 255, 255, 0.3);
            transform: translateX(5px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }

        /* Animated Background */
        .animated-bg {
            position: fixed;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            z-index: -1;
            background: linear-gradient(270deg, #0F0C29, #302B63, #24243e, #0F0C29);
            background-size: 800% 800%;
            animation: gradientShift 20s ease infinite;
        }

        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Glassmorphism Cards */
        .glass-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 30px;
            margin: 20px 0;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            transition: all 0.3s ease;
        }

        .glass-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px 0 rgba(31, 38, 135, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        /* Hero Section */
        .hero-name {
            font-family: 'Space Grotesk', sans-serif;
            font-size: clamp(3rem, 8vw, 6rem);
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 20%, #f093fb 40%, #f5576c 60%, #fda085 80%, #667eea 100%);
            background-size: 200% 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            animation: gradientText 5s ease infinite;
            letter-spacing: -0.02em;
            line-height: 1.1;
            margin-bottom: 0;
        }

        @keyframes gradientText {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .hero-title {
            font-family: 'Space Grotesk', sans-serif;
            font-size: clamp(1.2rem, 3vw, 1.8rem);
            color: rgba(255, 255, 255, 0.9);
            text-align: center;
            margin-top: 10px;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            font-weight: 300;
        }

        /* Metric Cards */
        .metric-card {
            background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 25px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        }

        .metric-card:hover {
            transform: translateY(-5px) scale(1.02);
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }

        .metric-number {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 5px;
        }

        .metric-label {
            color: rgba(255, 255, 255, 0.7);
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }

        /* Section Headers */
        .section-header {
            font-family: 'Space Grotesk', sans-serif;
            font-size: clamp(2rem, 4vw, 3rem);
            font-weight: 600;
            background: linear-gradient(135deg, #fff 0%, rgba(255,255,255,0.7) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 40px 0 30px 0;
            position: relative;
            padding-bottom: 15px;
        }

        .section-header:after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100px;
            height: 3px;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            border-radius: 2px;
        }

        /* Achievement Cards */
        .achievement-card {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 25px;
            margin-bottom: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .achievement-card:before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
            transition: left 0.5s ease;
        }

        .achievement-card:hover:before {
            left: 100%;
        }

        .achievement-card:hover {
            transform: translateX(5px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
        }

        /* Skills Grid */
        .skill-tag {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: rgba(255, 255, 255, 0.9);
            padding: 12px 20px;
            border-radius: 25px;
            text-align: center;
            font-weight: 500;
            transition: all 0.3s ease;
            cursor: default;
            display: inline-block;
            margin: 5px;
        }

        .skill-tag:hover {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
            transform: translateY(-3px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }

        /* Floating Elements */
        .floating {
            animation: float 6s ease-in-out infinite;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
        }

        /* Glow Effect */
        .glow {
            box-shadow: 0 0 30px rgba(102, 126, 234, 0.6),
                        0 0 60px rgba(102, 126, 234, 0.4),
                        0 0 90px rgba(102, 126, 234, 0.2);
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
        }

        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.05);
        }

        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 5px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        }

        /* Company Links */
        .company-link {
            color: inherit;
            text-decoration: none;
            transition: all 0.3s ease;
            position: relative;
        }

        .company-link:hover {
            text-shadow: 0 0 10px rgba(102, 126, 234, 0.8);
            transform: translateX(3px);
        }

        .company-link:after {
            content: ' 🔗';
            opacity: 0;
            transition: opacity 0.3s ease;
            font-size: 0.8em;
        }

        .company-link:hover:after {
            opacity: 0.7;
        }

        /* Text Styles */
        .text-gradient {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .text-white {
            color: rgba(255, 255, 255, 0.9);
        }

        .text-muted {
            color: rgba(255, 255, 255, 0.6);
        }

        /* Sidebar Header */
        .sidebar-header {
            color: white;
            text-align: center;
            padding: 20px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            margin-bottom: 20px;
        }

        .sidebar-name {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.5rem;
            font-weight: 600;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 5px;
        }

        .sidebar-title {
            color: rgba(255, 255, 255, 0.7);
            font-size: 0.9rem;
            letter-spacing: 0.1em;
        }
    </style>

    <div class="animated-bg"></div>
    """, unsafe_allow_html=True)

# Load CSS
load_css()

# Sidebar Navigation
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <div class="sidebar-name">Alisher Beisembekov</div>
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
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <p style="color: rgba(255, 255, 255, 0.6); margin-bottom: 15px;">Connect</p>
        <div style="display: flex; justify-content: center; gap: 15px;">
            <a href="https://www.linkedin.com/in/alisher-beisembekov/" style="color: rgba(255, 255, 255, 0.7); text-decoration: none;">💼</a>
            <a href="https://github.com/damn-glitch" style="color: rgba(255, 255, 255, 0.7); text-decoration: none;">💻</a>
            <a href="https://www.smartr.me/me/alisher.beisembekov" style="color: rgba(255, 255, 255, 0.7); text-decoration: none;">🌐</a>
            <a href="https://www.credly.com/users/alisher-beisembekov/badges" style="color: rgba(255, 255, 255, 0.7); text-decoration: none;">🏅</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Page content based on selection
if st.session_state.current_page == 'home':
    # Hero Section
    st.markdown('<h1 class="hero-name floating">Alisher Beisembekov</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-title">Polymath • Tech Innovator • Visionary Leader</p>', unsafe_allow_html=True)

    # Quick Stats
    st.markdown("---")
    cols = st.columns(4)
    metrics = [
        ("Patents", "12+", "📋"),
        ("Publications", "3", "📚"),
        ("Projects", "45+", "💡"),
        ("Awards", "80+", "🏆")
    ]

    for col, (label, value, icon) in zip(cols, metrics):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 2rem; margin-bottom: 10px;">{icon}</div>
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
        <p class="text-white" style="font-size: 1.1rem; line-height: 1.8;">
        Pioneering the intersection of technology, innovation, and human potential. Building revolutionary 
        solutions across AI, blockchain, quantum computing, and beyond. Leading multiple companies while 
        pushing the boundaries of what's possible in computer vision, autonomous systems, and intelligent platforms.
        </p>
        """, unsafe_allow_html=True)

        # Current Positions
        st.markdown('<h3 class="text-gradient" style="margin-top: 30px;">Current Leadership Roles</h3>',
                    unsafe_allow_html=True)

        positions = [
            {
                "title": "Co-Founder",
                "company": "Avtovin.kz",
                "period": "May 2025 - Present",
                "description": "Revolutionizing automotive warranty and service delivery through technology-driven solutions across Kazakhstan",
                "website": "https://avtovin.kz/"
            },
            {
                "title": "Chief Information Officer",
                "company": "Aleem",
                "period": "Mar 2025 - Present",
                "description": "Leading AI-powered EdTech and Web3 language learning platform development",
                "website": None
            },
            {
                "title": "Chief Executive Officer & Founder",
                "company": "Infinitum Intelligence",
                "period": "Oct 2023 - Present",
                "description": "Building AI, blockchain, and computer vision solutions for healthcare, finance, and urban planning",
                "website": None
            },
            {
                "title": "Chief Information Officer & Co-Founder",
                "company": "JASAIM",
                "period": "Feb 2024 - Present",
                "description": "Driving technology innovation in educational and philanthropic sectors",
                "website": None
            }
        ]

        for position in positions:
            # Create company name with optional link
            if position.get("website"):
                company_html = f'<a href="{position["website"]}" target="_blank" class="company-link text-gradient" style="font-weight: 600;">{position["company"]}</a>'
            else:
                company_html = f'<span class="text-gradient" style="font-weight: 600;">{position["company"]}</span>'
                
            st.markdown(f"""
            <div class="achievement-card">
                <h4 class="text-white">{position["title"]}</h4>
                <p>{company_html}</p>
                <p class="text-muted">{position["period"]}</p>
                <p class="text-white" style="margin-top: 10px;">{position["description"]}</p>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        # Core Expertise
        st.markdown('<h3 class="text-gradient">Core Expertise</h3>', unsafe_allow_html=True)

        expertise = {
            "AI & Technology": ["Machine Learning", "Computer Vision", "Blockchain", "Quantum Computing"],
            "Leadership": ["Strategic Planning", "Team Building", "Innovation", "R&D Management"],
            "Research": ["Patents", "Publications", "Speaking", "Mentorship"]
        }

        for category, skills in expertise.items():
            st.markdown(f'<p class="text-white" style="font-weight: 600; margin-top: 20px;">{category}</p>',
                        unsafe_allow_html=True)
            for skill in skills:
                st.markdown(f'<div class="skill-tag">{skill}</div>', unsafe_allow_html=True)

        # Languages
        st.markdown('<h3 class="text-gradient" style="margin-top: 30px;">Languages</h3>', unsafe_allow_html=True)
        languages = ["English (Native)", "Russian (Native)", "Kazakh (Native)", "French", "Turkish", "Ukrainian"]
        for lang in languages:
            st.markdown(f'<div class="skill-tag" style="margin: 5px 0;">{lang}</div>', unsafe_allow_html=True)

        # Education
        st.markdown('<h3 class="text-gradient" style="margin-top: 30px;">Education</h3>', unsafe_allow_html=True)
        st.markdown("""
        <div class="achievement-card">
            <h4 class="text-white">Bachelor's Degree</h4>
            <p class="text-gradient">Mathematics and Computer Science</p>
            <p class="text-muted">Rochester Institute of Technology, Dubai</p>
            <p class="text-muted">2020 - 2024 | Magna Cum Laude</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_page == 'career':
    st.markdown('<h1 class="hero-name">Career Journey</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-title">Professional Evolution & Leadership</p>', unsafe_allow_html=True)

    positions = [
        {
            "title": "Co-Founder",
            "company": "Carso.kz",
            "period": "May 2025 - Present",
            "description": "Leading automotive technology revolution in Kazakhstan",
            "achievements": ["Proprietary mobile/web applications", "Strategic partnerships", "Market leadership positioning"]
        },
        {
            "title": "Chief Information Officer",
            "company": "Aleem",
            "period": "Mar 2025 - Present",
            "description": "Revolutionary AI-powered language learning platform",
            "achievements": ["Web3 tokenomics integration", "AI-driven personalization", "Global market expansion"]
        },
        {
            "title": "Chief Executive Officer & Founder",
            "company": "Infinitum Intelligence",
            "period": "Oct 2023 - Present",
            "description": "Building the future of AI and blockchain technology",
            "achievements": ["9 flagship platforms delivered", "Multiple patents secured", "Global partnerships"]
        },
        {
            "title": "Lead Developer",
            "company": "IBM",
            "period": "May 2023 - Sep 2023",
            "description": "Advanced AI research and development",
            "achievements": ["AutoAI-for-Text optimization", "Benchmark infrastructure", "Performance improvements"]
        },
        {
            "title": "Senior Machine Learning Engineer",
            "company": "Google",
            "period": "Apr 2022 - Aug 2022",
            "description": "Real-time fraud detection and Google Translate enhancement",
            "achievements": ["30% fraud loss reduction", "15% BLEU score improvement", "Billions of events processed"]
        },
        {
            "title": "Senior Developer Python/C++",
            "company": "Yandex",
            "period": "Mar 2021 - Jun 2021",
            "description": "Yandex.Taxi platform upgrades and architecture",
            "achievements": ["99.9% uptime maintained", "25% API performance improvement", "Team mentorship"]
        }
    ]

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Professional Timeline</h2>', unsafe_allow_html=True)

    for i, position in enumerate(positions):
        color = "#667eea" if i < 3 else "#764ba2"
        # Create company name with optional link
        if position.get("website"):
            company_html = f'<a href="{position["website"]}" target="_blank" class="company-link text-gradient" style="font-weight: 600; font-size: 1.1rem;">{position["company"]}</a>'
        else:
            company_html = f'<span class="text-gradient" style="font-weight: 600; font-size: 1.1rem;">{position["company"]}</span>'
            
        st.markdown(f'''
        <div class="achievement-card">
            <div style="display: flex; align-items: start; gap: 20px;">
                <div style="min-width: 60px; height: 60px; background: linear-gradient(135deg, {color} 0%, #764ba2 100%); 
                            border-radius: 15px; display: flex; align-items: center; justify-content: center; color: white; 
                            font-weight: bold; font-size: 1.5rem;">
                    {i + 1}
                </div>
                <div style="flex: 1;">
                    <h3 class="text-white">{position["title"]}</h3>
                    <p class="text-gradient" style="font-weight: 600; font-size: 1.1rem;">{company_html}</p>
                    <p class="text-muted">{position["period"]}</p>
                    <p class="text-white" style="margin: 15px 0;">{position["description"]}</p>
                    <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 15px;">
                        {"".join([f'<span class="skill-tag">{achievement}</span>' for achievement in position["achievements"]])}
                    </div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Career Stats
    st.markdown('<h2 class="section-header">Career Impact</h2>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    stats = [
        ("Years Experience", "6+", "⏰"),
        ("Companies Led", "4", "🏢"),
        ("Major Projects", "45+", "🚀"),
        ("Team Members", "200+", "👥")
    ]

    for col, (label, value, icon) in zip([col1, col2, col3, col4], stats):
        with col:
            st.markdown(f'''
            <div class="metric-card glow">
                <div style="font-size: 2.5rem;">{icon}</div>
                <div class="metric-number">{value}</div>
                <div class="metric-label">{label}</div>
            </div>
            ''', unsafe_allow_html=True)

elif st.session_state.current_page == 'research':
    st.markdown('<h1 class="hero-name">Research & Innovation</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-title">Advancing the Frontiers of Knowledge</p>', unsafe_allow_html=True)

    # Research Areas
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Research Domains</h2>', unsafe_allow_html=True)

    research_areas = [
        {
            "area": "Artificial Intelligence & Machine Learning",
            "icon": "🧠",
            "focus": "Computer Vision, Deep Learning, Natural Language Processing, AutoML",
            "papers": 2,
            "patents": 8
        },
        {
            "area": "Blockchain & Distributed Systems",
            "icon": "🔗",
            "focus": "Smart Contracts, DeFi, Consensus Mechanisms, Decentralized Applications",
            "papers": 0,
            "patents": 4
        },
        {
            "area": "Computer Vision & Autonomous Systems",
            "icon": "👁️",
            "focus": "Real-time Processing, Object Detection, Autonomous Navigation",
            "papers": 1,
            "patents": 3
        },
        {
            "area": "Network Optimization & 5G/6G",
            "icon": "📡",
            "focus": "Speed Optimization, Edge Computing, Predictive Analytics",
            "papers": 0,
            "patents": 2
        }
    ]

    cols = st.columns(2)
    for i, area in enumerate(research_areas):
        with cols[i % 2]:
            st.markdown(f'''
            <div class="achievement-card">
                <div style="text-align: center;">
                    <div style="font-size: 4rem; margin-bottom: 15px;">{area["icon"]}</div>
                    <h3 class="text-gradient">{area["area"]}</h3>
                    <p class="text-white" style="margin: 15px 0;">{area["focus"]}</p>
                    <div style="display: flex; justify-content: space-around; margin-top: 20px;">
                        <div>
                            <p class="metric-number" style="font-size: 1.8rem;">{area["papers"]}</p>
                            <p class="text-muted">Papers</p>
                        </div>
                        <div>
                            <p class="metric-number" style="font-size: 1.8rem;">{area["patents"]}</p>
                            <p class="text-muted">Patents</p>
                        </div>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Publications
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Key Publications</h2>', unsafe_allow_html=True)

    publications = [
        {
            "title": "Study of the hydrocarbon-oxidizing activity of Bacillus subtillus on different substrates",
            "journal": "MSI",
            "year": 2017,
            "citations": "N/A",
            "description": "Bioremediation research using native microorganisms for oil pollution in Kazakhstan"
        },
        {
            "title": "Detecting Various Writing Styles in Documents Through Inherent Stylometric Analysis",
            "journal": "IEEE",
            "year": 2023,
            "citations": "N/A",
            "description": "K-Means clustering approach for detecting plagiarism and multiple writing styles"
        },
        {
            "title": "IoT and AI Applications for Healthcare Diagnostics",
            "journal": "IEEE",
            "year": 2023,
            "citations": "N/A",
            "description": "Comprehensive report on IoT/AI integration for sustainable healthcare systems"
        }
    ]

    for pub in publications:
        st.markdown(f'''
        <div class="achievement-card">
            <h3 class="text-white">{pub["title"]}</h3>
            <p class="text-gradient" style="font-weight: 600; margin: 10px 0;">{pub["journal"]} • {pub["year"]}</p>
            <p class="text-white" style="margin: 15px 0;">{pub["description"]}</p>
            <div style="display: flex; gap: 30px; margin-top: 15px;">
                <span class="text-white">📚 Citations: <strong>{pub["citations"]}</strong></span>
            </div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Patents
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Patent Portfolio</h2>', unsafe_allow_html=True)

    patents = [
        {"title": "DriveVision", "id": "KZ 60968", "year": "2025", "category": "Computer Vision"},
        {"title": "Hyperports - Blockchain Port Operations", "id": "KZ 59912", "year": "2025", "category": "Blockchain"},
        {"title": "AutoTrade - Automotive Dealership Management", "id": "KZ 59905", "year": "2025", "category": "AI/Business"},
        {"title": "XG SONIC - Network Speed Optimization", "id": "KZ 59121", "year": "2025", "category": "5G/6G"},
        {"title": "Carso - Auto Parts Trading Platform", "id": "KZ 58713", "year": "2025", "category": "AI/Marketplace"},
        {"title": "Shyndyq - AI Plagiarism Detector", "id": "KZ 47184", "year": "2024", "category": "AI/Education"}
    ]

    cols = st.columns(2)
    for i, patent in enumerate(patents):
        with cols[i % 2]:
            st.markdown(f'''
            <div class="achievement-card">
                <h4 class="text-white">{patent["title"]}</h4>
                <p class="text-gradient" style="font-weight: 600;">{patent["id"]} • {patent["year"]}</p>
                <span class="skill-tag">{patent["category"]}</span>
            </div>
            ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_page == 'projects':
    st.markdown('<h1 class="hero-name">Innovation Portfolio</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-title">Building Tomorrow\'s Technology</p>', unsafe_allow_html=True)

    # Featured Projects
    projects = [
        {
            "name": "XG SONIC - Network Speed Optimization",
            "category": "5G/6G Technology",
            "status": "Production",
            "description": "Revolutionary AI-powered speed optimization for 5G/6G networks with 66% latency reduction",
            "tech": ["LSTM", "CNN", "Python", "Edge Computing"],
            "metrics": {"Latency Reduction": "66%", "Throughput": "+150%", "Energy Savings": "30%"},
            "color": "#00ff88"
        },
        {
            "name": "Carso - Auto Parts Trading Platform",
            "category": "AI Marketplace",
            "status": "Production",
            "description": "Revolutionary auto parts marketplace with AI-powered matching and real-time trading",
            "tech": ["Python", "Flask", "PostgreSQL", "WebSocket"],
            "metrics": {"Sourcing Time": "-70%", "Price Reduction": "25%", "Satisfaction": "95%"},
            "color": "#00ff88"
        },
        {
            "name": "DriveVision - AI Driving Assessment",
            "category": "Computer Vision",
            "status": "Production",
            "description": "Computer vision solution for driving license exams with biometric authentication",
            "tech": ["PyTorch", "Transformers", "OpenCV", "Real-time Processing"],
            "metrics": {"Error Reduction": "25%", "Accuracy": "98%", "Processing": "Real-time"},
            "color": "#00ff88"
        },
        {
            "name": "Aleem - AI Language Learning",
            "category": "EdTech & Web3",
            "status": "Production",
            "description": "AI-powered language learning platform with Web3 tokenomics and 7-day fluency confidence",
            "tech": ["NLP", "Blockchain", "Telegram", "Web3"],
            "metrics": {"Error Reduction": "50%", "Reach": "300M+", "Revenue": "$200K"},
            "color": "#00ff88"
        },
        {
            "name": "Shyndyq - AI Plagiarism Detector",
            "category": "AI/Education",
            "status": "Production",
            "description": "Advanced plagiarism detection with writing style analysis and AI content recognition",
            "tech": ["AI/ML", "NLP", "Computer Vision", "Cross-platform"],
            "metrics": {"AI Detection": "100%", "Accuracy": "95%", "Speed": "Real-time"},
            "color": "#00ff88"
        },
        {
            "name": "HealthHub - AI Health Monitoring",
            "category": "Healthcare AI",
            "status": "Research",
            "description": "Comprehensive health monitoring platform integrating wearables with genetic analysis",
            "tech": ["AI/ML", "IoT", "Wearable Tech", "DNA Analysis"],
            "metrics": {"Monitoring": "Real-time", "Readmissions": "-20%", "Cost Savings": "Significant"},
            "color": "#ffa500"
        }
    ]

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Featured Projects</h2>', unsafe_allow_html=True)

    for project in projects:
        st.markdown(f'''
        <div class="achievement-card">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div style="flex: 1;">
                    <h3 class="text-white">{project["name"]}</h3>
                    <span style="background: {project["color"]}; color: #000; padding: 5px 15px; 
                                border-radius: 20px; font-weight: 600; font-size: 0.9rem; 
                                display: inline-block; margin: 10px 0;">
                        {project["status"]}
                    </span>
                    <p class="text-gradient" style="font-weight: 600; margin: 10px 0;">{project["category"]}</p>
                    <p class="text-white" style="margin: 15px 0;">{project["description"]}</p>

                    <div style="margin: 20px 0;">
                        <p class="text-muted" style="margin-bottom: 10px;">Technologies:</p>
                        <div style="display: flex; flex-wrap: wrap; gap: 10px;">
                            {"".join([f'<span class="skill-tag">{tech}</span>' for tech in project["tech"]])}
                        </div>
                    </div>

                    <div style="display: flex; gap: 30px; margin-top: 20px;">
                        {"".join([f'<div><p class="text-gradient" style="font-weight: 700; font-size: 1.2rem;">{value}</p><p class="text-muted" style="font-size: 0.9rem;">{key}</p></div>'
                                  for key, value in project["metrics"].items()])}
                    </div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Project Stats
    st.markdown('<h2 class="section-header">Impact Metrics</h2>', unsafe_allow_html=True)
    cols = st.columns(4)

    metrics = [
        ("Total Projects", "45+", "🚀"),
        ("Active Users", "1M+", "👥"),
        ("Patents Filed", "12+", "📋"),
        ("Open Source", "20+", "🌐")
    ]

    for col, (label, value, icon) in zip(cols, metrics):
        with col:
            st.markdown(f'''
            <div class="metric-card">
                <div style="font-size: 2.5rem;">{icon}</div>
                <div class="metric-number">{value}</div>
                <div class="metric-label">{label}</div>
            </div>
            ''', unsafe_allow_html=True)

elif st.session_state.current_page == 'achievements':
    st.markdown('<h1 class="hero-name">Achievements & Recognition</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-title">Excellence Across Multiple Disciplines</p>', unsafe_allow_html=True)

    # Recent Major Awards
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Recent Major Awards</h2>', unsafe_allow_html=True)

    recent_awards = [
        {
            "title": "Top 31 Among 241,817 Worldwide",
            "org": "ProjectEuler+ HackerRank",
            "year": 2025,
            "category": "Programming Excellence",
            "description": "Elite ranking in mathematical programming challenges"
        },
        {
            "title": "World Record Holder",
            "org": "IPC (International Powerlifting)",
            "year": 2025,
            "category": "Sports",
            "description": "Multiple world records in classic and extreme biceps curl"
        },
        {
            "title": "Undergraduate Research Scholar",
            "org": "Rochester Institute of Technology",
            "year": 2024,
            "category": "Academic Excellence",
            "description": "Prestigious recognition for exceptional research capabilities"
        },
        {
            "title": "International Astronomy Competition National Award",
            "org": "IAAC",
            "year": 2024,
            "category": "Science",
            "description": "National-level recognition in astronomy and astrophysics"
        },
        {
            "title": "ICE24 Competition Absolute Champions",
            "org": "United Nations",
            "year": 2024,
            "category": "AI Innovation",
            "description": "Global competition winner for AI in Healthcare solutions"
        }
    ]

    for award in recent_awards:
        st.markdown(f'''
        <div class="achievement-card">
            <div style="display: flex; align-items: start; gap: 20px;">
                <div style="font-size: 3rem;">🏆</div>
                <div style="flex: 1;">
                    <h3 class="text-white">{award["title"]}</h3>
                    <p class="text-gradient" style="font-weight: 600; font-size: 1.1rem;">{award["org"]} • {award["year"]}</p>
                    <p class="text-muted" style="margin: 10px 0;">{award["category"]}</p>
                    <p class="text-white">{award["description"]}</p>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Achievement Categories
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Achievement Categories</h2>', unsafe_allow_html=True)

    cols = st.columns(2)

    categories = [
        {
            "title": "Academic & Research",
            "icon": "🎓",
            "items": [
                "Dean's List (6 times)",
                "Magna Cum Laude Graduate",
                "International Math Challenge Silver",
                "Multiple Research Publications"
            ]
        },
        {
            "title": "Sports Excellence",
            "icon": "🥇",
            "items": [
                "World Records in Powerlifting",
                "Asia Champion in Multiple Events",
                "Master of Sports (Boxing, Martial Arts)",
                "Chess Arena International Master"
            ]
        },
        {
            "title": "Technology & Innovation",
            "icon": "💻",
            "items": [
                "Google Farewell Rounds Top 29/81,000",
                "Microsoft AI Skills Challenge Winner",
                "ZainTECH Data Challenge 3rd Place",
                "Multiple Hackathon Victories"
            ]
        },
        {
            "title": "Leadership & Mentorship",
            "icon": "🌟",
            "items": [
                "RIT Dubai Ambassador Award",
                "International Hackathon Mentor",
                "Guest Speaker at AI Conferences",
                "Teens in AI Mentor (1.5+ years)"
            ]
        }
    ]

    for i, category in enumerate(categories):
        with cols[i % 2]:
            st.markdown(f'''
            <div class="achievement-card">
                <div style="text-align: center; margin-bottom: 20px;">
                    <div style="font-size: 3rem;">{category["icon"]}</div>
                    <h3 class="text-gradient">{category["title"]}</h3>
                </div>
                <ul style="list-style: none; padding: 0;">
                    {"".join([f'<li class="text-white" style="margin: 10px 0;">• {item}</li>' for item in category["items"]])}
                </ul>
            </div>
            ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Achievement Timeline
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Achievement Timeline</h2>', unsafe_allow_html=True)

    timeline_awards = [
        {"year": 2025, "count": 8, "highlight": "World Records & #1 Country Choice"},
        {"year": 2024, "count": 12, "highlight": "UN Competition Winner & Research Scholar"},
        {"year": 2023, "count": 10, "highlight": "Google Top 29 & Microsoft AI Winner"},
        {"year": 2022, "count": 8, "highlight": "International Awards & Dean's List"},
        {"year": 2021, "count": 15, "highlight": "National Math Award & Hackathon Victories"},
        {"year": 2020, "count": 6, "highlight": "Multiple Certifications & Dean's List"}
    ]

    cols = st.columns(3)
    for i, item in enumerate(timeline_awards):
        with cols[i % 3]:
            st.markdown(f'''
            <div class="metric-card">
                <div class="metric-number">{item["count"]}</div>
                <div class="metric-label">{item["year"]}</div>
                <p class="text-white" style="font-size: 0.8rem; margin-top: 10px;">{item["highlight"]}</p>
            </div>
            ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_page == 'analytics':
    st.markdown('<h1 class="hero-name">Performance Analytics</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-title">Data-Driven Success Metrics</p>', unsafe_allow_html=True)

    # Overall Statistics
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Lifetime Statistics</h2>', unsafe_allow_html=True)

    cols = st.columns(4)
    stats = [
        ("Patents Filed", "12+", "📋", "From AI to Blockchain"),
        ("Research Papers", "3", "📚", "IEEE & MSI Publications"),
        ("Projects Completed", "45+", "💡", "Across Multiple Domains"),
        ("Awards Won", "80+", "🏆", "International Recognition"),
        ("Companies Founded", "4", "🏢", "Active Leadership Roles"),
        ("Team Members Led", "200+", "👥", "Across Organizations"),
        ("Conference Talks", "15+", "🎤", "Global Speaking"),
        ("Certifications", "50+", "🎓", "Technology & Leadership")
    ]

    for i, (label, value, icon, growth) in enumerate(stats):
        with cols[i % 4]:
            st.markdown(f'''
            <div class="metric-card">
                <div style="font-size: 2rem;">{icon}</div>
                <div class="metric-number">{value}</div>
                <div class="metric-label">{label}</div>
                <p class="text-gradient" style="font-size: 0.8rem; margin-top: 10px;">{growth}</p>
            </div>
            ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Growth Charts
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Career Growth Trajectory</h2>', unsafe_allow_html=True)

    # Create sample data for visualization based on real timeline
    years = [2019, 2020, 2021, 2022, 2023, 2024, 2025]
    projects = [2, 8, 15, 22, 30, 38, 45]
    patents = [0, 0, 1, 3, 6, 10, 12]
    team_size = [0, 10, 25, 50, 100, 150, 200]
    awards = [8, 15, 28, 45, 60, 70, 80]

    # Create plotly chart
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=years, y=projects,
        name='Projects',
        line=dict(color='#667eea', width=3),
        marker=dict(size=10)
    ))

    fig.add_trace(go.Scatter(
        x=years, y=patents,
        name='Patents',
        line=dict(color='#764ba2', width=3),
        marker=dict(size=10)
    ))

    fig.add_trace(go.Scatter(
        x=years, y=awards,
        name='Awards',
        line=dict(color='#f093fb', width=3),
        marker=dict(size=10)
    ))

    fig.add_trace(go.Scatter(
        x=years, y=team_size,
        name='Team Size',
        line=dict(color='#fda085', width=3),
        marker=dict(size=10),
        yaxis='y2'
    ))

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=400,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        yaxis=dict(
            title="Count",
            gridcolor='rgba(255,255,255,0.1)'
        ),
        yaxis2=dict(
            title="Team Size",
            overlaying='y',
            side='right',
            gridcolor='rgba(255,255,255,0.1)'
        ),
        xaxis=dict(
            title="Year",
            gridcolor='rgba(255,255,255,0.1)'
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Skills Distribution
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Core Competencies</h2>', unsafe_allow_html=True)

    skills_data = pd.DataFrame({
        'Skill': ['AI/ML', 'Leadership', 'Blockchain', 'Computer Vision', 'Research', 'Innovation'],
        'Level': [95, 92, 88, 90, 85, 94]
    })

    fig2 = px.bar(skills_data, x='Level', y='Skill', orientation='h',
                  color='Level', color_continuous_scale=['#667eea', '#764ba2'])

    fig2.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=300,
        showlegend=False,
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Impact Metrics
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Global Impact</h2>', unsafe_allow_html=True)

    impact_metrics = [
        {"metric": "Countries Reached", "value": "35+", "description": "Through Aleem platform"},
        {"metric": "Users Impacted", "value": "1M+", "description": "Across all platforms"},
        {"metric": "Revenue Generated", "value": "$50M+", "description": "Combined ventures"},
        {"metric": "Patents Pending", "value": "5+", "description": "Additional innovations"}
    ]

    cols = st.columns(2)
    for i, metric in enumerate(impact_metrics):
        with cols[i % 2]:
            st.markdown(f'''
            <div class="achievement-card">
                <h3 class="text-gradient">{metric["metric"]}</h3>
                <p class="metric-number" style="font-size: 2rem; margin: 10px 0;">{metric["value"]}</p>
                <p class="text-white">{metric["description"]}</p>
            </div>
            ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="margin-top: 60px; padding: 30px 0; text-align: center; border-top: 1px solid rgba(255,255,255,0.1);">
    <p class="text-muted">© 2025 Alisher Beisembekov. Building the future through innovation, one breakthrough at a time.</p>
    <div style="margin-top: 15px;">
        <a href="https://www.linkedin.com/in/alisher-beisembekov/" style="color: rgba(255, 255, 255, 0.6); margin: 0 10px;">LinkedIn</a>
        <a href="https://github.com/damn-glitch" style="color: rgba(255, 255, 255, 0.6); margin: 0 10px;">GitHub</a>
        <a href="https://www.smartr.me/me/alisher.beisembekov" style="color: rgba(255, 255, 255, 0.6); margin: 0 10px;">SmartR</a>
        <a href="https://www.credly.com/users/alisher-beisembekov/badges" style="color: rgba(255, 255, 255, 0.6); margin: 0 10px;">Credly</a>
    </div>
</div>
""", unsafe_allow_html=True)

