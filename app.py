import streamlit as st
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 🔥 Generator aur ML features ko import karo
import generator
from generator import generate_linkedin, generate_twitter, generate_email
from ml_features import analyze_sentiment, word_frequency, length_analysis

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Content Repurposing Pro",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- CUSTOM CSS (VIP Professional Look) ----------
st.markdown("""
<style>
    /* Main App Background - Dark */
    .stApp {
        background: #0e1117 !important;
    }
    
    /* Main Container - Dark Glass */
    .main > div {
        background: #1e1e2f !important;
        border-radius: 20px !important;
        padding: 25px !important;
        border: 1px solid #3a3a5c !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.5) !important;
    }
    
    /* ALL Headings - White & Bold */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    
    /* ALL Labels */
    label, .stTextArea label, .stTextInput label {
        color: #e0e0e0 !important;
        font-weight: 600 !important;
        font-size: 16px !important;
    }
    
    /* Text Box (Input Area) */
    .stTextArea textarea {
        background-color: #2a2a3e !important;
        color: #ffffff !important;
        font-size: 16px !important;
        border: 2px solid #4a4a6a !important;
        border-radius: 12px !important;
        padding: 15px !important;
        min-height: 150px !important;
    }
    .stTextArea textarea:focus {
        border-color: #6C63FF !important;
        box-shadow: 0 0 20px rgba(108, 99, 255, 0.3) !important;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(90deg, #6C63FF, #4a3fd9) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 12px 30px !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(108, 99, 255, 0.4) !important;
    }
    .stButton button:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 8px 25px rgba(108, 99, 255, 0.6) !important;
    }
    
    /* Output Code Blocks */
    .stCodeBlock {
        background-color: #1a1a2e !important;
        border-radius: 12px !important;
        padding: 15px !important;
        border: 1px solid #3a3a5c !important;
    }
    .stCodeBlock div {
        color: #e8e8e8 !important;
        font-size: 15px !important;
        line-height: 1.6 !important;
    }
    
    /* Metrics */
    .stMetric {
        background: #1e1e32 !important;
        border-radius: 15px !important;
        padding: 15px !important;
        border: 1px solid #3a3a5c !important;
    }
    .stMetric label {
        color: #a0a0c0 !important;
        font-size: 14px !important;
    }
    .stMetric div {
        color: #ffffff !important;
        font-size: 28px !important;
        font-weight: 700 !important;
    }
    
    /* Sidebar */
    .css-1d391kg, .stSidebar {
        background: #161625 !important;
        border-right: 1px solid #2a2a44 !important;
    }
    .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar label {
        color: #e0e0e0 !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px !important;
        background: #1a1a2e !important;
        padding: 10px !important;
        border-radius: 15px !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: #a0a0c0 !important;
        font-weight: 600 !important;
        background: transparent !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
    }
    .stTabs [aria-selected="true"] {
        color: #ffffff !important;
        background: #6C63FF !important;
        border-radius: 10px !important;
    }
    
    /* File Uploader */
    .stFileUploader {
        background: #1a1a2e !important;
        border: 2px dashed #4a4a6a !important;
        border-radius: 15px !important;
        padding: 20px !important;
    }
    
    /* Alert/Error Messages */
    .stAlert {
        background: #2a1a1a !important;
        border-left: 5px solid #ff4444 !important;
        color: #ff8888 !important;
        border-radius: 12px !important;
    }
    .stSuccess {
        background: #1a2a1a !important;
        border-left: 5px solid #44ff44 !important;
        color: #88ff88 !important;
        border-radius: 12px !important;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---------- SESSION STATE INIT ----------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------- SIDEBAR ----------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/null/artificial-intelligence.png", width=80)
    st.title("⚙️ Control Panel")
    
    st.markdown("---")
    st.subheader("🛠️ Client Config (Day 4 Ready)")
    
    show_emoji = st.checkbox("Show Emojis", value=True)
    thread_format = st.selectbox("Thread Format", ["MODERN (1/5)", "CLASSIC (Tweet 1)"], index=0)
    
    if st.button("🔄 Apply Client Changes", use_container_width=True):
        generator.CONFIG["SHOW_EMOJI"] = show_emoji
        generator.CONFIG["THREAD_FORMAT"] = "MODERN" if "MODERN" in thread_format else "CLASSIC"
        st.success("✅ Config updated! (Client Request Applied)")
        st.balloons()

    st.markdown("---")
    st.caption("⚡ Built by Sanaullah Kaka")

# ---------- MAIN UI ----------
st.title("📝 Content Repurposing Pro")
st.caption("Transform your blog into LinkedIn, Twitter, and Email content instantly using NLP & ML.")

# Top Metrics (Cost Removed)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Requests", len(st.session_state.history))
with col2:
    st.metric("Active Emojis", "✅ ON" if generator.CONFIG["SHOW_EMOJI"] else "❌ OFF")
with col3:
    st.metric("Thread Format", generator.CONFIG["THREAD_FORMAT"])

# ---------- TABS ----------
tab1, tab2 = st.tabs(["📄 Single Blog", "📂 Batch Upload"])

# ==========================================
# -------------------- TAB 1: SINGLE BLOG --------------------
# ==========================================
with tab1:
    input_text = st.text_area("✍️ Paste your blog content here:", height=200)
    
    if st.button("🚀 Generate", use_container_width=True, type="primary"):
        if not input_text.strip():
            st.error("❌ Please paste some text first!")
        else:
            with st.spinner("⏳ Processing your content... Please wait."):
                time.sleep(0.5)
                linkedin = generate_linkedin(input_text)
                twitter = generate_twitter(input_text)
                email = generate_email(input_text)
                
                st.session_state.history.append({
                    "input": input_text[:100] + "...",
                    "linkedin": linkedin[:100] + "...",
                    "twitter": twitter[:100] + "...",
                    "email": email[:100] + "..."
                })
            
            st.success(f"✅ Generated successfully!")
            
            # Outputs
            col1, col2, col3 = st.columns(3)
            with col1:
                st.subheader("💼 LinkedIn")
                st.code(linkedin, language="markdown")
                st.download_button("📥 Download", linkedin, file_name="linkedin_post.txt", use_container_width=True)
            with col2:
                st.subheader("🐦 Twitter Thread")
                st.code(twitter, language="markdown")
                st.download_button("📥 Download", twitter, file_name="twitter_thread.txt", use_container_width=True)
            with col3:
                st.subheader("📧 Email Newsletter")
                st.code(email, language="markdown")
                st.download_button("📥 Download", email, file_name="email_newsletter.txt", use_container_width=True)

            # ---------- ML FEATURES ----------
            st.markdown("---")
            st.subheader("🧠 ML/NLP Analysis")

            # Sentiment Analysis
            sentiment_label, polarity = analyze_sentiment(input_text)
            col_s1, col_s2 = st.columns(2)
            
            with col_s1:
                st.metric("Sentiment", sentiment_label)
            with col_s2:
                st.metric("Polarity Score", f"{polarity:.2f}")

            # Word Frequency Chart
            st.subheader("📊 Word Frequency (Top 10)")
            freq = word_frequency(input_text, top_n=10)
            if freq:
                fig = go.Figure(data=[go.Bar(x=list(freq.keys()), y=list(freq.values()), marker_color='#6C63FF')])
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    xaxis_title="Words",
                    yaxis_title="Frequency"
                )
                st.plotly_chart(fig, use_container_width=True)

            # Length Analysis
            st.subheader("📏 Text Statistics")
            analysis = length_analysis(input_text, [linkedin, twitter, email])
            st.json(analysis)


# ==========================================
# -------------------- TAB 2: BATCH MODE --------------------
# ==========================================
with tab2:
    st.subheader("📂 Process Multiple Blogs at Once")
    st.caption("Upload a CSV file with a column named 'text'")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        if "text" not in df.columns:
            st.error("❌ CSV must have a column named 'text'.")
        else:
            st.info(f"📊 Found **{len(df)}** blogs to process.")
            if st.button("🔁 Start Batch Processing", use_container_width=True):
                progress_bar = st.progress(0)
                status_text = st.empty()
                results = []
                
                for idx, row in df.iterrows():
                    status_text.text(f"⏳ Processing {idx+1} of {len(df)}...")
                    text = row["text"]
                    
                    linkedin = generate_linkedin(text)
                    twitter = generate_twitter(text)
                    email = generate_email(text)
                    
                    results.append({
                        "input": text[:50] + "...",
                        "linkedin": linkedin[:50] + "...",
                        "twitter": twitter[:50] + "...",
                        "email": email[:50] + "..."
                    })
                    
                    progress_bar.progress((idx + 1) / len(df))
                    time.sleep(0.2)
                
                status_text.text("✅ Batch processing complete!")
                st.dataframe(pd.DataFrame(results))
                
                csv_download = pd.DataFrame(results).to_csv(index=False)
                st.download_button("📥 Download Results CSV", csv_download, file_name="batch_results.csv", use_container_width=True)

# ---------- FOOTER ----------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #8888aa; padding: 20px;">
    <p>Made with ❤️ using Streamlit | Content Repurposing Pro v2.0</p>
    <p style="font-size: 12px;">⚡ Ready for Day 4 Client Change Requests ⚡</p>
</div>
""", unsafe_allow_html=True)