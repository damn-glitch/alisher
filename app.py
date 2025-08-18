import streamlit as st
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Alisher Beisembekov - Portfolio",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1e3d59;
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .section-header {
        font-size: 2rem;
        color: #2c3e50;
        border-bottom: 3px solid #3498db;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    .achievement-card {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        border-left: 4px solid #3498db;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Home'

# Sidebar Navigation
st.sidebar.markdown("# 🌟 Alisher Beisembekov")
st.sidebar.markdown("---")

# Navigation Menu
pages = {
    "🏠 Home": "Home",
    "👔 Professional": "Professional",
    "🔬 Science & Research": "Science",
    "💻 Programming": "Programming",
    "👨‍💼 Leadership": "Leadership",
    "🏆 Sports": "Sports",
    "📰 Media & News": "Media",
    "📊 Statistics": "Statistics"
}

for page_name, page_key in pages.items():
    if st.sidebar.button(page_name, key=page_key, use_container_width=True):
        st.session_state.current_page = page_key

st.sidebar.markdown("---")
st.sidebar.markdown("### 🌐 Quick Links")
st.sidebar.markdown("[LinkedIn](#) | [GitHub](#) | [Website](#)")

# Data Structure - To be filled with actual information
data = {
    "personal_info": {
        "name": "Alisher Beisembekov",
        "title": "CEO | Scientist | Programmer | Athlete",
        "email": "your.email@example.com",
        "location": "Your Location",
        "languages": [
            "English - Fluent",
            "Russian - Native",
            "Kazakh - Native",
            # Add more languages
        ],
        "bio": "Brief biography to be added here..."
    },

    "professional": {
        "current_positions": [
            {
                "title": "CEO / Founder",
                "company": "Company Name",
                "period": "2020 - Present",
                "description": "Description to be added..."
            },
            # Add more positions
        ],
        "patents": [
            {
                "title": "Patent Title 1",
                "number": "Patent Number",
                "date": "Date",
                "description": "Description",
                "link": "#"
            },
            # Add more patents
        ],
        "certifications": [
            {
                "name": "Certification Name",
                "issuer": "Issuing Organization",
                "date": "Date",
                "credential_id": "ID",
                "link": "#"
            },
            # Add more certifications
        ]
    },

    "science": {
        "research_papers": [
            {
                "title": "Research Paper Title",
                "journal": "Journal Name",
                "year": "Year",
                "authors": "Authors",
                "link": "#",
                "citations": 0
            },
            # Add more papers
        ],
        "research_projects": [
            {
                "name": "Project Name",
                "role": "Your Role",
                "period": "Time Period",
                "description": "Description",
                "technologies": ["Tech1", "Tech2"],
                "link": "#"
            },
            # Add more projects
        ],
        "conferences": [
            {
                "name": "Conference Name",
                "role": "Speaker/Attendee",
                "date": "Date",
                "topic": "Presentation Topic",
                "location": "Location"
            },
            # Add more conferences
        ]
    },

    "programming": {
        "skills": {
            "languages": ["Python", "JavaScript", "C++", "Java"],
            "frameworks": ["TensorFlow", "React", "Django", "Flutter"],
            "tools": ["Git", "Docker", "Kubernetes", "AWS"],
            "databases": ["PostgreSQL", "MongoDB", "Redis"]
        },
        "projects": [
            {
                "name": "Project Name",
                "description": "Project Description",
                "technologies": ["Tech1", "Tech2"],
                "github_link": "#",
                "demo_link": "#",
                "status": "Completed/Ongoing"
            },
            # Add more projects
        ],
        "contributions": [
            {
                "repo": "Repository Name",
                "type": "Feature/Bug Fix",
                "description": "Contribution Description",
                "link": "#"
            },
            # Add more contributions
        ]
    },

    "leadership": {
        "companies_founded": [
            {
                "name": "Company Name",
                "industry": "Industry",
                "founded": "Year",
                "employees": "Number",
                "description": "Company Description",
                "website": "#"
            },
            # Add more companies
        ],
        "board_positions": [
            {
                "organization": "Organization Name",
                "position": "Board Position",
                "period": "Time Period"
            },
            # Add more positions
        ],
        "mentorship": [
            {
                "program": "Mentorship Program",
                "role": "Mentor",
                "period": "Time Period",
                "mentees": 0
            },
            # Add more mentorship
        ]
    },

    "sports": {
        "disciplines": [
            {
                "sport": "Sport Name",
                "level": "Professional/Amateur",
                "years_active": "Years"
            },
            # Add more sports
        ],
        "achievements": [
            {
                "competition": "Competition Name",
                "position": "1st/2nd/3rd",
                "year": "Year",
                "location": "Location",
                "category": "Category",
                "certificate_link": "#"
            },
            # Add more achievements
        ],
        "records": [
            {
                "record": "Record Description",
                "date": "Date",
                "verified_by": "Organization"
            },
            # Add more records
        ]
    },

    "media": {
        "news_articles": [
            {
                "headline": "Article Headline",
                "publisher": "News Outlet",
                "date": "Date",
                "link": "#",
                "excerpt": "Brief excerpt..."
            },
            # Add more articles
        ],
        "interviews": [
            {
                "title": "Interview Title",
                "media": "TV/Radio/Podcast",
                "date": "Date",
                "link": "#"
            },
            # Add more interviews
        ],
        "social_media": {
            "linkedin": "#",
            "twitter": "#",
            "instagram": "#",
            "youtube": "#"
        }
    },

    "awards": [
        {
            "name": "Award Name",
            "organization": "Awarding Organization",
            "year": "Year",
            "category": "Category",
            "description": "Achievement Description",
            "certificate_link": "#"
        },
        # Add more awards
    ]
}

# Page Content Based on Selection
current_page = st.session_state.current_page

if current_page == "Home":
    # Hero Section
    st.markdown('<h1 class="main-header">Alisher Beisembekov</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p style="text-align: center; font-size: 1.5rem; color: #7f8c8d;">CEO | Scientist | Programmer | Athlete</p>',
        unsafe_allow_html=True)

    st.markdown("---")

    # Quick Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Patents", "0", "To be updated")
    with col2:
        st.metric("Publications", "0", "To be updated")
    with col3:
        st.metric("Projects", "0", "To be updated")
    with col4:
        st.metric("Awards", "0", "To be updated")

    st.markdown("---")

    # About Section
    st.markdown("## 📝 About Me")
    st.write(data["personal_info"]["bio"])

    # Languages
    st.markdown("### 🌍 Languages")
    cols = st.columns(3)
    for i, lang in enumerate(data["personal_info"]["languages"]):
        with cols[i % 3]:
            st.write(f"• {lang}")

    # Recent Highlights
    st.markdown("## ⭐ Recent Highlights")
    highlight_cols = st.columns(2)
    with highlight_cols[0]:
        st.info("📰 **Latest News**: Feature in major publication coming soon...")
    with highlight_cols[1]:
        st.success("🏆 **Recent Achievement**: Details to be added...")

elif current_page == "Professional":
    st.markdown("# 👔 Professional Experience")

    # Current Positions
    st.markdown("## Current Positions")
    for position in data["professional"]["current_positions"]:
        with st.expander(f"{position['title']} at {position['company']}"):
            st.write(f"**Period**: {position['period']}")
            st.write(position['description'])

    # Patents
    st.markdown("## 📋 Patents")
    if data["professional"]["patents"]:
        for patent in data["professional"]["patents"]:
            st.markdown(f"""
            <div class="achievement-card">
                <h4>{patent['title']}</h4>
                <p><strong>Patent Number:</strong> {patent['number']}</p>
                <p><strong>Date:</strong> {patent['date']}</p>
                <p>{patent['description']}</p>
                <a href="{patent['link']}">View Patent →</a>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Patent information to be added...")

    # Certifications
    st.markdown("## 🎓 Certifications")
    if data["professional"]["certifications"]:
        for cert in data["professional"]["certifications"]:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{cert['name']}**")
                st.write(f"Issued by: {cert['issuer']} | Date: {cert['date']}")
            with col2:
                st.markdown(f"[View Certificate]({cert['link']})")
    else:
        st.info("Certification information to be added...")

elif current_page == "Science":
    st.markdown("# 🔬 Science & Research")

    # Research Papers
    st.markdown("## 📚 Research Publications")
    if data["science"]["research_papers"]:
        for paper in data["science"]["research_papers"]:
            with st.expander(paper["title"]):
                st.write(f"**Journal**: {paper['journal']}")
                st.write(f"**Year**: {paper['year']}")
                st.write(f"**Authors**: {paper['authors']}")
                st.write(f"**Citations**: {paper['citations']}")
                st.markdown(f"[Read Paper]({paper['link']})")
    else:
        st.info("Research publications to be added...")

    # Research Projects
    st.markdown("## 🔬 Research Projects")
    for project in data["science"]["research_projects"]:
        with st.expander(project["name"]):
            st.write(f"**Role**: {project['role']}")
            st.write(f"**Period**: {project['period']}")
            st.write(project['description'])
            st.write(f"**Technologies**: {', '.join(project['technologies'])}")
            if project['link']:
                st.markdown(f"[Project Link]({project['link']})")

    # Conferences
    st.markdown("## 🎤 Conference Presentations")
    if data["science"]["conferences"]:
        for conf in data["science"]["conferences"]:
            st.write(f"• **{conf['name']}** ({conf['date']}) - {conf['role']}")
            st.write(f"  Topic: {conf['topic']}, Location: {conf['location']}")
    else:
        st.info("Conference information to be added...")

elif current_page == "Programming":
    st.markdown("# 💻 Programming & Technology")

    # Skills Overview
    st.markdown("## 🛠️ Technical Skills")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("### Languages")
        for lang in data["programming"]["skills"]["languages"]:
            st.write(f"• {lang}")

    with col2:
        st.markdown("### Frameworks")
        for fw in data["programming"]["skills"]["frameworks"]:
            st.write(f"• {fw}")

    with col3:
        st.markdown("### Tools")
        for tool in data["programming"]["skills"]["tools"]:
            st.write(f"• {tool}")

    with col4:
        st.markdown("### Databases")
        for db in data["programming"]["skills"]["databases"]:
            st.write(f"• {db}")

    # Projects
    st.markdown("## 💡 Projects")
    for project in data["programming"]["projects"]:
        with st.expander(project["name"]):
            st.write(project["description"])
            st.write(f"**Technologies**: {', '.join(project['technologies'])}")
            st.write(f"**Status**: {project['status']}")
            col1, col2 = st.columns(2)
            with col1:
                if project["github_link"]:
                    st.markdown(f"[GitHub]({project['github_link']})")
            with col2:
                if project["demo_link"]:
                    st.markdown(f"[Live Demo]({project['demo_link']})")

    # Open Source Contributions
    st.markdown("## 🌐 Open Source Contributions")
    if data["programming"]["contributions"]:
        for contrib in data["programming"]["contributions"]:
            st.write(f"• **{contrib['repo']}** - {contrib['type']}")
            st.write(f"  {contrib['description']}")
            st.markdown(f"  [View Contribution]({contrib['link']})")
    else:
        st.info("Contributions to be added...")

elif current_page == "Leadership":
    st.markdown("# 👨‍💼 Leadership & Entrepreneurship")

    # Companies Founded
    st.markdown("## 🏢 Companies Founded")
    for company in data["leadership"]["companies_founded"]:
        with st.expander(company["name"]):
            st.write(f"**Industry**: {company['industry']}")
            st.write(f"**Founded**: {company['founded']}")
            st.write(f"**Employees**: {company['employees']}")
            st.write(company["description"])
            if company["website"]:
                st.markdown(f"[Company Website]({company['website']})")

    # Board Positions
    st.markdown("## 👥 Board Positions")
    if data["leadership"]["board_positions"]:
        for position in data["leadership"]["board_positions"]:
            st.write(f"• **{position['organization']}** - {position['position']} ({position['period']})")
    else:
        st.info("Board positions to be added...")

    # Mentorship
    st.markdown("## 🎯 Mentorship & Coaching")
    if data["leadership"]["mentorship"]:
        for mentor in data["leadership"]["mentorship"]:
            st.write(f"• **{mentor['program']}** - {mentor['role']} ({mentor['period']})")
            st.write(f"  Mentees: {mentor['mentees']}")
    else:
        st.info("Mentorship information to be added...")

elif current_page == "Sports":
    st.markdown("# 🏆 Sports Achievements")

    # Sports Disciplines
    st.markdown("## 🏃 Sports Disciplines")
    cols = st.columns(3)
    for i, sport in enumerate(data["sports"]["disciplines"]):
        with cols[i % 3]:
            st.info(f"**{sport['sport']}**\n\nLevel: {sport['level']}\n\nActive: {sport['years_active']}")

    # Competition Achievements
    st.markdown("## 🥇 Competition Results")
    if data["sports"]["achievements"]:
        for achievement in data["sports"]["achievements"]:
            with st.expander(f"{achievement['competition']} - {achievement['position']} Place"):
                st.write(f"**Year**: {achievement['year']}")
                st.write(f"**Location**: {achievement['location']}")
                st.write(f"**Category**: {achievement['category']}")
                if achievement["certificate_link"]:
                    st.markdown(f"[View Certificate]({achievement['certificate_link']})")
    else:
        st.info("Competition achievements to be added...")

    # Records
    st.markdown("## 📊 Records")
    if data["sports"]["records"]:
        for record in data["sports"]["records"]:
            st.success(f"**{record['record']}**\n\nDate: {record['date']}\n\nVerified by: {record['verified_by']}")
    else:
        st.info("Records to be added...")

elif current_page == "Media":
    st.markdown("# 📰 Media Coverage & News")

    # News Articles
    st.markdown("## 📰 News Articles")
    if data["media"]["news_articles"]:
        for article in data["media"]["news_articles"]:
            with st.expander(article["headline"]):
                st.write(f"**Publisher**: {article['publisher']}")
                st.write(f"**Date**: {article['date']}")
                st.write(article["excerpt"])
                st.markdown(f"[Read Full Article]({article['link']})")
    else:
        st.info("News articles to be added...")

    # Interviews
    st.markdown("## 🎙️ Interviews & Features")
    if data["media"]["interviews"]:
        for interview in data["media"]["interviews"]:
            st.write(f"• **{interview['title']}** - {interview['media']} ({interview['date']})")
            st.markdown(f"  [Watch/Listen]({interview['link']})")
    else:
        st.info("Interview information to be added...")

    # Social Media
    st.markdown("## 🌐 Social Media Presence")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"[LinkedIn]({data['media']['social_media']['linkedin']})")
    with col2:
        st.markdown(f"[Twitter]({data['media']['social_media']['twitter']})")
    with col3:
        st.markdown(f"[Instagram]({data['media']['social_media']['instagram']})")
    with col4:
        st.markdown(f"[YouTube]({data['media']['social_media']['youtube']})")

elif current_page == "Statistics":
    st.markdown("# 📊 Statistics & Overview")

    # Overall Stats
    st.markdown("## 📈 Career Statistics")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Patents", "0")
        st.metric("Research Papers", "0")
        st.metric("Projects Completed", "0")
        st.metric("Companies Founded", "0")

    with col2:
        st.metric("Sports Medals", "0")
        st.metric("Media Features", "0")
        st.metric("Certifications", "0")
        st.metric("Conference Talks", "0")

    # Timeline
    st.markdown("## 📅 Career Timeline")
    st.info("Interactive timeline to be implemented...")

    # Awards Summary
    st.markdown("## 🏅 All Awards & Recognitions")
    if data["awards"]:
        for award in data["awards"]:
            with st.expander(f"{award['name']} ({award['year']})"):
                st.write(f"**Organization**: {award['organization']}")
                st.write(f"**Category**: {award['category']}")
                st.write(award["description"])
                if award["certificate_link"]:
                    st.markdown(f"[View Certificate]({award['certificate_link']})")
    else:
        st.info("Awards information to be added...")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #7f8c8d; padding: 20px;'>
        <p>© 2024 Alisher Beisembekov. All rights reserved.</p>
        <p>Last Updated: """ + datetime.now().strftime("%B %Y") + """</p>
    </div>
    """,
    unsafe_allow_html=True
)