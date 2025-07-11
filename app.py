import streamlit as st
import pickle
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()

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

tfidf = pickle.load(open('vectorizer.pkl','rb'))
model = pickle.load(open('model.pkl','rb'))

st.set_page_config(
    page_title="Spam Classifier",
    page_icon="🛡️",
    layout="wide"
)

st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #FF6B6B;
        font-size: 3.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .stTextArea > div > div > textarea {
        border: 3px solid #4ECDC4;
        border-radius: 15px;
        padding: 20px;
        font-size: 18px;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 1rem 3rem;
        font-size: 1.3rem;
        font-weight: bold;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(255, 107, 107, 0.4);
    }
    
    .spam-result {
        background: linear-gradient(45deg, #FF416C, #FF4B2B);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        font-size: 2rem;
        font-weight: bold;
        margin: 2rem 0;
        box-shadow: 0 8px 25px rgba(255, 65, 108, 0.3);
        animation: shake 0.82s cubic-bezier(.36,.07,.19,.97) both;
    }
    
    .safe-result {
        background: linear-gradient(45deg, #56ab2f, #a8e6cf);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        font-size: 2rem;
        font-weight: bold;
        margin: 2rem 0;
        box-shadow: 0 8px 25px rgba(86, 171, 47, 0.3);
        animation: bounce 0.6s ease-out;
    }
    
    @keyframes shake {
        10%, 90% { transform: translate3d(-1px, 0, 0); }
        20%, 80% { transform: translate3d(2px, 0, 0); }
        30%, 50%, 70% { transform: translate3d(-4px, 0, 0); }
        40%, 60% { transform: translate3d(4px, 0, 0); }
    }
    
    @keyframes bounce {
        0%, 20%, 53%, 80%, 100% { transform: translate3d(0,0,0); }
        40%, 43% { transform: translate3d(0,-30px,0); }
        70% { transform: translate3d(0,-15px,0); }
        90% { transform: translate3d(0,-4px,0); }
    }
    
    .info-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
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
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🛡️ SPAM DETECTOR</h1>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    st.markdown("""
    <div class="info-card">
        <h2 style="margin-top: 0; text-align: center;">Email/SMS Message Analyzer</h2>
        <p style="text-align: center; font-size: 1.1rem;">Advanced machine learning technology to detect spam messages instantly</p>
    </div>
    """, unsafe_allow_html=True)

    input_sms = st.text_area(
        "📱 Enter your message:",
        placeholder="Paste your email or SMS content here for analysis...",
        height=200
    )

    if st.button('🔍 ANALYZE MESSAGE'):
        if input_sms.strip():
            with st.spinner('🤖 Processing...'):
                transformed_sms = transform_text(input_sms)
                vector_input = tfidf.transform([transformed_sms])
                result = model.predict(vector_input)[0]
                
                if result == 1:
                    st.markdown('''
                    <div class="spam-result">
                        🚨 SPAM DETECTED 🚨<br>
                        <div style="font-size: 1.2rem; margin-top: 1rem;">
                            This message appears to be spam!
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                else:
                    st.markdown('''
                    <div class="safe-result">
                        ✅ LEGITIMATE MESSAGE ✅<br>
                        <div style="font-size: 1.2rem; margin-top: 1rem;">
                            This message appears to be safe!
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
        else:
            st.error("⚠️ Please enter a message to analyze!")

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