import streamlit as st
import pickle
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# Ensure NLTK resources are downloaded
nltk.download('punkt')
nltk.download('stopwords')

ps = PorterStemmer()

# Preprocessing function
def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

# Load model and vectorizer
tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))

# App config
st.set_page_config(
    page_title="Spam Classifier",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS for enhanced UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }

 .main-header {
    text-align: center;
    font-size: 4rem;
    font-weight: 900;
    color: #2C3E50; /* Deep, modern dark blue */
    letter-spacing: 1px;
    margin-bottom: 1.5rem;
    text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.15);
    border-bottom: 4px solid #FF6B6B;
    padding-bottom: 0.3rem;
}


    .stTextArea > div > div > textarea {
        border: 2px solid #f7971e;
        border-radius: 12px;
        padding: 16px;
        font-size: 18px;
        background: linear-gradient(to right, #e0eafc, #cfdef3);
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }

    .stButton > button {
        background: linear-gradient(to right, #ff416c, #ff4b2b);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0.8rem 2.5rem;
        font-size: 1.2rem;
        font-weight: 600;
        width: 100%;
        box-shadow: 0 10px 25px rgba(255, 65, 108, 0.3);
        transition: all 0.3s ease-in-out;
    }

    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 15px 35px rgba(255, 75, 43, 0.5);
    }

    .spam-result, .safe-result {
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        font-size: 2rem;
        font-weight: bold;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        animation-duration: 1s;
    }

    .spam-result {
        background: radial-gradient(circle, #ff416c 0%, #ff4b2b 100%);
        animation-name: shake;
    }

    .safe-result {
        background: radial-gradient(circle, #11998e 0%, #38ef7d 100%);
        animation-name: bounce;
    }

    @keyframes shake {
        10%, 90% { transform: translate3d(-1px, 0, 0); }
        20%, 80% { transform: translate3d(2px, 0, 0); }
        30%, 50%, 70% { transform: translate3d(-4px, 0, 0); }
        40%, 60% { transform: translate3d(4px, 0, 0); }
    }

    @keyframes bounce {
        0%, 20%, 53%, 80%, 100% { transform: translateY(0); }
        40%, 43% { transform: translateY(-30px); }
        70% { transform: translateY(-15px); }
        90% { transform: translateY(-4px); }
    }

    .info-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        text-align: center;
    }

    .metric-container {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 6px 20px rgba(240, 147, 251, 0.3);
    }

    .stApp {
        background: linear-gradient(120deg, #a1c4fd 0%, #c2e9fb 100%);
    }

    .main {
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(8px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 10px 35px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Main Header
st.markdown('<h1 class="main-header">🛡️ SPAM DETECTOR</h1>', unsafe_allow_html=True)

# Centered Layout
col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    st.markdown("""
    <div class="info-card">
        <h2 style="margin-top: 0;">Email/SMS Message Analyzer</h2>
        <p style="font-size: 1.1rem;">💡 Uses NLP & Machine Learning to detect spam messages instantly</p>
    </div>
    """, unsafe_allow_html=True)

    input_sms = st.text_area(
        "📱 Enter your message:",
        placeholder="Paste your email or SMS content here...",
        height=200
    )

    if st.button('🔍 ANALYZE MESSAGE'):
        if input_sms.strip():
            with st.spinner('🤖 Analyzing...'):
                transformed_sms = transform_text(input_sms)
                vector_input = tfidf.transform([transformed_sms])
                result = model.predict(vector_input)[0]
                
                if result == 1:
                    st.markdown('''
                    <div class="spam-result">
                        🚨 SPAM DETECTED 🚨<br>
                        <div style="font-size: 1.2rem; margin-top: 1rem;">
                            This message appears to be SPAM!
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                else:
                    st.markdown('''
                    <div class="safe-result">
                        ✅ LEGITIMATE MESSAGE ✅<br>
                        <div style="font-size: 1.2rem; margin-top: 1rem;">
                            This message appears to be SAFE!
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                    st.balloons()
        else:
            st.error("⚠️ Please enter a message to analyze!")

# Metrics at bottom
col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("""
    <div class="metric-container">
        <h3 style="margin: 0;">⚡ Speed</h3>
        <p style="margin: 0.5rem 0;">Instant Analysis</p>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div class="metric-container">
        <h3 style="margin: 0;">🎯 Accuracy</h3>
        <p style="margin: 0.5rem 0;">High Precision</p>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown("""
    <div class="metric-container">
        <h3 style="margin: 0;">🔒 Privacy</h3>
        <p style="margin: 0.5rem 0;">Secure Processing</p>
    </div>
    """, unsafe_allow_html=True)
