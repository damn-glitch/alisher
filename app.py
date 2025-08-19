import streamlit as st
from datetime import datetime
import json
import base64

# Page Configuration
st.set_page_config(
    page_title="Alisher Beisembekov | Polymath",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Advanced Post-Modern CSS Design
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
    header {visibility: hidden;}
    
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
    
    /* Navigation Pills */
    .nav-container {
        display: flex;
        justify-content: center;
        gap: 15px;
        flex-wrap: wrap;
        margin: 40px 0;
        padding: 20px;
    }
    
    .nav-pill {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: rgba(255, 255, 255, 0.9);
        padding: 12px 25px;
        border-radius: 50px;
        font-weight: 500;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        text-decoration: none;
        display: inline-block;
    }
    
    .nav-pill:hover {
        background: rgba(255, 255, 255, 0.15);
        transform: translateY(-2px) scale(1.05);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .nav-pill.active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: 1px solid transparent;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
    }
    
    /* Metric Cards */
    .metric-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin: 30px 0;
    }
    
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
    
    /* Timeline */
    .timeline {
        position: relative;
        padding: 20px 0;
    }
    
    .timeline:before {
        content: '';
        position: absolute;
        left: 50%;
        top: 0;
        bottom: 0;
        width: 2px;
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        transform: translateX(-50%);
    }
    
    .timeline-item {
        position: relative;
        margin: 30px 0;
        display: flex;
        align-items: center;
    }
    
    .timeline-item:nth-child(odd) {
        flex-direction: row-reverse;
    }
    
    .timeline-content {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 20px;
        width: 45%;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .timeline-content:hover {
        transform: scale(1.05);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .timeline-dot {
        position: absolute;
        left: 50%;
        transform: translateX(-50%);
        width: 20px;
        height: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 50%;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.5);
    }
    
    /* Skills Grid */
    .skills-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 15px;
        margin: 20px 0;
    }
    
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
    
    /* Responsive */
    @media (max-width: 768px) {
        .timeline:before {
            left: 30px;
        }
        
        .timeline-content {
            width: calc(100% - 60px);
            margin-left: 60px;
        }
        
        .timeline-item:nth-child(odd) {
            flex-direction: row;
        }
        
        .timeline-dot {
            left: 30px;
        }
    }
</style>

<div class="animated-bg"></div>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# Data Structure
data = {
    "personal": {
        "name": "Alisher Beisembekov",
        "title": "Polymath • Innovator • Visionary",
        "tagline": "CEO | Scientist | Developer | Athlete",
        "bio": """
        Pioneering the intersection of technology, science, and human potential. 
        Building the future through innovation, leadership, and relentless pursuit of excellence.
        """,
        "location": "Global",
        "email": "contact@example.com",
        "languages": ["English", "Russian", "Kazakh", "Turkish", "Spanish"],
        "social": {
            "linkedin": "#",
            "github": "#",
            "twitter": "#",
            "instagram": "#"
        }
    },
    
    "positions": [
        {
            "title": "Founder & CEO",
            "company": "TechVision AI",
            "period": "2022 - Present",
            "description": "Leading AI innovation in computer vision and machine learning",
            "type": "current"
        },
        {
            "title": "Chief Technology Officer",
            "company": "Innovation Labs",
            "period": "2021 - Present",
            "description": "Driving technological advancement and R&D initiatives",
            "type": "current"
        },
        {
            "title": "Research Scientist",
            "company": "Quantum Computing Institute",
            "period": "2020 - Present",
            "description": "Pioneering quantum algorithms for optimization problems",
            "type": "current"
        },
        {
            "title": "Senior Software Architect",
            "company": "Global Tech Solutions",
            "period": "2019 - 2021",
            "description": "Architected scalable cloud solutions for enterprise clients",
            "type": "past"
        }
    ],
    
    "stats": {
        "patents": 12,
        "publications": 28,
        "projects": 45,
        "awards": 23,
        "companies": 3,
        "medals": 15,
        "talks": 32,
        "students": 150
    },
    
    "skills": {
        "Programming": ["Python", "JavaScript", "C++", "Rust", "Go", "TypeScript"],
        "AI/ML": ["TensorFlow", "PyTorch", "Computer Vision", "NLP", "Deep Learning"],
        "Cloud": ["AWS", "GCP", "Azure", "Kubernetes", "Docker"],
        "Blockchain": ["Ethereum", "Smart Contracts", "Web3", "DeFi"],
        "Leadership": ["Strategy", "Team Building", "Public Speaking", "Mentorship"]
    },
    
    "achievements": [
        {
            "title": "AI Innovation Award",
            "organization": "Tech Summit 2024",
            "year": 2024,
            "description": "Recognized for breakthrough in neural architecture"
        },
        {
            "title": "Forbes 30 Under 30",
            "organization": "Forbes",
            "year": 2023,
            "description": "Featured in Technology category"
        },
        {
            "title": "Best Research Paper",
            "organization": "International Conference on AI",
            "year": 2023,
            "description": "Novel approach to reinforcement learning"
        }
    ],
    
    "projects": [
        {
            "name": "Neural Vision Pro",
            "type": "AI/Computer Vision",
            "status": "Active",
            "description": "Advanced computer vision system for medical diagnostics",
            "tech": ["PyTorch", "OpenCV", "CUDA"],
            "link": "#"
        },
        {
            "name": "Quantum Optimizer",
            "type": "Quantum Computing",
            "status": "Research",
            "description": "Quantum algorithms for NP-hard optimization problems",
            "tech": ["Qiskit", "Python", "Mathematics"],
            "link": "#"
        },
        {
            "name": "DeFi Protocol",
            "type": "Blockchain",
            "status": "Launched",
            "description": "Decentralized finance protocol with $10M TVL",
            "tech": ["Solidity", "Web3.js", "React"],
            "link": "#"
        }
    ]
}

