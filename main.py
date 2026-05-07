import streamlit as st
import json
import time
import random
from datetime import datetime
from backend.interview_engine import InterviewEngine
from backend.evaluator import ResponseEvaluator
from backend.session_manager import SessionManager

# ─────────────────────────────────────────────
# Page Configuration
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AI Mock Interview Platform",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# Custom CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* Main theme */
    .main { background-color: #0f1117; }
    
    /* Hero banner */
    .hero-banner {
        background: linear-gradient(135deg, #1a1f36 0%, #0d1b2a 100%);
        border: 1px solid #2d3561;
        border-radius: 16px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    .hero-banner h1 { color: #6c63ff; font-size: 2.5rem; margin-bottom: 0.5rem; }
    .hero-banner p { color: #a0aec0; font-size: 1.1rem; }

    /* Cards */
    .metric-card {
        background: linear-gradient(145deg, #1e2235, #161929);
        border: 1px solid #2d3561;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card h3 { color: #6c63ff; font-size: 2rem; margin: 0; }
    .metric-card p  { color: #a0aec0; margin: 0; font-size: 0.9rem; }

    /* Question box */
    .question-box {
        background: linear-gradient(145deg, #1a2744, #111827);
        border-left: 4px solid #6c63ff;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #e2e8f0;
        font-size: 1.1rem;
        line-height: 1.6;
    }

    /* Feedback box */
    .feedback-box {
        background: #0d1f0d;
        border: 1px solid #2d7a2d;
        border-radius: 8px;
        padding: 1.2rem;
        margin: 0.5rem 0;
        color: #c6efce;
    }
    .feedback-box.warning {
        background: #1a1a0d;
        border-color: #7a7a2d;
        color: #efefce;
    }

    /* Score badge */
    .score-badge {
        display: inline-block;
        background: linear-gradient(135deg, #6c63ff, #a78bfa);
        color: white;
        border-radius: 50px;
        padding: 0.4rem 1.2rem;
        font-weight: bold;
        font-size: 1.2rem;
    }

    /* Chat message */
    .chat-msg-ai {
        background: #1e2235;
        border-radius: 12px 12px 12px 2px;
        padding: 1rem 1.2rem;
        margin: 0.5rem 0;
        color: #e2e8f0;
        border-left: 3px solid #6c63ff;
    }
    .chat-msg-user {
        background: #1a2f1a;
        border-radius: 12px 12px 2px 12px;
        padding: 1rem 1.2rem;
        margin: 0.5rem 0;
        color: #e2e8f0;
        border-right: 3px solid #48bb78;
        text-align: right;
    }

    /* Progress bar override */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #6c63ff, #a78bfa);
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #6c63ff, #a78bfa);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(108, 99, 255, 0.4);
    }

    /* Sidebar */
    .css-1d391kg { background: #0d1117; }
    
    /* Section headers */
    .section-header {
        color: #6c63ff;
        font-size: 1.3rem;
        font-weight: 700;
        border-bottom: 2px solid #2d3561;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }
    
    /* Status indicator */
    .status-dot {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 6px;
    }
    .status-dot.active { background: #48bb78; box-shadow: 0 0 6px #48bb78; }
    .status-dot.inactive { background: #718096; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Session State Initialization
# ─────────────────────────────────────────────
def init_session():
    defaults = {
        "page": "home",
        "role": None,
        "difficulty": "Intermediate",
        "questions": [],
        "current_q": 0,
        "answers": [],
        "scores": [],
        "feedbacks": [],
        "chat_history": [],
        "session_started": False,
        "session_complete": False,
        "interview_id": None,
        "start_time": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()
engine = InterviewEngine()
evaluator = ResponseEvaluator()
session_mgr = SessionManager()


# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎯 Mock Interview AI")
    st.markdown("---")

    # Status
    if st.session_state.session_started and not st.session_state.session_complete:
        st.markdown('<span class="status-dot active"></span> **Session Active**', unsafe_allow_html=True)
        q_num = st.session_state.current_q
        total  = len(st.session_state.questions)
        if total > 0:
            progress = q_num / total
            st.progress(progress)
            st.markdown(f"**Question {q_num}/{total}**")
    else:
        st.markdown('<span class="status-dot inactive"></span> No Active Session', unsafe_allow_html=True)

    st.markdown("---")

    # Navigation
    st.markdown("### 📋 Navigation")
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()
    if st.button("🎤 Interview Room", use_container_width=True):
        st.session_state.page = "interview"
        st.rerun()
    if st.button("📊 Dashboard", use_container_width=True):
        st.session_state.page = "dashboard"
        st.rerun()
    if st.button("📜 Session History", use_container_width=True):
        st.session_state.page = "history"
        st.rerun()

    st.markdown("---")

    # Quick stats
    history = session_mgr.get_all_sessions()
    if history:
        avg_score = sum(s["total_score"] for s in history) / len(history)
        st.markdown("### 📈 Quick Stats")
        st.metric("Total Sessions", len(history))
        st.metric("Avg Score", f"{avg_score:.1f}/10")
        best = max(history, key=lambda x: x["total_score"])
        st.metric("Best Score", f"{best['total_score']:.1f}/10")

    st.markdown("---")
    st.markdown("*Powered by Claude AI*")
    st.markdown("*Built with Streamlit*")


# ═══════════════════════════════════════════════════════════
# PAGE: HOME
# ═══════════════════════════════════════════════════════════
def page_home():
    st.markdown("""
    <div class="hero-banner">
        <h1>🎯 AI Mock Interview Platform</h1>
        <p>Practice your interviews with AI-powered feedback, adaptive questions, and detailed scoring</p>
    </div>
    """, unsafe_allow_html=True)

    # Feature cards
    col1, col2, col3, col4 = st.columns(4)
    features = [
        ("🤖", "AI Questions", "Dynamic role-based questions"),
        ("📊", "Live Scoring", "Real-time answer evaluation"),
        ("💬", "Feedback", "Detailed improvement tips"),
        ("📈", "Analytics", "Track progress over time"),
    ]
    for col, (icon, title, desc) in zip([col1, col2, col3, col4], features):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{icon}</h3>
                <p><strong style="color:#e2e8f0">{title}</strong></p>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-header">🚀 Start New Interview Session</div>', unsafe_allow_html=True)

    col_left, col_right = st.columns([2, 1])
    with col_left:
        roles = [
            "Software Engineer",
            "Data Scientist",
            "Product Manager",
            "DevOps Engineer",
            "Frontend Developer",
            "Backend Developer",
            "Machine Learning Engineer",
            "System Design Engineer",
            "HR Manager",
            "Business Analyst",
        ]
        role = st.selectbox("🎭 Select Your Role", roles)
        difficulty = st.select_slider(
            "⚙️ Difficulty Level",
            options=["Beginner", "Intermediate", "Advanced", "Expert"],
            value="Intermediate",
        )
        num_questions = st.slider("❓ Number of Questions", 3, 10, 5)

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🎤 Start Interview", use_container_width=True):
                with st.spinner("Generating your personalized interview..."):
                    questions = engine.generate_questions(role, difficulty, num_questions)
                st.session_state.role = role
                st.session_state.difficulty = difficulty
                st.session_state.questions = questions
                st.session_state.current_q = 0
                st.session_state.answers = []
                st.session_state.scores = []
                st.session_state.feedbacks = []
                st.session_state.chat_history = []
                st.session_state.session_started = True
                st.session_state.session_complete = False
                st.session_state.interview_id = datetime.now().strftime("%Y%m%d_%H%M%S")
                st.session_state.start_time = datetime.now()
                st.session_state.page = "interview"
                st.rerun()
        with col_btn2:
            if st.button("📊 View Dashboard", use_container_width=True):
                st.session_state.page = "dashboard"
                st.rerun()

    with col_right:
        st.markdown("### 📝 How It Works")
        steps = [
            "Select your target role",
            "Choose difficulty level",
            "AI generates questions",
            "Answer each question",
            "Get instant AI feedback",
            "View session summary",
        ]
        for i, step in enumerate(steps, 1):
            st.markdown(f"**{i}.** {step}")

        st.markdown("---")
        st.info("💡 **Tip:** Use the Intermediate difficulty first to calibrate your performance.")


# ═══════════════════════════════════════════════════════════
# PAGE: INTERVIEW ROOM
# ═══════════════════════════════════════════════════════════
def page_interview():
    if not st.session_state.session_started:
        st.warning("⚠️ No active interview session. Please start from Home.")
        if st.button("Go to Home"):
            st.session_state.page = "home"
            st.rerun()
        return

    if st.session_state.session_complete:
        page_results()
        return

    questions = st.session_state.questions
    current_q = st.session_state.current_q

    # Header
    col_h1, col_h2, col_h3 = st.columns([3, 1, 1])
    with col_h1:
        st.markdown(f"## 🎤 {st.session_state.role} Interview")
    with col_h2:
        st.markdown(f"**Difficulty:** {st.session_state.difficulty}")
    with col_h3:
        elapsed = (datetime.now() - st.session_state.start_time).seconds
        mins, secs = divmod(elapsed, 60)
        st.markdown(f"**⏱ {mins:02d}:{secs:02d}**")

    # Progress
    progress = current_q / len(questions)
    st.progress(progress)
    st.markdown(f"**Question {current_q + 1} of {len(questions)}**")

    # Two-column layout
    col_main, col_side = st.columns([3, 2])

    with col_main:
        if current_q < len(questions):
            q_text = questions[current_q]
            st.markdown(f"""
            <div class="question-box">
                <strong>Q{current_q + 1}:</strong> {q_text}
            </div>
            """, unsafe_allow_html=True)

            answer = st.text_area(
                "✍️ Your Answer",
                placeholder="Type your detailed answer here...",
                height=200,
                key=f"answer_{current_q}",
            )

            col_b1, col_b2, col_b3 = st.columns([2, 2, 1])
            with col_b1:
                submit = st.button("✅ Submit Answer", use_container_width=True)
            with col_b2:
                skip = st.button("⏭ Skip Question", use_container_width=True)
            with col_b3:
                end = st.button("🏁 End", use_container_width=True)

            if submit and answer.strip():
                with st.spinner("🤖 AI is evaluating your answer..."):
                    result = evaluator.evaluate(q_text, answer, st.session_state.role, st.session_state.difficulty)
                st.session_state.answers.append(answer)
                st.session_state.scores.append(result["score"])
                st.session_state.feedbacks.append(result)
                st.session_state.chat_history.append({"role": "ai", "content": q_text})
                st.session_state.chat_history.append({"role": "user", "content": answer})
                st.session_state.chat_history.append({"role": "feedback", "content": result})
                st.session_state.current_q += 1
                if st.session_state.current_q >= len(questions):
                    _finish_session()
                st.rerun()

            elif submit and not answer.strip():
                st.error("Please type your answer before submitting.")

            if skip:
                st.session_state.answers.append("[Skipped]")
                st.session_state.scores.append(0)
                st.session_state.feedbacks.append({"score": 0, "strengths": [], "weaknesses": ["Question skipped"], "suggestion": "", "sample_answer": ""})
                st.session_state.current_q += 1
                if st.session_state.current_q >= len(questions):
                    _finish_session()
                st.rerun()

            if end:
                # Pad remaining
                remaining = len(questions) - current_q
                for _ in range(remaining):
                    st.session_state.answers.append("[Not answered]")
                    st.session_state.scores.append(0)
                    st.session_state.feedbacks.append({"score": 0, "strengths": [], "weaknesses": ["Not answered"], "suggestion": "", "sample_answer": ""})
                _finish_session()
                st.rerun()

    with col_side:
        st.markdown("### 💬 Interview Chat Log")
        chat = st.session_state.chat_history
        if not chat:
            st.info("Your conversation will appear here as you answer questions.")
        else:
            for msg in chat[-10:]:
                if msg["role"] == "ai":
                    st.markdown(f'<div class="chat-msg-ai">🤖 <strong>AI:</strong> {msg["content"]}</div>', unsafe_allow_html=True)
                elif msg["role"] == "user":
                    ans = msg["content"]
                    if len(ans) > 100:
                        ans = ans[:100] + "..."
                    st.markdown(f'<div class="chat-msg-user">👤 {ans}</div>', unsafe_allow_html=True)
                elif msg["role"] == "feedback":
                    fb = msg["content"]
                    st.markdown(f"""
                    <div class="feedback-box">
                        <strong>Score: {fb['score']}/10</strong> ✨
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 📊 Score Progress")
        if st.session_state.scores:
            for i, (q, s) in enumerate(zip(questions[:current_q], st.session_state.scores)):
                label = q[:40] + "..." if len(q) > 40 else q
                color = "#48bb78" if s >= 7 else "#ecc94b" if s >= 5 else "#fc8181"
                st.markdown(f"**Q{i+1}:** <span style='color:{color}'>{s}/10</span>", unsafe_allow_html=True)
        else:
            st.caption("Scores will appear after each answer.")


def _finish_session():
    scores = st.session_state.scores
    total = sum(scores) / len(scores) if scores else 0
    session_mgr.save_session({
        "id": st.session_state.interview_id,
        "role": st.session_state.role,
        "difficulty": st.session_state.difficulty,
        "questions": st.session_state.questions,
        "answers": st.session_state.answers,
        "scores": scores,
        "feedbacks": st.session_state.feedbacks,
        "total_score": round(total, 2),
        "timestamp": datetime.now().isoformat(),
        "duration_secs": (datetime.now() - st.session_state.start_time).seconds,
    })
    st.session_state.session_complete = True


# ═══════════════════════════════════════════════════════════
# PAGE: RESULTS
# ═══════════════════════════════════════════════════════════
def page_results():
    scores = st.session_state.scores
    feedbacks = st.session_state.feedbacks
    questions = st.session_state.questions
    answers = st.session_state.answers
    total_score = round(sum(scores) / len(scores), 2) if scores else 0

    st.markdown("## 🏆 Session Complete!")

    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    grade = "A" if total_score >= 8 else "B" if total_score >= 6 else "C" if total_score >= 4 else "D"
    with col1:
        st.markdown(f'<div class="metric-card"><h3>{total_score}/10</h3><p>Overall Score</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><h3>{grade}</h3><p>Grade</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><h3>{len([s for s in scores if s >= 7])}/{len(scores)}</h3><p>Strong Answers</p></div>', unsafe_allow_html=True)
    with col4:
        dur = (datetime.now() - st.session_state.start_time).seconds
        st.markdown(f'<div class="metric-card"><h3>{dur//60}m {dur%60}s</h3><p>Duration</p></div>', unsafe_allow_html=True)

    st.markdown("---")

    # Score breakdown chart (using streamlit native)
    st.markdown("### 📊 Score Breakdown")
    import pandas as pd
    df = pd.DataFrame({
        "Question": [f"Q{i+1}" for i in range(len(scores))],
        "Score": scores,
    })
    st.bar_chart(df.set_index("Question"))

    st.markdown("---")
    st.markdown("### 📋 Detailed Feedback")

    for i, (q, a, s, fb) in enumerate(zip(questions, answers, scores, feedbacks)):
        with st.expander(f"Q{i+1}: {q[:60]}... — Score: {s}/10"):
            col_l, col_r = st.columns(2)
            with col_l:
                st.markdown("**Your Answer:**")
                st.info(a if a not in ("[Skipped]", "[Not answered]") else f"*{a}*")
                if fb.get("strengths"):
                    st.markdown("**✅ Strengths:**")
                    for strength in fb["strengths"]:
                        st.markdown(f"- {strength}")
                if fb.get("weaknesses"):
                    st.markdown("**⚠️ Areas to Improve:**")
                    for weak in fb["weaknesses"]:
                        st.markdown(f"- {weak}")
            with col_r:
                if fb.get("suggestion"):
                    st.markdown("**💡 Suggestion:**")
                    st.success(fb["suggestion"])
                if fb.get("sample_answer"):
                    st.markdown("**📖 Sample Better Answer:**")
                    st.markdown(f'<div class="feedback-box">{fb["sample_answer"]}</div>', unsafe_allow_html=True)

    st.markdown("---")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🔄 Start New Interview", use_container_width=True):
            for key in ["session_started", "session_complete", "questions", "answers",
                        "scores", "feedbacks", "chat_history", "current_q"]:
                if key in st.session_state:
                    del st.session_state[key]
            init_session()
            st.session_state.page = "home"
            st.rerun()
    with col_b:
        if st.button("📊 View Full Dashboard", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()


# ═══════════════════════════════════════════════════════════
# PAGE: DASHBOARD
# ═══════════════════════════════════════════════════════════
def page_dashboard():
    import pandas as pd

    st.markdown("## 📊 Performance Dashboard")
    history = session_mgr.get_all_sessions()

    if not history:
        st.info("📭 No sessions yet. Complete an interview to see your analytics!")
        if st.button("Start Interview"):
            st.session_state.page = "home"
            st.rerun()
        return

    # KPIs
    avg_score = sum(s["total_score"] for s in history) / len(history)
    best_score = max(s["total_score"] for s in history)
    total_q = sum(len(s["questions"]) for s in history)

    col1, col2, col3, col4 = st.columns(4)
    kpis = [
        ("🎯", f"{len(history)}", "Total Sessions"),
        ("⭐", f"{avg_score:.1f}/10", "Average Score"),
        ("🏆", f"{best_score:.1f}/10", "Best Score"),
        ("❓", f"{total_q}", "Total Questions"),
    ]
    for col, (icon, val, label) in zip([col1, col2, col3, col4], kpis):
        with col:
            st.markdown(f'<div class="metric-card"><h3>{icon} {val}</h3><p>{label}</p></div>', unsafe_allow_html=True)

    st.markdown("---")

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("### 📈 Score Over Time")
        df_scores = pd.DataFrame([
            {"Session": s["id"], "Score": s["total_score"], "Role": s["role"]}
            for s in history
        ])
        st.line_chart(df_scores.set_index("Session")["Score"])

        st.markdown("### 🎭 Sessions by Role")
        role_counts = {}
        for s in history:
            role_counts[s["role"]] = role_counts.get(s["role"], 0) + 1
        df_roles = pd.DataFrame(list(role_counts.items()), columns=["Role", "Count"])
        st.bar_chart(df_roles.set_index("Role"))

    with col_right:
        st.markdown("### 📊 Score Distribution")
        all_q_scores = []
        for s in history:
            all_q_scores.extend(s["scores"])
        df_dist = pd.DataFrame({"Score": all_q_scores})
        st.bar_chart(df_dist["Score"].value_counts().sort_index())

        st.markdown("### 🏅 Best Sessions")
        top3 = sorted(history, key=lambda x: x["total_score"], reverse=True)[:3]
        for i, s in enumerate(top3, 1):
            medal = ["🥇", "🥈", "🥉"][i - 1]
            st.markdown(f"""
            **{medal} Session {s['id'][-8:]}**  
            Role: {s['role']} | Score: **{s['total_score']}/10** | Difficulty: {s.get('difficulty','N/A')}
            """)
            st.markdown("---")

    st.markdown("### 📋 All Sessions")
    df_all = pd.DataFrame([
        {
            "ID": s["id"][-8:],
            "Role": s["role"],
            "Difficulty": s.get("difficulty", "N/A"),
            "Score": s["total_score"],
            "Questions": len(s["questions"]),
            "Date": s["timestamp"][:10],
        }
        for s in history
    ])
    st.dataframe(df_all, use_container_width=True)

    if st.button("🗑️ Clear All History", type="secondary"):
        session_mgr.clear_all()
        st.success("History cleared!")
        st.rerun()


# ═══════════════════════════════════════════════════════════
# PAGE: HISTORY
# ═══════════════════════════════════════════════════════════
def page_history():
    st.markdown("## 📜 Session History")
    history = session_mgr.get_all_sessions()

    if not history:
        st.info("No sessions found. Start your first interview!")
        return

    for s in reversed(history):
        score_color = "#48bb78" if s["total_score"] >= 7 else "#ecc94b" if s["total_score"] >= 5 else "#fc8181"
        with st.expander(f"📁 {s['role']} | Score: {s['total_score']}/10 | {s['timestamp'][:10]}"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Role:** {s['role']}")
                st.markdown(f"**Difficulty:** {s.get('difficulty','N/A')}")
                st.markdown(f"**Questions:** {len(s['questions'])}")
                st.markdown(f"**Duration:** {s.get('duration_secs',0)//60}m {s.get('duration_secs',0)%60}s")
            with col2:
                st.markdown(f"**Overall Score:** <span style='color:{score_color}'>{s['total_score']}/10</span>", unsafe_allow_html=True)
                st.markdown(f"**Date:** {s['timestamp'][:19]}")

            st.markdown("**Per-Question Scores:**")
            for i, (q, sc) in enumerate(zip(s["questions"], s["scores"])):
                col_q, col_s = st.columns([5, 1])
                with col_q:
                    st.caption(f"Q{i+1}: {q[:80]}...")
                with col_s:
                    c = "#48bb78" if sc >= 7 else "#ecc94b" if sc >= 5 else "#fc8181"
                    st.markdown(f"<span style='color:{c}'>{sc}/10</span>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Router
# ─────────────────────────────────────────────
page = st.session_state.page
if page == "home":
    page_home()
elif page == "interview":
    page_interview()
elif page == "dashboard":
    page_dashboard()
elif page == "history":
    page_history()
