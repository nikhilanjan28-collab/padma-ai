import streamlit as st
import os, PyPDF2, groq, datetime

# 1. యాప్ సెట్టింగ్స్
st.set_page_config(page_title="Padma AI Services", layout="wide", page_icon="🔮")
st.title("🔮 Padma AI Services")
st.markdown("### గ్రంథాలు మరియు ఆన్లైన్ ఏఐ ఆధారిత జాతక విశ్లేషణ")

# 2. యూజర్ ఇన్పుట్ (పేరు కనబడదు - ఏజ్ లిమిట్ అలాగే ఉంటుంది)
col1, col2 = st.columns(2)
with col1:
    user_name = st.text_input("మీ పేరు నమోదు చేయండి:", placeholder="మీ పేరు ఇక్కడ టైప్ చేయండి")
    birth_date = st.date_input("మీ పుట్టిన తేదీని ఎంచుకోండి:", 
                               min_value=datetime.date(1900, 1, 1), 
                               max_value=datetime.date(2100, 12, 31))
with col2:
    birth_time = st.time_input("పుట్టిన సమయం (అంచనా):")
    zodiac = st.selectbox("మీ రాశిని ఎంచుకోండి:", [
        'మేషం ♈', 'వృషభం ♉', 'మిథునం ♊', 'కర్కాటకం ♋', 
        'సింహం ♌', 'కన్య ♍', 'తుల ♎', 'వృశ్చికం ♏', 
        'ధనుస్సు ♐', 'మకరం ♑', 'కుంభం ♒', 'మీనం ♓'
    ])

# 3. ఫైల్ అప్‌లోడర్
st.divider()
st.subheader("📁 మీ దగ్గర ఉన్న జాతక గ్రంథాలు (PDF) అప్‌లోడ్ చేయండి")
files = st.file_uploader("పిడిఎఫ్ ఫైల్స్ ఇక్కడ వేయండి", accept_multiple_files=True)

# 4. విశ్లేషణ బటన్ (రెడ్ కలర్ తీసేసి బ్లూ కలర్ పెట్టాను)
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #0047AB;
        color: white;
        border-radius: 10px;
        width: 100%;
        height: 50px;
        font-size: 20px;
    }
    </style>""", unsafe_allow_html=True)

if st.button("జాతక నివేదిక పొందండి"):
    if user_name:
        with st.spinner("విశ్లేషిస్తున్నాను..."):
            book_context = ""
            if files:
                for f in files:
                    pdf = PyPDF2.PdfReader(f)
                    for page in pdf.pages[:50]: 
                        book_context += page.extract_text()
            
            client = groq.Groq(api_key="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")
            
            prompt = f"యూజర్ పేరు: {user_name}, పుట్టిన తేదీ: {birth_date}, రాశి: {zodiac}. పుస్తక డేటా: {book_context[:8000]}. వీటి ఆధారంగా తెలుగులో జాతకం చెప్పు."
            
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile", 
                messages=[{"role": "user", "content": prompt}]
            )
            
            st.success("విశ్లేషణ పూర్తయింది!")
            st.markdown(f"## 📜 జాతక ఫలితాలు")
            st.write(res.choices[0].message.content)
            st.balloons()
    else:
        st.warning("దయచేసి మీ పేరు నమోదు చేయండి!")

st.divider()
st.caption("© 2026 Padma AI Services")