# Navigation Function
def navigate_to(page):
    st.session_state.current_page = page

# Hero Section
st.markdown(f'<h1 class="hero-name floating">{data["personal"]["name"]}</h1>', unsafe_allow_html=True)
st.markdown(f'<p class="hero-title">{data["personal"]["title"]}</p>', unsafe_allow_html=True)

# Navigation Pills
nav_items = [
    ("🏠 Home", "home"),
    ("💼 Career", "career"),
    ("🔬 Research", "research"),
    ("💻 Projects", "projects"),
    ("🏆 Achievements", "achievements"),
    ("📊 Analytics", "analytics")
]

nav_html = '<div class="nav-container">'
for label, page in nav_items:
    active_class = "active" if st.session_state.current_page == page else ""
    nav_html += f'<span class="nav-pill {active_class}" onclick="navigate(\'{page}\')">{label}</span>'
nav_html += '</div>'

st.markdown(nav_html, unsafe_allow_html=True)

# Quick Stats Bar
st.markdown('<div class="metric-container">', unsafe_allow_html=True)
cols = st.columns(4)
metrics = [
    ("Patents", data["stats"]["patents"], "📋"),
    ("Publications", data["stats"]["publications"], "📚"),
    ("Projects", data["stats"]["projects"], "💡"),
    ("Awards", data["stats"]["awards"], "🏆")
]

for col, (label, value, icon) in zip(cols, metrics):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 2rem; margin-bottom: 10px;">{icon}</div>
            <div class="metric-number">{value}+</div>
            <div class="metric-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Main Content Area
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

