import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ──────────────────────────────────────────────
# Page Config
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Exam Question Analysis System",
    page_icon="📝",
    layout="wide",
)

# ──────────────────────────────────────────────
# Custom CSS for a clean, modern look
# ──────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1a1a2e;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #555;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card h3 {
        margin: 0;
        font-size: 2rem;
    }
    .metric-card p {
        margin: 0;
        font-size: 0.9rem;
        opacity: 0.85;
    }
    .card {
        background: #f8f9fa;
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# Sidebar Navigation
# ──────────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/fluency/96/exam.png", width=80)
st.sidebar.title("📚 Navigation")
page = st.sidebar.radio(
    "Go to",
    [
        "🏠 Home",
        "📤 Upload Data",
        "📊 Difficulty Analysis",
        "👨‍🎓 Student Performance",
        "📈 Visualizations",
        "🤖 Model Evaluation",
    ],
)

st.sidebar.markdown("---")
st.sidebar.info("**Milestone 1** – ML-Based Exam Question Analytics")

# ──────────────────────────────────────────────
# Session State for uploaded data
# ──────────────────────────────────────────────
if "questions_df" not in st.session_state:
    st.session_state.questions_df = None
if "responses_df" not in st.session_state:
    st.session_state.responses_df = None


# ══════════════════════════════════════════════
# PAGE: Home
# ══════════════════════════════════════════════
if page == "🏠 Home":
    st.markdown('<p class="main-header">📝 Intelligent Exam Question Analysis</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-driven system to assess exam question quality, difficulty, and student performance patterns.</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>📤</h3>
            <p>Upload exam questions & student responses</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <h3>📊</h3>
            <p>Analyze difficulty & quality classifications</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <h3>📈</h3>
            <p>Visualize performance trends & insights</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.subheader("🔑 Key Features")
    features = {
        "Question Difficulty Prediction": "Classify questions as Easy, Medium, or Hard using Logistic Regression.",
        "Student Performance Patterns": "Analyze how students respond to each question.",
        "Text Feature Extraction": "TF-IDF based feature extraction from question text.",
        "Model Evaluation": "Accuracy, Precision, Recall & Confusion Matrix for Logistic Regression.",
        "Visual Insights": "Interactive charts for question-wise performance trends.",
    }
    for title, desc in features.items():
        st.markdown(f"""
        <div class="card">
            <strong>{title}</strong><br/>
            <span style="color:#666">{desc}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📐 System Architecture")
    st.markdown("""
    ```
    ┌──────────────┐    ┌──────────────────┐    ┌─────────────────┐
    │  Raw Data     │───▶│  Preprocessing   │───▶│ Feature         │
    │  (CSV Upload) │    │  & Text Cleaning │    │ Extraction      │
    └──────────────┘    └──────────────────┘    │ (TF-IDF)        │
                                                 └────────┬────────┘
                                                          │
                         ┌──────────────────┐    ┌────────▼────────┐
                         │ Difficulty        │◀───│ Logistic        │
                         │ Classification    │    │ Regression      │
                         └────────┬─────────┘    └─────────────────┘
                                  │
                         ┌────────▼─────────┐
                         │  Dashboard &      │
                         │  Visualizations   │
                         └──────────────────┘
    ```
    """)

# ══════════════════════════════════════════════
# PAGE: Upload Data
# ══════════════════════════════════════════════
elif page == "📤 Upload Data":
    st.markdown('<p class="main-header">📤 Upload Data</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Upload your exam questions and student response data (CSV format).</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📝 Exam Questions")
        st.caption("Expected columns: `Id`, `Title`, `Body`, `Score`, `Tags` (or similar)")
        questions_file = st.file_uploader("Upload Questions CSV", type=["csv"], key="q_upload")
        if questions_file is not None:
            st.session_state.questions_df = pd.read_csv(questions_file, encoding="latin1", nrows=5000)
            st.success(f"✅ Loaded {len(st.session_state.questions_df)} questions!")
            st.dataframe(st.session_state.questions_df.head(10), use_container_width=True)

    with col2:
        st.subheader("👨‍🎓 Student Responses / Answers")
        st.caption("Expected columns: `Id`, `ParentId`, `Body`, `Score` (or similar)")
        responses_file = st.file_uploader("Upload Responses CSV", type=["csv"], key="r_upload")
        if responses_file is not None:
            st.session_state.responses_df = pd.read_csv(responses_file, encoding="latin1", nrows=5000)
            st.success(f"✅ Loaded {len(st.session_state.responses_df)} responses!")
            st.dataframe(st.session_state.responses_df.head(10), use_container_width=True)

    st.markdown("---")
    if st.session_state.questions_df is not None:
        st.subheader("📋 Questions Data Summary")
        st.write(st.session_state.questions_df.describe())
    if st.session_state.responses_df is not None:
        st.subheader("📋 Responses Data Summary")
        st.write(st.session_state.responses_df.describe())


# ══════════════════════════════════════════════
# PAGE: Difficulty Analysis
# ══════════════════════════════════════════════
elif page == "📊 Difficulty Analysis":
    st.markdown('<p class="main-header">📊 Difficulty Classification</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Questions classified as Easy, Medium, or Hard based on their score distribution.</p>', unsafe_allow_html=True)

    if st.session_state.questions_df is not None:
        df = st.session_state.questions_df.copy()

        # Simple difficulty classification based on Score column
        score_col = None
        for col in ["Score", "score", "OwnerUserId"]:
            if col in df.columns:
                score_col = col
                break

        if score_col and pd.api.types.is_numeric_dtype(df[score_col]):
            q_low = df[score_col].quantile(0.33)
            q_high = df[score_col].quantile(0.66)

            df["Difficulty"] = pd.cut(
                df[score_col],
                bins=[-np.inf, q_low, q_high, np.inf],
                labels=["Hard", "Medium", "Easy"],
            )

            # Show metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Questions", len(df))
            with col2:
                st.metric("🟢 Easy", int((df["Difficulty"] == "Easy").sum()))
            with col3:
                st.metric("🟡 Medium", int((df["Difficulty"] == "Medium").sum()))
            with col4:
                st.metric("🔴 Hard", int((df["Difficulty"] == "Hard").sum()))

            st.markdown("---")

            # Difficulty distribution bar chart
            st.subheader("Difficulty Distribution")
            diff_counts = df["Difficulty"].value_counts()
            fig, ax = plt.subplots(figsize=(6, 4))
            colors = ["#2ecc71", "#f39c12", "#e74c3c"]
            diff_counts.reindex(["Easy", "Medium", "Hard"]).plot(
                kind="bar", ax=ax, color=colors, edgecolor="white", linewidth=1.5
            )
            ax.set_ylabel("Number of Questions")
            ax.set_xlabel("Difficulty Level")
            ax.set_title("Question Difficulty Distribution")
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            plt.xticks(rotation=0)
            plt.tight_layout()
            st.pyplot(fig)

            st.markdown("---")

            # Show the classified table
            st.subheader("Classified Questions")
            display_cols = [c for c in ["Id", "Title", "Score", score_col, "Difficulty"] if c in df.columns]
            display_cols = list(dict.fromkeys(display_cols))  # remove duplicates
            st.dataframe(df[display_cols].head(50), use_container_width=True)

        else:
            st.warning("⚠️ Could not find a numeric 'Score' column to classify difficulty. Please check your data.")
    else:
        st.info("👈 Please upload questions data first from the **Upload Data** page.")
