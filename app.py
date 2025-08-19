import streamlit as st
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Alisher Beisembekov | Polymath",
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
            <a href="#" style="color: rgba(255, 255, 255, 0.7); text-decoration: none;">📧</a>
            <a href="#" style="color: rgba(255, 255, 255, 0.7); text-decoration: none;">💼</a>
            <a href="#" style="color: rgba(255, 255, 255, 0.7); text-decoration: none;">🐦</a>
            <a href="#" style="color: rgba(255, 255, 255, 0.7); text-decoration: none;">📷</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Page content based on selection
if st.session_state.current_page == 'home':
    # Hero Section
    st.markdown('<h1 class="hero-name floating">Alisher Beisembekov</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-title">Polymath • Innovator • Visionary</p>', unsafe_allow_html=True)
    
    # Quick Stats
    st.markdown("---")
    cols = st.columns(4)
    metrics = [
        ("Patents", "12+", "📋"),
        ("Publications", "28+", "📚"),
        ("Projects", "45+", "💡"),
        ("Awards", "23+", "🏆")
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
        Pioneering the intersection of technology, science, and human potential. 
        Building the future through innovation, leadership, and relentless pursuit of excellence.
        </p>
        """, unsafe_allow_html=True)
        
        # Current Positions
        st.markdown('<h3 class="text-gradient" style="margin-top: 30px;">Current Positions</h3>', unsafe_allow_html=True)
        
        positions = [
            {
                "title": "Founder & CEO",
                "company": "TechVision AI",
                "period": "2022 - Present",
                "description": "Leading AI innovation in computer vision and machine learning applications"
            },
            {
                "title": "Chief Technology Officer",
                "company": "Innovation Labs",
                "period": "2021 - Present",
                "description": "Driving technological advancement and R&D initiatives across multiple domains"
            },
            {
                "title": "Research Scientist",
                "company": "Quantum Computing Institute",
                "period": "2020 - Present",
                "description": "Pioneering quantum algorithms for complex optimization problems"
            }
        ]
        
        for position in positions:
            st.markdown(f"""
            <div class="achievement-card">
                <h4 class="text-white">{position["title"]}</h4>
                <p class="text-gradient" style="font-weight: 600;">{position["company"]}</p>
                <p class="text-muted">{position["period"]}</p>
                <p class="text-white" style="margin-top: 10px;">{position["description"]}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        # Core Expertise
        st.markdown('<h3 class="text-gradient">Core Expertise</h3>', unsafe_allow_html=True)
        
        expertise = {
            "Technology": ["AI/ML", "Quantum", "Blockchain"],
            "Leadership": ["Strategy", "Innovation", "Mentorship"],
            "Research": ["Publications", "Patents", "Speaking"]
        }
        
        for category, skills in expertise.items():
            st.markdown(f'<p class="text-white" style="font-weight: 600; margin-top: 20px;">{category}</p>', unsafe_allow_html=True)
            for skill in skills:
                st.markdown(f'<div class="skill-tag">{skill}</div>', unsafe_allow_html=True)
        
        # Languages
        st.markdown('<h3 class="text-gradient" style="margin-top: 30px;">Languages</h3>', unsafe_allow_html=True)
        languages = ["English", "Russian", "Kazakh", "Turkish", "Spanish"]
        for lang in languages:
            st.markdown(f'<div class="skill-tag" style="margin: 5px 0;">{lang}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_page == 'career':
    st.markdown('<h1 class="hero-name">Career Journey</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-title">Professional Evolution</p>', unsafe_allow_html=True)
    
    positions = [
        {
            "title": "Founder & CEO",
            "company": "TechVision AI",
            "period": "2022 - Present",
            "description": "Leading AI innovation in computer vision and machine learning",
            "achievements": ["Raised $5M funding", "Built team of 25+", "3 patents filed"]
        },
        {
            "title": "Chief Technology Officer",
            "company": "Innovation Labs",
            "period": "2021 - Present",
            "description": "Driving technological advancement and R&D initiatives",
            "achievements": ["Led 10+ projects", "Published 5 papers", "Managed 50+ engineers"]
        },
        {
            "title": "Research Scientist",
            "company": "Quantum Computing Institute",
            "period": "2020 - Present",
            "description": "Pioneering quantum algorithms for optimization problems",
            "achievements": ["2 breakthrough algorithms", "International recognition", "Key speaker at QC Summit"]
        },
        {
            "title": "Senior Software Architect",
            "company": "Global Tech Solutions",
            "period": "2019 - 2021",
            "description": "Architected scalable cloud solutions for enterprise clients",
            "achievements": ["Designed systems for 1M+ users", "Reduced costs by 40%", "Led digital transformation"]
        },
        {
            "title": "Machine Learning Engineer",
            "company": "AI Dynamics",
            "period": "2018 - 2019",
            "description": "Developed ML models for predictive analytics",
            "achievements": ["95% accuracy models", "Automated key processes", "Saved $2M annually"]
        }
    ]
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Professional Timeline</h2>', unsafe_allow_html=True)
    
    for i, position in enumerate(positions):
        color = "#667eea" if i < 3 else "#764ba2"
        st.markdown(f'''
        <div class="achievement-card">
            <div style="display: flex; align-items: start; gap: 20px;">
                <div style="min-width: 60px; height: 60px; background: linear-gradient(135deg, {color} 0%, #764ba2 100%); 
                            border-radius: 15px; display: flex; align-items: center; justify-content: center; color: white; 
                            font-weight: bold; font-size: 1.5rem;">
                    {i+1}
                </div>
                <div style="flex: 1;">
                    <h3 class="text-white">{position["title"]}</h3>
                    <p class="text-gradient" style="font-weight: 600; font-size: 1.1rem;">{position["company"]}</p>
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
        ("Teams Led", "150+", "👥"),
        ("Projects Delivered", "45+", "🚀"),
        ("Revenue Generated", "$50M+", "💰")
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
            "area": "Artificial Intelligence",
            "icon": "🧠",
            "focus": "Deep Learning, Computer Vision, Natural Language Processing",
            "papers": 12,
            "citations": 450
        },
        {
            "area": "Quantum Computing",
            "icon": "⚛️",
            "focus": "Quantum Algorithms, Optimization, Cryptography",
            "papers": 8,
            "citations": 220
        },
        {
            "area": "Blockchain Technology",
            "icon": "🔗",
            "focus": "Smart Contracts, DeFi Protocols, Consensus Mechanisms",
            "papers": 5,
            "citations": 180
        },
        {
            "area": "Biotechnology",
            "icon": "🧬",
            "focus": "Computational Biology, Drug Discovery, Genomics",
            "papers": 3,
            "citations": 95
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
                            <p class="metric-number" style="font-size: 1.8rem;">{area["citations"]}</p>
                            <p class="text-muted">Citations</p>
                        </div>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Publications
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Selected Publications</h2>', unsafe_allow_html=True)
    
    publications = [
        {
            "title": "Quantum-Enhanced Machine Learning for Complex Optimization",
            "journal": "Nature Quantum Information",
            "year": 2024,
            "citations": 127,
            "impact": 12.5
        },
        {
            "title": "Self-Supervised Vision Transformers for Medical Image Analysis",
            "journal": "Medical Image Analysis",
            "year": 2023,
            "citations": 89,
            "impact": 10.2
        },
        {
            "title": "Decentralized Consensus Mechanisms in Blockchain Networks",
            "journal": "IEEE Transactions on Network Science",
            "year": 2023,
            "citations": 65,
            "impact": 8.7
        }
    ]
    
    for pub in publications:
        st.markdown(f'''
        <div class="achievement-card">
            <h3 class="text-white">{pub["title"]}</h3>
            <p class="text-gradient" style="font-weight: 600; margin: 10px 0;">{pub["journal"]} • {pub["year"]}</p>
            <div style="display: flex; gap: 30px; margin-top: 15px;">
                <span class="text-white">📚 Citations: <strong>{pub["citations"]}</strong></span>
                <span class="text-white">📊 Impact Factor: <strong>{pub["impact"]}</strong></span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_page == 'projects':
    st.markdown('<h1 class="hero-name">Innovation Portfolio</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-title">Building Tomorrow\'s Technology</p>', unsafe_allow_html=True)
    
    # Projects
    projects = [
        {
            "name": "Neural Vision Pro",
            "category": "AI/Computer Vision",
            "status": "Production",
            "description": "Advanced medical imaging AI that detects diseases with 98% accuracy",
            "tech": ["PyTorch", "CUDA", "OpenCV", "Docker"],
            "metrics": {"Users": "10K+", "Accuracy": "98%", "Processing": "Real-time"},
            "color": "#00ff88"
        },
        {
            "name": "Quantum Optimizer Suite",
            "category": "Quantum Computing",
            "status": "Beta",
            "description": "Quantum algorithms solving NP-hard problems 1000x faster",
            "tech": ["Qiskit", "Python", "C++", "CUDA"],
            "metrics": {"Speed": "1000x", "Problems": "50+", "Accuracy": "99.9%"},
            "color": "#ffa500"
        },
        {
            "name": "DeFi Protocol Alpha",
            "category": "Blockchain",
            "status": "Launched",
            "description": "Decentralized finance protocol with $10M+ total value locked",
            "tech": ["Solidity", "Web3.js", "React", "Hardhat"],
            "metrics": {"TVL": "$10M+", "Users": "5K+", "APY": "12%"},
            "color": "#00bfff"
        },
        {
            "name": "BioML Discovery",
            "category": "Biotechnology",
            "status": "Research",
            "description": "ML platform for drug discovery reducing development time by 60%",
            "tech": ["TensorFlow", "RDKit", "PyMOL", "AWS"],
            "metrics": {"Compounds": "1M+", "Time Saved": "60%", "Success Rate": "3x"},
            "color": "#ff69b4"
        },
        {
            "name": "AutoScale Cloud",
            "category": "Infrastructure",
            "status": "Production",
            "description": "Intelligent cloud infrastructure that auto-scales based on ML predictions",
            "tech": ["Kubernetes", "Terraform", "Go", "Prometheus"],
            "metrics": {"Cost Saved": "40%", "Uptime": "99.99%", "Response": "<100ms"},
            "color": "#00ff88"
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
        ("Code Commits", "10K+", "💻"),
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
    st.markdown('<p class="hero-title">Excellence Across Disciplines</p>', unsafe_allow_html=True)
    
    # Awards
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Major Awards</h2>', unsafe_allow_html=True)
    
    awards = [
        {
            "title": "AI Innovation Award",
            "org": "World Technology Summit",
            "year": 2024,
            "category": "Technology",
            "description": "Recognized for breakthrough in neural architecture search"
        },
        {
            "title": "Forbes 30 Under 30",
            "org": "Forbes",
            "year": 2023,
            "category": "Technology & Innovation",
            "description": "Featured as one of the most promising young innovators"
        },
        {
            "title": "Best Research Paper Award",
            "org": "International Conference on AI",
            "year": 2023,
            "category": "Research",
            "description": "Novel approach to reinforcement learning in quantum systems"
        },
        {
            "title": "Startup of the Year",
            "org": "TechCrunch",
            "year": 2023,
            "category": "Entrepreneurship",
            "description": "TechVision AI recognized for innovation in computer vision"
        },
        {
            "title": "National Science Medal",
            "org": "National Academy of Sciences",
            "year": 2022,
            "category": "Science",
            "description": "Contributions to quantum computing research"
        }
    ]
    
    for award in awards:
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
    
    # Other Achievements
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Additional Recognition</h2>', unsafe_allow_html=True)
    
    cols = st.columns(2)
    
    categories = [
        {
            "title": "Patents",
            "icon": "📋",
            "items": [
                "Quantum ML Algorithm (US Patent #12345)",
                "Computer Vision System (Patent Pending)",
                "Blockchain Consensus Method (EU Patent)",
                "Medical AI Diagnostic Tool (Patent Filed)"
            ]
        },
        {
            "title": "Speaking Engagements",
            "icon": "🎤",
            "items": [
                "Keynote at World AI Summit 2024",
                "TEDx Talk: 'Future of Quantum Computing'",
                "Google I/O Developer Conference",
                "MIT Technology Review Conference"
            ]
        },
        {
            "title": "Media Features",
            "icon": "📰",
            "items": [
                "Featured in TechCrunch",
                "Interview on Bloomberg Technology",
                "Profile in Wired Magazine",
                "Documentary: 'Next Gen Innovators'"
            ]
        },
        {
            "title": "Sports Achievements",
            "icon": "🥇",
            "items": [
                "National Chess Champion 2023",
                "Marathon Personal Best: 2:45:30",
                "Black Belt in Taekwondo",
                "University Swimming Team Captain"
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

elif st.session_state.current_page == 'analytics':
    st.markdown('<h1 class="hero-name">Performance Analytics</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-title">Data-Driven Success Metrics</p>', unsafe_allow_html=True)
    
    # Overall Statistics
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Lifetime Statistics</h2>', unsafe_allow_html=True)
    
    cols = st.columns(4)
    stats = [
        ("Patents Filed", "12", "📋", "+3 this year"),
        ("Research Papers", "28", "📚", "+7 this year"),
        ("Projects Completed", "45", "💡", "+12 this year"),
        ("Awards Won", "23", "🏆", "+5 this year"),
        ("Companies Founded", "3", "🏢", "+1 this year"),
        ("Team Members", "150+", "👥", "+50 this year"),
        ("Conference Talks", "32", "🎤", "+8 this year"),
        ("Students Mentored", "75", "🎓", "+20 this year")
    ]
    
    for i, (label, value, icon, growth) in enumerate(stats):
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
    
    # Create sample data for visualization
    years = [2019, 2020, 2021, 2022, 2023, 2024]
    projects = [5, 12, 20, 28, 38, 45]
    publications = [2, 5, 10, 15, 22, 28]
    team_size = [5, 15, 35, 60, 100, 150]
    
    # Create plotly chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=years, y=projects,
        name='Projects',
        line=dict(color='#667eea', width=3),
        marker=dict(size=10)
    ))
    
    fig.add_trace(go.Scatter(
        x=years, y=publications,
        name='Publications',
        line=dict(color='#764ba2', width=3),
        marker=dict(size=10)
    ))
    
    fig.add_trace(go.Scatter(
        x=years, y=team_size,
        name='Team Size',
        line=dict(color='#f093fb', width=3),
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
    st.markdown('<h2 class="section-header">Skills Distribution</h2>', unsafe_allow_html=True)
    
    skills_data = pd.DataFrame({
        'Skill': ['AI/ML', 'Cloud', 'Blockchain', 'Quantum', 'Leadership', 'Research'],
        'Level': [95, 90, 85, 80, 92, 88]
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

# Footer
st.markdown("""
<div style="margin-top: 60px; padding: 30px 0; text-align: center; border-top: 1px solid rgba(255,255,255,0.1);">
    <p class="text-muted">© 2024 Alisher Beisembekov. Crafting the future, one innovation at a time.</p>
</div>
""", unsafe_allow_html=True)
