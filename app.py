import streamlit as st
from google import genai
import sqlite3
import pypdf

# 1. Page Configuration & Custom CSS for SaaS Layout
st.set_page_config(page_title="StudyMate AI", page_icon="📚", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-color: #0b0f19;
        color: #ffffff;
    }
    .hero-title {
        font-size: 3.5rem;
        font-weight: 900;
        line-height: 1.1;
        color: #ffffff;
        margin-bottom: 20px;
    }
    .hero-title span {
        color: #818cf8;
    }
    .badge {
        background-color: rgba(99, 102, 241, 0.15);
        color: #818cf8;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        border: 1px solid rgba(99, 102, 241, 0.3);
        display: inline-block;
        margin-bottom: 20px;
    }
    .hero-desc {
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 30px;
        line-height: 1.6;
    }
    .chat-card {
        background: linear-gradient(145deg, #131826, #0e131f);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.5);
    }
    .chat-bubble {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 12px 18px;
        border-radius: 12px;
        margin-bottom: 12px;
        border: 1px solid rgba(255, 255, 255, 0.04);
        font-size: 0.95rem;
        color: #e2e8f0;
    }
    .stButton>button {
        background: linear-gradient(90deg, #6366f1, #818cf8);
        color: white;
        font-weight: bold;
        border: none;
        padding: 12px 24px;
        border-radius: 10px;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Database & Client Setup
def init_db():
    conn = sqlite3.connect('study_planner.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS study_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subjects TEXT,
            exam_date TEXT,
            study_hours INTEGER,
            plan TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# 3. Main Hero Section
col1, col2 = st.columns([1.2, 1], gap="large")

with col1:
    st.markdown('<div class="badge">🚀 Generative & Agentic AI Powered</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">Your Personal <span>AI</span><br>Studying<br>Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-desc">StudyMate AI uses Generative AI to create personalized study plans from your manual inputs or uploaded syllabus documents, generate quizzes, and help you prepare smarter.</div>', unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="chat-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <span style="font-weight: bold; font-size: 1.1rem;">🤖 AI Assistant</span>
                <span style="color: #22c55e; font-size: 0.85rem; font-weight: 600;">● Online</span>
            </div>
            <div class="chat-bubble">👋 Hello student!</div>
            <div class="chat-bubble">📄 PDF syllabus processing ready.</div>
            <div class="chat-bubble">📊 Structured scheduling active.</div>
            <div class="chat-bubble">📥 Instant text export enabled.</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.1); margin: 40px 0;'>", unsafe_allow_html=True)

# 4. Functional App Sections (Planner & Quiz Generator Tabs)
st.markdown("### 🛠️ Interactive Workspace")
tab1, tab2 = st.tabs(["📅 AI Study Planner", "📝 AI Quiz Generator"])

with tab1:
    with st.form("study_form"):
        st.subheader("Configure Your Study Plan")
        
        # PDF Uploader inside the form workflow
        uploaded_file = st.file_uploader("Upload your syllabus or curriculum (PDF - Optional)", type=["pdf"])
        
        subjects = st.text_input("Or enter subjects manually:", placeholder="e.g., Physics, Data Structures")
        exam_date = st.date_input("When is your exam?")
        study_hours = st.slider("How many hours can you study per day?", 1, 12, 3)
        submit_button = st.form_submit_button("Generate My Study Plan")

    if submit_button:
        syllabus_text = ""
        if uploaded_file is not None:
            reader = pypdf.PdfReader(uploaded_file)
            for page in reader.pages:
                syllabus_text += page.extract_text() or ""
        
        if subjects or syllabus_text:
            with st.spinner("🤖 Analyzing material and crafting your intelligent schedule..."):
                prompt = f"""
                Create a detailed, day-by-day study schedule for a student studying for {exam_date} with {study_hours} hours available per day.
                Subjects/Focus: {subjects}
                Additional Syllabus/Curriculum Context extracted from PDF: {syllabus_text}
                Format it beautifully with markdown.
                """
                try:
                    response = client.models.generate_content(model='gemini-3.5-flash', contents=prompt)
                    plan_text = response.text
                    
                    conn = sqlite3.connect('study_planner.db')
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO study_plans (subjects, exam_date, study_hours, plan) VALUES (?, ?, ?, ?)",
                                   (subjects if subjects else "PDF Syllabus Plan", str(exam_date), study_hours, plan_text))
                    conn.commit()
                    conn.close()
                    
                    st.success("✨ Study plan generated and saved successfully!")
                    st.markdown("---")
                    st.markdown(plan_text)
                    
                    st.download_button(
                        label="📥 Download Study Plan as Text File",
                        data=plan_text,
                        file_name="studymate_plan.txt",
                        mime="text/plain"
                    )
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("⚠️ Please provide manual subjects or upload a syllabus PDF.")

with tab2:
    with st.form("quiz_form"):
        st.subheader("Generate Interactive Practice Quiz")
        quiz_subject = st.text_input("Enter subject or topic:", placeholder="e.g., Calculus, Python Programming")
        quiz_button = st.form_submit_button("Generate Quiz")

    if quiz_button:
        if quiz_subject:
            with st.spinner("✍️ Crafting custom practice questions..."):
                quiz_prompt = f"Create a 5-question multiple-choice practice quiz with answers at the bottom for the topic: {quiz_subject}. Format it clearly."
                try:
                    quiz_response = client.models.generate_content(model='gemini-3.5-flash', contents=quiz_prompt)
                    st.success("🎯 Quiz Ready!")
                    st.markdown("---")
                    st.markdown(quiz_response.text)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("⚠️ Please enter a topic.")