if st.session_state.current_page == "home":
    # Bio Section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<h2 class="section-header">Redefining Possibilities</h2>', unsafe_allow_html=True)
        st.markdown(f'<p class="text-white" style="font-size: 1.1rem; line-height: 1.8;">{data["personal"]["bio"]}</p>', unsafe_allow_html=True)
        
        # Current Positions
        st.markdown('<h3 class="text-gradient" style="margin-top: 30px;">Current Positions</h3>', unsafe_allow_html=True)
        for position in [p for p in data["positions"] if p["type"] == "current"]:
            st.markdown(f"""
            <div class="achievement-card">
                <h4 class="text-white">{position["title"]}</h4>
                <p class="text-gradient" style="font-weight: 600;">{position["company"]}</p>
                <p class="text-muted">{position["period"]}</p>
                <p class="text-white" style="margin-top: 10px;">{position["description"]}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        # Skills Cloud
        st.markdown('<h3 class="text-gradient">Expertise</h3>', unsafe_allow_html=True)
        for category, skills in data["skills"].items():
            st.markdown(f'<p class="text-white" style="font-weight: 600; margin-top: 20px;">{category}</p>', unsafe_allow_html=True)
            st.markdown('<div class="skills-grid">', unsafe_allow_html=True)
            for skill in skills[:3]:  # Show top 3 skills per category
                st.markdown(f'<span class="skill-tag">{skill}</span>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Languages
        st.markdown('<h3 class="text-gradient" style="margin-top: 30px;">Languages</h3>', unsafe_allow_html=True)
        for lang in data["personal"]["languages"]:
            st.markdown(f'<div class="skill-tag" style="margin: 5px 0;">{lang}</div>', unsafe_allow_html=True)

elif st.session_state.current_page == "career":
    st.markdown('<h2 class="section-header">Career Journey</h2>', unsafe_allow_html=True)
    
    # Timeline View
    st.markdown('<div class="timeline">', unsafe_allow_html=True)
    
    for i, position in enumerate(data["positions"]):
        alignment = "left" if i % 2 == 0 else "right"
        st.markdown(f"""
        <div class="timeline-item">
            <div class="timeline-dot"></div>
            <div class="timeline-content">
                <h3 class="text-gradient">{position["title"]}</h3>
                <h4 class="text-white">{position["company"]}</h4>
                <p class="text-muted">{position["period"]}</p>
                <p class="text-white">{position["description"]}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Additional Stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-card glow">
            <div class="metric-number">3</div>
            <div class="metric-label">Companies Founded</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card glow">
            <div class="metric-number">150+</div>
            <div class="metric-label">Team Members Led</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card glow">
            <div class="metric-number">$50M+</div>
            <div class="metric-label">Revenue Generated</div>
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.current_page == "research":
    st.markdown('<h2 class="section-header">Research & Innovation</h2>', unsafe_allow_html=True)
    
    # Research Areas
    research_areas = [
        ("Artificial Intelligence", "Deep learning, Computer vision, NLP", "🧠"),
        ("Quantum Computing", "Quantum algorithms, Optimization", "⚛️"),
        ("Blockchain", "DeFi protocols, Smart contracts", "🔗"),
        ("Biotechnology", "Computational biology, Drug discovery", "🧬")
    ]
    
    cols = st.columns(2)
    for i, (area, desc, icon) in enumerate(research_areas):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="achievement-card">
                <div style="font-size: 3rem; text-align: center; margin-bottom: 15px;">{icon}</div>
                <h3 class="text-gradient" style="text-align: center;">{area}</h3>
                <p class="text-white" style="text-align: center;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Publications Highlight
    st.markdown('<h3 class="text-gradient" style="margin-top: 40px;">Featured Publications</h3>', unsafe_allow_html=True)
    st.markdown("""
    <div class="glass-card">
        <p class="text-muted">PUBLICATION HIGHLIGHTS</p>
        <h4 class="text-white">28 peer-reviewed papers</h4>
        <p class="text-white">500+ citations | h-index: 12</p>
        <p class="text-gradient" style="margin-top: 15px;">Top venues: NeurIPS, ICML, Nature Communications</p>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.current_page == "projects":
    st.markdown('<h2 class="section-header">Innovation Portfolio</h2>', unsafe_allow_html=True)
    
    for project in data["projects"]:
        status_color = "#00ff88" if project["status"] == "Active" else "#ffa500" if project["status"] == "Research" else "#00bfff"
        st.markdown(f"""
        <div class="achievement-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h3 class="text-white">{project["name"]}</h3>
                <span style="background: {status_color}; color: #000; padding: 5px 15px; border-radius: 20px; font-weight: 600; font-size: 0.9rem;">
                    {project["status"]}
                </span>
            </div>
            <p class="text-gradient" style="font-weight: 600; margin: 10px 0;">{project["type"]}</p>
            <p class="text-white">{project["description"]}</p>
            <div style="margin-top: 15px;">
                {"".join([f'<span class="skill-tag" style="display: inline-block; margin: 5px;">{tech}</span>' for tech in project["tech"]])}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Project Stats
    st.markdown('<h3 class="text-gradient" style="margin-top: 40px;">Impact Metrics</h3>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">45+</div>
            <div class="metric-label">Projects Completed</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">1M+</div>
            <div class="metric-label">Users Impacted</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">12</div>
            <div class="metric-label">Patents Filed</div>
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.current_page == "achievements":
    st.markdown('<h2 class="section-header">Recognition & Awards</h2>', unsafe_allow_html=True)
    
    for achievement in data["achievements"]:
        st.markdown(f"""
        <div class="achievement-card">
            <div style="display: flex; align-items: center; margin-bottom: 15px;">
                <div style="font-size: 2rem; margin-right: 15px;">🏆</div>
                <div>
                    <h3 class="text-white" style="margin: 0;">{achievement["title"]}</h3>
                    <p class="text-gradient" style="margin: 5px 0; font-weight: 600;">{achievement["organization"]} • {achievement["year"]}</p>
                </div>
            </div>
            <p class="text-white">{achievement["description"]}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Additional Recognition
    st.markdown('<h3 class="text-gradient" style="margin-top: 40px;">Additional Recognition</h3>', unsafe_allow_html=True)
    
    recognitions = [
        ("Speaking Engagements", "32", "International conferences and summits"),
        ("Media Features", "45", "Major publications and interviews"),
        ("Sports Achievements", "15", "National and international competitions"),
        ("Academic Honors", "8", "Scholarships and academic awards")
    ]
    
    cols = st.columns(2)
    for i, (title, count, desc) in enumerate(recognitions):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="glass-card">
                <h4 class="text-gradient">{title}</h4>
                <p style="font-size: 2rem; font-weight: 700; color: white; margin: 10px 0;">{count}</p>
                <p class="text-muted">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

elif st.session_state.current_page == "analytics":
    st.markdown('<h2 class="section-header">Performance Analytics</h2>', unsafe_allow_html=True)
    
    # Career Growth Chart (Placeholder)
    st.markdown("""
    <div class="glass-card" style="height: 300px; display: flex; align-items: center; justify-content: center;">
        <div style="text-align: center;">
            <div style="font-size: 4rem; margin-bottom: 20px;">📈</div>
            <h3 class="text-gradient">Career Growth Trajectory</h3>
            <p class="text-white">Interactive charts will be displayed here</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Comprehensive Stats
    st.markdown('<h3 class="text-gradient" style="margin-top: 40px;">Lifetime Statistics</h3>', unsafe_allow_html=True)
    
    all_stats = [
        ("Patents Filed", data["stats"]["patents"], "📋"),
        ("Research Papers", data["stats"]["publications"], "📚"),
        ("Projects Completed", data["stats"]["projects"], "💡"),
        ("Awards Won", data["stats"]["awards"], "🏆"),
        ("Companies Founded", data["stats"]["companies"], "🏢"),
        ("Sports Medals", data["stats"]["medals"], "🥇"),
        ("Conference Talks", data["stats"]["talks"], "🎤"),
        ("Students Mentored", data["stats"]["students"], "👥")
    ]
    
    cols = st.columns(4)
    for i, (label, value, icon) in enumerate(all_stats):
        with cols[i % 4]:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 2rem; margin-bottom: 10px;">{icon}</div>
                <div class="metric-number">{value}+</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="margin-top: 60px; padding: 30px 0; text-align: center; border-top: 1px solid rgba(255,255,255,0.1);">
    <p class="text-muted">© 2024 Alisher Beisembekov. Crafting the future, one innovation at a time.</p>
    <div style="margin-top: 20px;">
        <a href="#" class="nav-pill" style="margin: 0 10px;">LinkedIn</a>
        <a href="#" class="nav-pill" style="margin: 0 10px;">GitHub</a>
        <a href="#" class="nav-pill" style="margin: 0 10px;">Twitter</a>
        <a href="#" class="nav-pill" style="margin: 0 10px;">Email</a>
    </div>
</div>
""", unsafe_allow_html=True)

# JavaScript for navigation (this won't work in Streamlit, but shows intent)
st.markdown("""
<script>
function navigate(page) {
    // In a real implementation, this would handle navigation
    console.log('Navigating to:', page);
}
</script>
""", unsafe_allow_html=True)
