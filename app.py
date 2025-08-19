import streamlit as st
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from collections import Counter, defaultdict

# =========================
# Page Configuration
# =========================
st.set_page_config(
    page_title="Alisher Beisembekov | Portfolio",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# App State
# =========================
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# =========================
# Advanced Post-Modern CSS
# =========================
def load_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        * { font-family: 'Inter', sans-serif; }
        .stApp { background: linear-gradient(135deg, #0F0C29 0%, #302B63 50%, #24243e 100%); background-attachment: fixed; }
        #MainMenu{visibility:hidden;} footer{visibility:hidden;}

        section[data-testid="stSidebar"]{background:rgba(15,12,41,0.8); backdrop-filter:blur(20px); border-right:1px solid rgba(255,255,255,0.1);}
        section[data-testid="stSidebar"] .stButton>button{
            background:rgba(255,255,255,0.05); color:rgba(255,255,255,0.9);
            border:1px solid rgba(255,255,255,0.1); border-radius:15px; padding:15px; width:100%;
            transition:all .3s ease; font-weight:500; margin-bottom:10px;
        }
        section[data-testid="stSidebar"] .stButton>button:hover{
            background:linear-gradient(135deg, rgba(102,126,234,.3) 0%, rgba(118,75,162,.3) 100%);
            border:1px solid rgba(255,255,255,.3); transform:translateX(5px);
            box-shadow:0 5px 15px rgba(102,126,234,.3);
        }

        .animated-bg{position:fixed;width:100%;height:100%;top:0;left:0;z-index:-1;
            background:linear-gradient(270deg,#0F0C29,#302B63,#24243e,#0F0C29); background-size:800% 800%;
            animation:gradientShift 20s ease infinite;}
        @keyframes gradientShift{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}

        .glass-card{background:rgba(255,255,255,0.05); backdrop-filter:blur(10px);
            border-radius:20px; border:1px solid rgba(255,255,255,0.1); padding:30px; margin:20px 0;
            box-shadow:0 8px 32px 0 rgba(31,38,135,0.37); transition:all .3s ease;}
        .glass-card:hover{transform:translateY(-5px); box-shadow:0 15px 35px rgba(31,38,135,0.5); border:1px solid rgba(255,255,255,0.2);}

        .hero-name{font-family:'Space Grotesk',sans-serif; font-size:clamp(3rem,8vw,6rem); font-weight:700;
            background:linear-gradient(135deg,#667eea 0%,#764ba2 20%,#f093fb 40%,#f5576c 60%,#fda085 80%,#667eea 100%);
            background-size:200% 200%; -webkit-background-clip:text; -webkit-text-fill-color:transparent;
            text-align:center; animation:gradientText 5s ease infinite; letter-spacing:-.02em; line-height:1.1; margin-bottom:0;}
        @keyframes gradientText{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
        .hero-title{font-family:'Space Grotesk',sans-serif; font-size:clamp(1.2rem,3vw,1.8rem); color:rgba(255,255,255,.9); text-align:center; margin-top:10px; letter-spacing:.2em; text-transform:uppercase; font-weight:300;}
        .metric-card{background:linear-gradient(135deg,rgba(255,255,255,.1) 0%,rgba(255,255,255,.05) 100%); backdrop-filter:blur(10px);
            border-radius:16px; padding:25px; text-align:center; border:1px solid rgba(255,255,255,.1); transition:all .3s ease;}
        .metric-card:hover{transform:translateY(-5px) scale(1.02); border:1px solid rgba(255,255,255,.3); box-shadow:0 10px 30px rgba(0,0,0,.3);}
        .metric-number{font-size:2.5rem; font-weight:700; background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);
            -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin-bottom:5px;}
        .metric-label{color:rgba(255,255,255,.7); font-size:.9rem; text-transform:uppercase; letter-spacing:.1em;}
        .section-header{font-family:'Space Grotesk',sans-serif; font-size:clamp(2rem,4vw,3rem); font-weight:600;
            background:linear-gradient(135deg,#fff 0%,rgba(255,255,255,.7) 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent;
            margin:40px 0 30px 0; position:relative; padding-bottom:15px;}
        .section-header:after{content:''; position:absolute; bottom:0; left:0; width:100px; height:3px;
            background:linear-gradient(90deg,#667eea 0%,#764ba2 100%); border-radius:2px;}
        .achievement-card{background:rgba(255,255,255,.03); backdrop-filter:blur(10px); border-radius:16px; padding:25px; margin-bottom:20px;
            border:1px solid rgba(255,255,255,.1); transition:all .3s ease; position:relative; overflow:hidden;}
        .achievement-card:before{content:''; position:absolute; top:0; left:-100%; width:100%; height:100%;
            background:linear-gradient(90deg,transparent,rgba(255,255,255,.1),transparent); transition:left .5s ease;}
        .achievement-card:hover:before{left:100%}
        .achievement-card:hover{transform:translateX(5px); border:1px solid rgba(255,255,255,.2); box-shadow:0 5px 20px rgba(0,0,0,.3);}
        .skill-tag{background:rgba(255,255,255,.05); backdrop-filter:blur(10px); border:1px solid rgba(255,255,255,.1); color:rgba(255,255,255,.9);
            padding:12px 20px; border-radius:25px; font-weight:500; transition:all .3s ease; display:inline-block; margin:5px;}
        .skill-tag:hover{background:linear-gradient(135deg,rgba(102,126,234,.2) 0%,rgba(118,75,162,.2) 100%); transform:translateY(-3px);
            box-shadow:0 5px 15px rgba(0,0,0,.3); border:1px solid rgba(255,255,255,.3);}
        .floating{animation:float 6s ease-in-out infinite;} @keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-20px)}}
        .glow{box-shadow:0 0 30px rgba(102,126,234,.6), 0 0 60px rgba(102,126,234,.4), 0 0 90px rgba(102,126,234,.2);}
        ::-webkit-scrollbar{width:10px;} ::-webkit-scrollbar-track{background:rgba(255,255,255,.05);}
        ::-webkit-scrollbar-thumb{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%); border-radius:5px;}
        ::-webkit-scrollbar-thumb:hover{background:linear-gradient(135deg,#764ba2 0%,#667eea 100%);}
        .text-gradient{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent;}
        .text-white{color:rgba(255,255,255,.9);} .text-muted{color:rgba(255,255,255,.6);}
        .sidebar-header{color:white; text-align:center; padding:20px 0; border-bottom:1px solid rgba(255,255,255,.1); margin-bottom:20px;}
        .sidebar-name{font-family:'Space Grotesk',sans-serif; font-size:1.5rem; font-weight:600;
            background:linear-gradient(135deg,#667eea 0%,#764ba2 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin-bottom:5px;}
        .sidebar-title{color:rgba(255,255,255,.7); font-size:.9rem; letter-spacing:.1em;}
    </style>
    <div class="animated-bg"></div>
    """, unsafe_allow_html=True)

load_css()

# =========================
# DATA from All info alish.pdf (hardcoded)
# =========================
PROFILE = {
    "name": "Alisher Beisembekov",
    "tagline": "AI/ML Founder • Multi‑patented Inventor • Builder",
    "summary": (
        "Founder & CEO of Infinitum Intelligence, co‑founder of Carso (AI автозапчасти). "
        "Автор патентов в ИИ/телеком/хелс‑тех и блокчейне. Лауреат IAAC/IYMC, "
        "AIM (FIDE), Undergrad Research Scholar RIT Dubai."
    ),
    "languages": ["English", "Русский", "Қазақ тілі"],
    "links": {
        "Email": "#",
        "LinkedIn": "#",
        "GitHub": "#",
        "Telegram": "#"
    }
}

EXPERIENCE = [
    {
        "title": "Co‑Founder",
        "company": "Carso (AI‑Powered Auto Parts Trading Platform)",
        "period": "May 2025 – Present",
        "location": "Kazakhstan",
        "bullets": [
            "Со‑создатель и автор патента KZ 58713: AI‑маркетплейс автозапчастей с real‑time откликами поставщиков и интеграцией доставки.",
            "Архитектура: Python/Flask, PostgreSQL, Flask‑SocketIO; платежи (3D‑Secure, Kaspi Pay), Yandex.Delivery, админ‑аналитика."
        ],
        "stack": ["Python", "Flask", "PostgreSQL", "WebSockets", "Yandex.Delivery", "Kaspi Pay"]
    },  # Carso: filecite markers in text outside code
    {
        "title": "Founder & CEO",
        "company": "Infinitum Intelligence",
        "period": "Oct 2023 – Present",
        "location": "Global",
        "bullets": [
            "R&D продуктов XG SONIC (AI оптимизация скорости сетей 5G/6G, KZ 59121) и MedGPT/HealthHub (KZ 38024).",
            "Фокус: AI/ML, сетевые оптимизации (LSTM/CNN/DNN), edge‑инференс, healthcare‑аналитика."
        ],
        "stack": ["AI/ML", "LSTM/CNN/DNN", "Edge", "Python", "TensorFlow/PyTorch"]
    },
    {
        "title": "Project Lead / Engineer",
        "company": "Jasaim (projects)",
        "period": "Jul 2023 – Feb 2025",
        "location": "UAE/KZ",
        "bullets": [
            "eDiploma (NFT‑дипломы, смарт‑контракты, KZ 38001/KZ 37650).",
            "Agile Job Description (AI‑подбор, GitHub‑оценка кода), Meta University (VR‑образование), JasWallet, Hyperports (B/L на Hyperledger Fabric)."
        ],
        "stack": ["Blockchain", "Smart Contracts", "Hyperledger", "NLP", "VR/Unity"]
    },
    {
        "title": "Martial Arts Instructor",
        "company": "AJS Jiu Jitsu (part‑time)",
        "period": "Jul 2018 – Aug 2019",
        "location": "—",
        "bullets": ["MMA, Jiu‑Jitsu, Boxing — тренерская деятельность."],
        "stack": []
    }
]

EDUCATION = [
    {
        "school": "Rochester Institute of Technology, Dubai (RIT Dubai)",
        "degree": "BSc, Computer Science & IT — Magna Cum Laude",
        "period": "Sep 2020 – May 2024",
        "details": ["Minor: Mathematics", "Dean’s List x6", "Undergraduate Research Scholar (2024)"]
    },
    {
        "school": "The Coding School (Qubit by Qubit)",
        "degree": "Quantum Computing Program (IBM) — 101.5% / 100%",
        "period": "Sep 2020 – May 2021",
        "details": ["Квантовые алгоритмы, суперпозиция/энтангльмент, телепортация."]
    },
    {
        "school": "National School of Physics & Math (FIZMAT)",
        "degree": "High School Diploma (5.0/5)",
        "period": "Oct 2016 – May 2020",
        "details": []
    }
]

PATENTS = [
    {"title": "XG SONIC — Universal Network Speed Optimization", "no": "KZ 59121", "date": "2025-06-03",
     "area": "Telecom/AI", "summary": "66%↓ latency, 150%↑ throughput, <30s anomaly detection; LSTM/CNN/DNN."},
    {"title": "AutoTrade — Automotive Dealership Management", "no": "KZ 59905", "date": "2025-06-17",
     "area": "Auto/Analytics", "summary": "DMS: инвентарь, платежи, BI, real‑time отчёты."},
    {"title": "Carso — AI Auto Parts Trading Platform", "no": "KZ 58713", "date": "2025-05-27",
     "area": "Marketplace/AI", "summary": "AI‑поиск запчастей, WebSocket отклики, Yandex.Delivery, 3D‑Secure/Kaspi Pay."},
    {"title": "HealthHub / MedGPT / Medica", "no": "KZ 38024", "date": "2023-07-12",
     "area": "HealthTech/AI", "summary": "Непрерывный мониторинг, ДНК‑анализ, LSTM‑предикции и ранние предупреждения."},
    {"title": "GazeWriter — Eye‑Tracking Communication", "no": "KZ 38046", "date": "2023-07-15",
     "area": "CV/Assistive Tech", "summary": "Написание глазами: pupil‑tracking, виртуальная клавиатура, TTS."},
    {"title": "ShareTalk — Expert Knowledge Marketplace", "no": "KZ 41750", "date": "2023-12-01",
     "area": "Platform/Video", "summary": "Биржа консультаций: видео, биллинг/календарь, рейтинги, запись сессий."},
    {"title": "eDiploma (Generator + Smart Contract + Portal)", "no": "KZ 38001", "date": "2023-07-01",
     "area": "Blockchain/EdTech", "summary": "NFT‑дипломы, мгновенная верификация, API‑интеграция."},
    {"title": "eDiploma (second patent no.)", "no": "KZ 37650", "date": "2023-07-01",
     "area": "Blockchain/EdTech", "summary": "Технологический стек и архитектура системы NFT‑документов."}
]

PROJECTS = [
    {
        "name": "XG SONIC",
        "category": "Telecom/AI",
        "status": "Patented",
        "year": 2025,
        "description": "AI‑ядро оптимизации скорости 5G/6G/Beyond: 66%↓ latency, 150%↑ throughput; self‑learning.",
        "tech": ["AI/ML", "LSTM", "CNN", "DNN", "Edge"],
        "metrics": {"Latency": "−66%", "Throughput": "+150%", "Anomaly": "<30s"}
    },
    {
        "name": "Carso",
        "category": "Marketplace/Automotive",
        "status": "Patented",
        "year": 2025,
        "description": "Маркетплейс автозапчастей: AI‑подбор, мгновенный отклик поставщиков, доставка и платежи.",
        "tech": ["Python", "Flask", "PostgreSQL", "WebSocket"],
        "metrics": {"Sourcing time": "−70%", "Price": "−25%", "CSAT": "95%"}
    },
    {
        "name": "AutoTrade (DMS)",
        "category": "Auto/Analytics",
        "status": "Patented",
        "year": 2025,
        "description": "Управление дилершипами: инвентарь, платежи, роль‑модель, BI‑дашборды.",
        "tech": ["Python", "SQLite", "Dash/Plotly"],
        "metrics": {"Processing": "×1.5", "Accuracy": "95%", "Dealers": "33+"}
    },
    {
        "name": "HealthHub / MedGPT / Medica",
        "category": "HealthTech",
        "status": "Patented",
        "year": 2023,
        "description": "Непрерывный мониторинг + ДНК‑анализ, AI‑рекомендации и ранние предупреждения.",
        "tech": ["AI/ML", "IoT", "LSTM", "Encryption"],
        "metrics": {"Readmissions": "↓", "Insights": "continuous", "Security": "HIPAA‑style"}
    },
    {
        "name": "eDiploma",
        "category": "Blockchain/EdTech",
        "status": "Patented",
        "year": 2023,
        "description": "NFT‑дипломы на смарт‑контрактах: неизменяемость, мгновенная верификация, портал/АПИ.",
        "tech": ["Hyperledger/Smart contracts", "NFT"],
        "metrics": {"Fraud": "0", "Verification": "instant"}
    },
    {
        "name": "Hyperports — Blockchain Port Operations",
        "category": "Supply Chain",
        "status": "Production‑ready",
        "year": 2024,
        "description": "Smart B/L на Hyperledger Fabric: 60% быстрее, нулевая подделка, полный аудит.",
        "tech": ["Hyperledger Fabric", "Smart Contracts"],
        "metrics": {"B/L time": "−60%", "Paper": "0%", "Audit": "100%"}
    },
    {
        "name": "Agile Job Description",
        "category": "HR/AI",
        "status": "Beta",
        "year": 2023,
        "description": "NLP‑разбор JD, скоринг совпадения, GitHub‑оценка кода, анти‑bias‑matching.",
        "tech": ["NLP", "GitHub API", "Python"],
        "metrics": {"Screening": "−75%", "Accuracy": "90%", "Retention": "+60%"}
    },
    {
        "name": "Meta University (VR)",
        "category": "EdTech/VR",
        "status": "R&D",
        "year": 2022,
        "description": "VR‑лабы, геймификация, learn‑to‑earn токеномика; B2B интеграции и B2C‑маркетплейс.",
        "tech": ["VR/AR", "Unity", "Cloud"],
        "metrics": {"Market": "$23B", "Vision": "Meta City/University/Bank"}
    },
    {
        "name": "GazeWriter",
        "category": "Assistive Tech/CV",
        "status": "Patented",
        "year": 2023,
        "description": "Письмо глазами: pupil‑tracking, dwell/blink, виртуальная клавиатура, TTS.",
        "tech": ["OpenCV", "CV", "Python"],
        "metrics": {"Hardware": "webcam", "Mode": "hands‑free"}
    },
    {
        "name": "ShareTalk",
        "category": "Platform/Video",
        "status": "Patented",
        "year": 2023,
        "description": "Маркетплейс консультаций: профили, фильтры, видео‑созвоны, биллинг, записи.",
        "tech": ["WebRTC", "Payments", "Calendars"],
        "metrics": {"Use cases": "career, founders, students"}
    }
]

AWARDS = [
    {"title": "IAAC — Gold Honour", "org": "International Astronomy and Astrophysics Competition", "year": 2022, "notes": "Также National Award (UAE)"},
    {"title": "IAAC — Bronze Honour", "org": "International Astronomy and Astrophysics Competition", "year": 2023, "notes": ""},
    {"title": "IAAC — Silver Honour", "org": "International Astronomy and Astrophysics Competition", "year": 2024, "notes": ""},
    {"title": "IYMC — National Award", "org": "International Youth Math Challenge", "year": 2021, "notes": ""},
    {"title": "IYMC — Silver Honour", "org": "International Youth Math Challenge", "year": 2021, "notes": ""},
    {"title": "IYMC — Silver Honour", "org": "International Youth Math Challenge", "year": 2022, "notes": ""},
    {"title": "IYMC — Silver Honour", "org": "International Youth Math Challenge", "year": 2023, "notes": ""},
    {"title": "Google HashCode — Top 121/9004", "org": "Google", "year": 2021, "notes": ""},
    {"title": "Google Farewell Rounds — Top 29/81,000", "org": "Google", "year": 2023, "notes": ""},
    {"title": "ZainTECH RIT Data Challenge — 3rd Place", "org": "ZainTECH", "year": 2023, "notes": ""},
    {"title": "Microsoft Learn AI Skills Challenge — 4× winner", "org": "Microsoft", "year": 2023, "notes": "ML, MLOps, Cognitive, AI Builder"},
    {"title": "Undergraduate Research Scholar", "org": "RIT Dubai", "year": 2024, "notes": ""},
    {"title": "RIT Dubai Ambassador Award", "org": "RIT Dubai", "year": 2023, "notes": ""},
    {"title": "Future Health Hackathon 2071 — Bronze", "org": "UAE", "year": 2021, "notes": ""},
    {"title": "Project ICE24 Absolute Champions (Phase I & II)", "org": "United Nations", "year": 2024, "notes": ""},
    {"title": "Arena International Master (AIM)", "org": "FIDE", "year": 2024, "notes": "Rapid/Blitz/Bullet requirements"},
    {"title": "Payit Hackathon (Participation)", "org": "Dubai", "year": 2024, "notes": "UX редизайн и ресерч"}
]

SKILLS = {
    "AI/ML": ["TensorFlow", "PyTorch", "scikit‑learn", "NLP", "Computer Vision", "LSTM/CNN/DNN"],
    "Backend": ["Python", "Flask", "Django", "FastAPI", "PostgreSQL", "MySQL"],
    "DevOps/Cloud": ["Docker", "Kubernetes", "AWS", "Azure", "GCP", "CI/CD"],
    "Blockchain": ["Hyperledger Fabric", "Smart Contracts", "NFT", "Web3"],
    "Other": ["Edge Computing", "IoT", "OpenCV", "Git", "Data Analytics"]
}

# Quick counters
total_patents = len(PATENTS)
total_projects = len(PROJECTS)
total_awards = len(AWARDS)

# =========================
# Sidebar Navigation
# =========================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <div class="sidebar-name">Alisher Beisembekov</div>
        <div class="sidebar-title">Portfolio Navigation</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🏠 Home", use_container_width=True): st.session_state.current_page = 'home'
    if st.button("💼 Career", use_container_width=True): st.session_state.current_page = 'career'
    if st.button("🎓 Education", use_container_width=True): st.session_state.current_page = 'education'
    if st.button("💻 Projects", use_container_width=True): st.session_state.current_page = 'projects'
    if st.button("📑 Patents", use_container_width=True): st.session_state.current_page = 'patents'
    if st.button("🏆 Achievements", use_container_width=True): st.session_state.current_page = 'achievements'
    if st.button("📊 Analytics", use_container_width=True): st.session_state.current_page = 'analytics'

    st.markdown("---")
    st.markdown("""
    <div style="text-align:center; padding:20px 0;">
        <p style="color:rgba(255,255,255,.6); margin-bottom:15px;">Connect</p>
        <div style="display:flex; justify-content:center; gap:15px;">
            <a href="#" style="color:rgba(255,255,255,.7); text-decoration:none;">📧</a>
            <a href="#" style="color:rgba(255,255,255,.7); text-decoration:none;">💼</a>
            <a href="#" style="color:rgba(255,255,255,.7); text-decoration:none;">🐦</a>
            <a href="#" style="color:rgba(255,255,255,.7); text-decoration:none;">📷</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# Pages
# =========================
if st.session_state.current_page == 'home':
    st.markdown(f'<h1 class="hero-name floating">{PROFILE["name"]}</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="hero-title">{PROFILE["tagline"]}</p>', unsafe_allow_html=True)

    # Quick Stats
    st.markdown("---")
    cols = st.columns(4)
    metrics = [
        ("Patents", f"{total_patents}+", "📋"),
        ("Projects", f"{total_projects}+", "💡"),
        ("Awards & Certificates", f"{total_awards}+", "🏆"),
        ("Dean’s List", "6", "🎓")
    ]
    for col, (label, value, icon) in zip(cols, metrics):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size:2rem; margin-bottom:10px;">{icon}</div>
                <div class="metric-number">{value}</div>
                <div class="metric-label">{label}</div>
            </div>""", unsafe_allow_html=True)

    # Summary + Core Expertise
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">About</h2>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f'<p class="text-white" style="font-size:1.1rem; line-height:1.8;">{PROFILE["summary"]}</p>', unsafe_allow_html=True)

        st.markdown('<h3 class="text-gradient" style="margin-top: 30px;">Current Focus</h3>', unsafe_allow_html=True)
        for p in ["AI‑продукты (Telecom/Health/EdTech)", "Blockchain‑системы (Edu/Ports/Supply Chain)", "Edge‑инференс и оптимизация производительности"]:
            st.markdown(f'<div class="skill-tag">{p}</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<h3 class="text-gradient">Core Expertise</h3>', unsafe_allow_html=True)
        for cat, skills in SKILLS.items():
            st.markdown(f'<p class="text-white" style="font-weight:600; margin-top:15px;">{cat}</p>', unsafe_allow_html=True)
            for s in skills[:6]:
                st.markdown(f'<div class="skill-tag">{s}</div>', unsafe_allow_html=True)

        st.markdown('<h3 class="text-gradient" style="margin-top: 30px;">Languages</h3>', unsafe_allow_html=True)
        for lang in PROFILE["languages"]:
            st.markdown(f'<div class="skill-tag" style="margin:5px 0;">{lang}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_page == 'career':
    st.markdown('<h1 class="hero-name">Career Journey</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-title">Professional Evolution</p>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Professional Timeline</h2>', unsafe_allow_html=True)
    for i, position in enumerate(EXPERIENCE):
        color = "#667eea" if i % 2 == 0 else "#764ba2"
        bullets_html = "".join([f'<li class="text-white" style="margin:6px 0;">{b}</li>' for b in position["bullets"]])
        stack_html = "".join([f'<span class="skill-tag">{t}</span>' for t in position["stack"]])
        st.markdown(f"""
        <div class="achievement-card">
          <div style="display:flex; align-items:start; gap:20px;">
            <div style="min-width:60px;height:60px;background:linear-gradient(135deg,{color} 0%,#764ba2 100%);
                        border-radius:15px;display:flex;align-items:center;justify-content:center;color:white;font-weight:bold;font-size:1.5rem;">
              {i+1}
            </div>
            <div style="flex:1;">
              <h3 class="text-white">{position["title"]}</h3>
              <p class="text-gradient" style="font-weight:600; font-size:1.05rem;">{position["company"]}</p>
              <p class="text-muted">{position["period"]}{' • ' + position['location'] if position['location'] else ''}</p>
              <ul style="list-style: none; padding-left:0; margin:10px 0 0 0;">{bullets_html}</ul>
              <div style="margin-top:12px;">{stack_html}</div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_page == 'education':
    st.markdown('<h1 class="hero-name">Education</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-title">Degrees, Programs & Distinctions</p>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Academic Background</h2>', unsafe_allow_html=True)

    for e in EDUCATION:
        details = "".join([f'<li class="text-white" style="margin:6px 0;">{d}</li>' for d in e["details"]])
        st.markdown(f"""
        <div class="achievement-card">
            <h3 class="text-white">{e["school"]}</h3>
            <p class="text-gradient" style="font-weight:600; font-size:1.05rem;">{e["degree"]}</p>
            <p class="text-muted">{e["period"]}</p>
            <ul style="list-style:none; padding-left:0; margin-top:10px;">{details}</ul>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_page == 'projects':
    st.markdown('<h1 class="hero-name">Innovation Portfolio</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-title">Building Technology That Ships</p>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Featured Projects</h2>', unsafe_allow_html=True)
    for p in PROJECTS:
        metrics_html = "".join([f'<div><p class="text-gradient" style="font-weight:700; font-size:1.1rem;">{v}</p><p class="text-muted" style="font-size:.9rem;">{k}</p></div>' for k, v in p["metrics"].items()])
        tech_html = "".join([f'<span class="skill-tag">{t}</span>' for t in p["tech"]])
        st.markdown(f"""
        <div class="achievement-card">
            <div style="display:flex; justify-content:space-between; align-items:start;">
                <div style="flex:1;">
                    <h3 class="text-white">{p["name"]}</h3>
                    <span style="background:#00ff88; color:#000; padding:5px 15px; border-radius:20px; font-weight:600; font-size:.9rem; display:inline-block; margin:10px 0;">
                        {p["status"]}
                    </span>
                    <p class="text-gradient" style="font-weight:600; margin:10px 0;">{p["category"]} • {p["year"]}</p>
                    <p class="text-white" style="margin:15px 0;">{p["description"]}</p>
                    <div style="margin: 20px 0;">
                        <p class="text-muted" style="margin-bottom:10px;">Technologies:</p>
                        <div style="display:flex; flex-wrap:wrap; gap:10px;">{tech_html}</div>
                    </div>
                    <div style="display:flex; gap:30px; margin-top:10px;">{metrics_html}</div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_page == 'patents':
    st.markdown('<h1 class="hero-name">Patents</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-title">Intellectual Property Portfolio</p>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Registered Patents (KZ)</h2>', unsafe_allow_html=True)

    for pt in sorted(PATENTS, key=lambda x: x["date"], reverse=True):
        dt = datetime.fromisoformat(pt["date"]).strftime("%b %d, %Y")
        st.markdown(f"""
        <div class="achievement-card">
            <h3 class="text-white">{pt["title"]}</h3>
            <p class="text-gradient" style="font-weight:600;">{pt["no"]} • {dt} • {pt["area"]}</p>
            <p class="text-white" style="margin-top:10px;">{pt["summary"]}</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_page == 'achievements':
    st.markdown('<h1 class="hero-name">Achievements & Recognition</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-title">Awards, Honors & Certificates</p>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Highlights</h2>', unsafe_allow_html=True)

    for a in sorted(AWARDS, key=lambda x: (x["year"], x["title"]), reverse=True):
        st.markdown(f"""
        <div class="achievement-card">
            <div style="display:flex; align-items:start; gap:20px;">
                <div style="font-size:3rem;">🏆</div>
                <div style="flex:1;">
                    <h3 class="text-white">{a["title"]}</h3>
                    <p class="text-gradient" style="font-weight:600; font-size:1.05rem;">{a["org"]} • {a["year"]}</p>
                    <p class="text-muted" style="margin:10px 0;">{a["notes"]}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_page == 'analytics':
    st.markdown('<h1 class="hero-name">Performance Analytics</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-title">Data‑Driven Snapshot</p>', unsafe_allow_html=True)

    # Summary metrics
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Snapshot</h2>', unsafe_allow_html=True)

    cols = st.columns(4)
    stats = [
        ("Patents Filed", str(total_patents), "📋", f"{sum(1 for p in PATENTS if p['date'][:4]=='2025')} in 2025"),
        ("Projects (featured)", str(total_projects), "💡", f"{sum(1 for p in PROJECTS if p['year']>=2023)} since 2023"),
        ("Awards & Certificates", str(total_awards), "🏆", "multi‑year"),
        ("Dean’s List", "6", "🎓", "RIT Dubai")
    ]
    for i, (label, value, icon, note) in enumerate(stats):
        with cols[i % 4]:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size:2rem;">{icon}</div>
                <div class="metric-number">{value}</div>
                <div class="metric-label">{label}</div>
                <p class="text-gradient" style="font-size:.9rem; margin-top:10px;">{note}</p>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Growth lines by year
    def count_by_year(items, get_year):
        c = Counter(get_year(x) for x in items)
        ys = sorted(y for y in c if y is not None)
        return ys, [c[y] for y in ys]

    # patents per year
    py, pc = count_by_year(PATENTS, lambda x: int(x["date"][:4]))
    # projects per year
    jy, jc = count_by_year(PROJECTS, lambda x: x.get("year"))
    # awards per year
    ay, ac = count_by_year(AWARDS, lambda x: x.get("year"))

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Growth Trajectory</h2>', unsafe_allow_html=True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=py, y=pc, name='Patents', line=dict(width=3), marker=dict(size=8)))
    fig.add_trace(go.Scatter(x=jy, y=jc, name='Projects', line=dict(width=3), marker=dict(size=8)))
    fig.add_trace(go.Scatter(x=ay, y=ac, name='Awards', line=dict(width=3), marker=dict(size=8)))
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'),
        height=420, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(title="Year", gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(title="Count", gridcolor='rgba(255,255,255,0.1)')
    )
    st.plotly_chart(fig, use_container_width=True)

    # Skills bar
    st.markdown('<h2 class="section-header">Skills Distribution</h2>', unsafe_allow_html=True)
    skills_data = pd.DataFrame({
        'Skill': ["AI/ML","Backend","DevOps/Cloud","Blockchain","Other"],
        'Level': [95, 90, 85, 80, 88]
    })
    fig2 = px.bar(skills_data, x='Level', y='Skill', orientation='h', color='Level', color_continuous_scale=['#667eea','#764ba2'])
    fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'),
                       height=320, showlegend=False,
                       xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                       yaxis=dict(gridcolor='rgba(255,255,255,0.1)'))
    st.plotly_chart(fig2, use_container_width=True)

# Footer
st.markdown("""
<div style="margin-top: 60px; padding: 30px 0; text-align: center; border-top: 1px solid rgba(255,255,255,0.1);">
    <p class="text-muted">© 2025 Alisher Beisembekov. Building at the intersection of AI, telecom, health & blockchain.</p>
</div>
""", unsafe_allow_html=True)
